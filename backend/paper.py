from typing import Optional
from functools import cached_property
from tempfile import TemporaryDirectory, NamedTemporaryFile
import arxiv
import tarfile
import re
from .llm import get_llm
import requests
from requests.adapters import HTTPAdapter, Retry
from loguru import logger
import tiktoken
from contextlib import ExitStack
import shutil
import os
import ssl
from urllib.error import URLError



class ArxivPaper:
    def __init__(self,paper:arxiv.Result):
        self._paper = paper
        self.score = None
    
    @property
    def title(self) -> str:
        return self._paper.title
    
    @property
    def summary(self) -> str:
        return self._paper.summary
    
    @property
    def authors(self) -> list[str]:
        return self._paper.authors
    
    @cached_property
    def arxiv_id(self) -> str:
        return re.sub(r'v\d+$', '', self._paper.get_short_id())
    
    @property
    def pdf_url(self) -> str:
        return self._paper.pdf_url

    @property
    def published(self):
        return getattr(self._paper, "published", None)

    @property
    def categories(self) -> list:
        return getattr(self._paper, "categories", []) or []

    @cached_property
    def code_url(self) -> Optional[str]:
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1)
        s.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            paper_list = s.get(f'https://paperswithcode.com/api/v1/papers/?arxiv_id={self.arxiv_id}').json()
        except Exception as e:
            logger.debug(f'Error when searching {self.arxiv_id}: {e}')
            return None

        if paper_list.get('count',0) == 0:
            return None
        paper_id = paper_list['results'][0]['id']

        try:
            repo_list = s.get(f'https://paperswithcode.com/api/v1/papers/{paper_id}/repositories/').json()
        except Exception as e:
            logger.debug(f'Error when searching {self.arxiv_id}: {e}')
            return None
        if repo_list.get('count',0) == 0:
            return None
        return repo_list['results'][0]['url']
    
    @cached_property
    def tex(self) -> dict[str,str]:
        with ExitStack() as stack:
            tmpdirname = stack.enter_context(TemporaryDirectory())
            try:
                file = self._paper.download_source(dirpath=tmpdirname)
            except (URLError, ssl.SSLError, OSError) as e:
                logger.debug(f"Failed to download source for {self.arxiv_id}: {e}")
                return None
            try:
                tar = stack.enter_context(tarfile.open(file))
            except tarfile.ReadError:
                logger.debug(f"Failed to find main tex file of {self.arxiv_id}: Not a tar file.")
                return None
 
            tex_files = [f for f in tar.getnames() if f.endswith('.tex')]
            if len(tex_files) == 0:
                logger.debug(f"Failed to find main tex file of {self.arxiv_id}: No tex file.")
                return None
            
            bbl_file = [f for f in tar.getnames() if f.endswith('.bbl')]
            match len(bbl_file) :
                case 0:
                    if len(tex_files) > 1:
                        logger.debug(f"Cannot find main tex file of {self.arxiv_id} from bbl: There are multiple tex files while no bbl file.")
                        main_tex = None
                    else:
                        main_tex = tex_files[0]
                case 1:
                    main_name = bbl_file[0].replace('.bbl','')
                    main_tex = f"{main_name}.tex"
                    if main_tex not in tex_files:
                        logger.debug(f"Cannot find main tex file of {self.arxiv_id} from bbl: The bbl file does not match any tex file.")
                        main_tex = None
                case _:
                    logger.debug(f"Cannot find main tex file of {self.arxiv_id} from bbl: There are multiple bbl files.")
                    main_tex = None
            if main_tex is None:
                logger.debug(f"Trying to choose tex file containing the document block as main tex file of {self.arxiv_id}")
            #read all tex files
            file_contents = {}
            for t in tex_files:
                f = tar.extractfile(t)
                content = f.read().decode('utf-8',errors='ignore')
                #remove comments
                content = re.sub(r'%.*\n', '\n', content)
                content = re.sub(r'\\begin{comment}.*?\\end{comment}', '', content, flags=re.DOTALL)
                content = re.sub(r'\\iffalse.*?\\fi', '', content, flags=re.DOTALL)
                #remove redundant \n
                content = re.sub(r'\n+', '\n', content)
                content = re.sub(r'\\\\', '', content)
                #remove consecutive spaces
                content = re.sub(r'[ \t\r\f]{3,}', ' ', content)
                if main_tex is None and re.search(r'\\begin\{document\}', content):
                    main_tex = t
                    logger.debug(f"Choose {t} as main tex file of {self.arxiv_id}")
                file_contents[t] = content
            
            if main_tex is not None:
                main_source:str = file_contents[main_tex]
                #find and replace all included sub-files
                include_files = re.findall(r'\\input\{(.+?)\}', main_source) + re.findall(r'\\include\{(.+?)\}', main_source)
                for f in include_files:
                    if not f.endswith('.tex'):
                        file_name = f + '.tex'
                    else:
                        file_name = f
                    main_source = main_source.replace(f'\\input{{{f}}}', file_contents.get(file_name, ''))
                file_contents["all"] = main_source
            else:
                logger.debug(f"Failed to find main tex file of {self.arxiv_id}: No tex file containing the document block.")
                file_contents["all"] = None
        return file_contents
    
    @cached_property
    def tldr(self) -> str:
        introduction = ""
        conclusion = ""
        if self.tex is not None:
            content = self.tex.get("all")
            if content is None:
                content = "\n".join(self.tex.values())
            #remove cite
            content = re.sub(r'~?\\cite.?\{.*?\}', '', content)
            #remove figure
            content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
            #remove table
            content = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '', content, flags=re.DOTALL)
            #find introduction and conclusion
            # end word can be \section or \end{document} or \bibliography or \appendix
            match = re.search(r'\\section\{Introduction\}.*?(\\section|\\end\{document\}|\\bibliography|\\appendix|$)', content, flags=re.DOTALL)
            if match:
                introduction = match.group(0)
            match = re.search(r'\\section\{Conclusion\}.*?(\\section|\\end\{document\}|\\bibliography|\\appendix|$)', content, flags=re.DOTALL)
            if match:
                conclusion = match.group(0)
        llm = get_llm()
        prompt = """Given the title, abstract, introduction and the conclusion (if any) of a paper in latex format, generate a one-sentence TLDR summary in __LANG__:
        
        \\title{__TITLE__}
        \\begin{abstract}__ABSTRACT__\\end{abstract}
        __INTRODUCTION__
        __CONCLUSION__
        """
        prompt = prompt.replace('__LANG__', llm.lang)
        prompt = prompt.replace('__TITLE__', self.title)
        prompt = prompt.replace('__ABSTRACT__', self.summary)
        prompt = prompt.replace('__INTRODUCTION__', introduction)
        prompt = prompt.replace('__CONCLUSION__', conclusion)

        # use gpt-4o tokenizer for estimation
        enc = tiktoken.encoding_for_model("gpt-4o")
        prompt_tokens = enc.encode(prompt)
        prompt_tokens = prompt_tokens[:4000]  # truncate to 4000 tokens
        prompt = enc.decode(prompt_tokens)
        
        tldr = llm.generate(
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant who perfectly summarizes scientific paper, and gives the core idea of the paper to the user.",
                },
                {"role": "user", "content": prompt},
            ]
        )
        return tldr

    def to_web_dict(self) -> dict:
        """JSON-serializable dict for web display (daily recommendations)."""
        author_names = [
            getattr(a, "name", str(a)) for a in self._paper.authors
        ]
        return {
            "id": self.arxiv_id,
            "arxivId": self.arxiv_id,
            "title": self.title,
            "abstract": self.summary,
            "authors": author_names,
            "category": self.categories[0] if self.categories else "",
            "categories": self.categories,
            "date": self.published.strftime("%Y-%m-%d") if self.published else "",
            "link": f"https://arxiv.org/abs/{self.arxiv_id}",
            "pdf_url": self.pdf_url,
            "code_url": self.code_url,
            "tldr": self.tldr,
        }

    @cached_property
    def affiliations(self) -> Optional[list[str]]:
        if self.tex is not None:
            content = self.tex.get("all")
            if content is None:
                content = "\n".join(self.tex.values())
            #search for affiliations
            possible_regions = [r'\\author.*?\\maketitle',r'\\begin{document}.*?\\begin{abstract}']
            matches = [re.search(p, content, flags=re.DOTALL) for p in possible_regions]
            match = next((m for m in matches if m), None)
            if match:
                information_region = match.group(0)
            else:
                logger.debug(f"Failed to extract affiliations of {self.arxiv_id}: No author information found.")
                return None
            prompt = f"Given the author information of a paper in latex format, extract the affiliations of the authors in a python list format, which is sorted by the author order. If there is no affiliation found, return an empty list '[]'. Following is the author information:\n{information_region}"
            # use gpt-4o tokenizer for estimation
            enc = tiktoken.encoding_for_model("gpt-4o")
            prompt_tokens = enc.encode(prompt)
            prompt_tokens = prompt_tokens[:4000]  # truncate to 4000 tokens
            prompt = enc.decode(prompt_tokens)
            llm = get_llm()
            affiliations = llm.generate(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant who perfectly extracts affiliations of authors from the author information of a paper. You should return a python list of affiliations sorted by the author order, like ['TsingHua University','Peking University']. If an affiliation is consisted of multi-level affiliations, like 'Department of Computer Science, TsingHua University', you should return the top-level affiliation 'TsingHua University' only. Do not contain duplicated affiliations. If there is no affiliation found, you should return an empty list [ ]. You should only return the final list of affiliations, and do not return any intermediate results.",
                    },
                    {"role": "user", "content": prompt},
                ]
            )

            try:
                affiliations = re.search(r'\[.*?\]', affiliations, flags=re.DOTALL).group(0)
                affiliations = eval(affiliations)
                affiliations = list(set(affiliations))
                affiliations = [str(a) for a in affiliations]
            except Exception as e:
                logger.debug(f"Failed to extract affiliations of {self.arxiv_id}: {e}")
                return None
            return affiliations
    
    @cached_property
    def methodology_image(self) -> Optional[str]:
        """
        从 LaTeX 源码中提取第一张方法图/模型图
        
        通过分析 LaTeX 源码中的 figure 环境和 caption 来识别方法图：
        1. 解析所有 figure 环境
        2. 提取每个 figure 的 caption 文本
        3. 根据 caption 中的关键词评分（方法图关键词权重更高）
        4. 根据图片所在 section 评分（Methodology/Introduction 部分权重更高）
        5. 选择得分最高的图片
        
        Returns:
            Optional[str]: 图片文件路径（临时文件），如果找不到图片则返回 None
        """
        # 支持的图片格式
        image_extensions = ['.png', '.jpg', '.jpeg', '.eps', '.pdf']
        
        # 方法图关键词（高权重）
        methodology_keywords_high = [
            'architecture', 'framework', 'model', 'pipeline', 'system',
            'methodology', 'approach', 'method', 'structure', 'design',
            'overview', 'workflow', 'process', 'algorithm'
        ]
        
        # 方法图关键词（中权重）
        methodology_keywords_medium = [
            'proposed', 'novel', 'main', 'overall', 'illustration',
            'diagram', 'scheme', 'layout', 'network'
        ]
        
        # 需要排除的关键词（实验、结果类图片）
        exclude_keywords = [
            'result', 'experiment', 'evaluation', 'comparison', 'baseline',
            'performance', 'accuracy', 'loss', 'error', 'table', 'dataset',
            'example', 'sample', 'visualization', 'qualitative'
        ]
        
        # 相关 section 关键词
        methodology_sections = [
            'method', 'methodology', 'approach', 'framework', 'architecture',
            'model', 'system', 'proposed', 'introduction', 'overview'
        ]
        
        try:
            # 首先获取 LaTeX 源码
            if self.tex is None:
                logger.debug(f"No LaTeX source available for {self.arxiv_id}")
                return None
            
            tex_content = self.tex.get("all")
            if tex_content is None:
                logger.debug(f"No main LaTeX content for {self.arxiv_id}")
                return None
            
            # 提取所有 figure 环境
            # 匹配 \begin{figure}...\end{figure}，包括嵌套的 figure
            figure_pattern = r'\\begin\{figure\}(.*?)\\end\{figure\}'
            figures = re.findall(figure_pattern, tex_content, re.DOTALL | re.IGNORECASE)
            
            if len(figures) == 0:
                logger.debug(f"No figure environments found in {self.arxiv_id}")
                # 如果没有找到 figure 环境，回退到文件名匹配方法
                return self._extract_image_by_filename()
            
            # 解析每个 figure，提取 caption 和图片文件名
            figure_scores = []
            
            for fig_idx, figure_content in enumerate(figures):
                # 提取 caption
                caption_match = re.search(r'\\caption\{(.*?)\}', figure_content, re.DOTALL | re.IGNORECASE)
                caption_text = caption_match.group(1) if caption_match else ""
                
                # 清理 caption 文本（移除 LaTeX 命令）
                caption_clean = re.sub(r'\\[a-zA-Z]+\{.*?\}', '', caption_text)  # 移除命令
                caption_clean = re.sub(r'\\[a-zA-Z]+', '', caption_clean)  # 移除单独的命令
                caption_clean = re.sub(r'[{}]', '', caption_clean)  # 移除大括号
                caption_lower = caption_clean.lower()
                
                # 提取图片文件名（支持多种格式）
                # \includegraphics{filename} 或 \includegraphics[options]{filename}
                includegraphics_pattern = r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}'
                image_matches = re.findall(includegraphics_pattern, figure_content, re.IGNORECASE)
                
                if len(image_matches) == 0:
                    continue
                
                # 取第一个图片（通常一个 figure 只有一个主图）
                image_filename = image_matches[0]
                # 移除可能的路径，只保留文件名
                image_filename = os.path.basename(image_filename)
                # 移除可能的扩展名（LaTeX 中可能不包含扩展名）
                image_base = os.path.splitext(image_filename)[0]
                
                # 计算 caption 得分
                caption_score = 0
                
                # 检查排除关键词
                if any(keyword in caption_lower for keyword in exclude_keywords):
                    caption_score -= 10  # 大幅降低得分
                
                # 高权重关键词
                for keyword in methodology_keywords_high:
                    if keyword in caption_lower:
                        caption_score += 5
                
                # 中权重关键词
                for keyword in methodology_keywords_medium:
                    if keyword in caption_lower:
                        caption_score += 2
                
                # 检查图片所在 section
                section_score = 0
                # 找到 figure 在文档中的位置
                fig_start_pos = tex_content.find(f'\\begin{{figure}}')
                if fig_start_pos > 0:
                    # 查找最近的 \section 或 \subsection
                    before_fig = tex_content[:fig_start_pos]
                    section_matches = re.findall(r'\\section\{(.*?)\}|\\subsection\{(.*?)\}', before_fig, re.IGNORECASE)
                    if section_matches:
                        # 取最后一个 section（最近的）
                        last_section = section_matches[-1]
                        section_title = (last_section[0] or last_section[1]).lower()
                        if any(keyword in section_title for keyword in methodology_sections):
                            section_score += 3
                
                # 文件名匹配得分（作为补充）
                filename_score = 0
                image_lower = image_filename.lower()
                if any(keyword in image_lower for keyword in methodology_keywords_high):
                    filename_score += 2
                elif any(keyword in image_lower for keyword in methodology_keywords_medium):
                    filename_score += 1
                
                # 排除文件名中的排除关键词
                if any(keyword in image_lower for keyword in exclude_keywords):
                    filename_score -= 5
                
                # 总得分
                total_score = caption_score + section_score + filename_score
                
                figure_scores.append({
                    'filename': image_filename,
                    'base': image_base,
                    'caption': caption_clean,
                    'score': total_score,
                    'index': fig_idx
                })
                
                logger.debug(f"Figure {fig_idx}: {image_filename}, caption: {caption_clean[:50]}..., score: {total_score}")
            
            if len(figure_scores) == 0:
                logger.debug(f"No valid figures found in {self.arxiv_id}")
                return self._extract_image_by_filename()
            
            # 按得分排序，选择得分最高的
            figure_scores.sort(key=lambda x: x['score'], reverse=True)
            best_figure = figure_scores[0]
            
            logger.debug(f"Best figure for {self.arxiv_id}: {best_figure['filename']}, score: {best_figure['score']}, caption: {best_figure['caption'][:50]}...")
            
            # 现在从 tar 文件中提取图片
            with ExitStack() as stack:
                tmpdirname = stack.enter_context(TemporaryDirectory())
                file = self._paper.download_source(dirpath=tmpdirname)
                
                try:
                    tar = stack.enter_context(tarfile.open(file))
                except tarfile.ReadError:
                    logger.debug(f"Failed to extract image from {self.arxiv_id}: Not a tar file.")
                    return None
                
                # 获取所有文件列表
                all_files = tar.getnames()
                
                # 查找匹配的图片文件（支持多种扩展名和路径）
                selected_image = None
                best_base = best_figure['base'].lower()
                best_filename = best_figure['filename'].lower()
                
                # 优先级：1. 完全匹配文件名 2. 匹配基础名（不含扩展名）
                for f in all_files:
                    f_lower = f.lower()
                    # 检查文件扩展名
                    if not any(f_lower.endswith(ext) for ext in image_extensions):
                        continue
                    
                    # 排除明显不是方法图的文件
                    if any(skip in f_lower for skip in ['logo', 'icon', 'author', 'affiliation']):
                        continue
                    
                    f_base = os.path.splitext(os.path.basename(f))[0].lower()
                    
                    # 完全匹配文件名或基础名
                    if f_lower.endswith(best_filename) or f_base == best_base:
                        selected_image = f
                        break
                
                # 如果没找到，尝试匹配基础名（可能扩展名不同）
                if selected_image is None:
                    for f in all_files:
                        f_lower = f.lower()
                        if not any(f_lower.endswith(ext) for ext in image_extensions):
                            continue
                        if any(skip in f_lower for skip in ['logo', 'icon', 'author', 'affiliation']):
                            continue
                        
                        f_base = os.path.splitext(os.path.basename(f))[0].lower()
                        # 基础名匹配（允许不同的扩展名）
                        if best_base in f_base or f_base in best_base:
                            selected_image = f
                            break
                
                # 如果还是没找到，使用得分最高的图片文件名直接查找
                if selected_image is None:
                    for f in all_files:
                        f_lower = f.lower()
                        if not any(f_lower.endswith(ext) for ext in image_extensions):
                            continue
                        if any(skip in f_lower for skip in ['logo', 'icon', 'author', 'affiliation']):
                            continue
                        
                        # 文件名包含基础名的一部分
                        if best_base[:5] in f_lower or any(part in f_lower for part in best_base.split('_') if len(part) > 3):
                            selected_image = f
                            break
                
                if selected_image is None:
                    logger.debug(f"Could not find image file matching {best_figure['filename']} in tar")
                    # 回退到文件名匹配方法
                    return self._extract_image_by_filename()
                
                # 提取图片文件
                try:
                    tar_member = tar.getmember(selected_image)
                    extracted_file = tar.extractfile(tar_member)
                    if extracted_file is None:
                        logger.debug(f"Failed to extract image file {selected_image} from {self.arxiv_id}")
                        return None
                    
                    # 读取图片数据
                    image_data = extracted_file.read()
                    
                    # 确定文件扩展名
                    file_ext = os.path.splitext(selected_image)[1].lower()
                    if file_ext not in ['.png', '.jpg', '.jpeg']:
                        logger.debug(f"Image format {file_ext} not supported for WeChat, skipping: {selected_image}")
                        return None
                    
                    # 创建临时文件保存图片
                    temp_file = NamedTemporaryFile(
                        suffix=file_ext,
                        prefix=f'arxiv_{self.arxiv_id}_',
                        delete=False
                    )
                    temp_file.write(image_data)
                    temp_file.close()
                    
                    # 检查文件大小（微信公众号限制 1MB）
                    file_size = os.path.getsize(temp_file.name)
                    if file_size > 1024 * 1024:  # 1MB
                        logger.warning(f"Image file too large ({file_size} bytes) for {self.arxiv_id}, skipping")
                        os.unlink(temp_file.name)
                        return None
                    
                    logger.success(f"Extracted methodology image for {self.arxiv_id}: {selected_image} (score: {best_figure['score']}, caption: {best_figure['caption'][:30]}...)")
                    return temp_file.name
                    
                except Exception as e:
                    logger.debug(f"Failed to extract image {selected_image} from {self.arxiv_id}: {e}")
                    return None
                    
        except Exception as e:
            logger.debug(f"Error extracting methodology image for {self.arxiv_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            # 回退到文件名匹配方法
            return self._extract_image_by_filename()
    
    def _extract_image_by_filename(self) -> Optional[str]:
        """
        回退方法：通过文件名匹配提取图片（原始方法）
        
        Returns:
            Optional[str]: 图片文件路径（临时文件），如果找不到图片则返回 None
        """
        # 支持的图片格式
        image_extensions = ['.png', '.jpg', '.jpeg', '.eps', '.pdf']
        # 方法图关键词（小写）
        methodology_keywords = ['method', 'architecture', 'framework', 'model', 'overview', 
                               'pipeline', 'system', 'approach', 'structure', 'design']
        
        try:
            with ExitStack() as stack:
                tmpdirname = stack.enter_context(TemporaryDirectory())
                file = self._paper.download_source(dirpath=tmpdirname)
                
                try:
                    tar = stack.enter_context(tarfile.open(file))
                except tarfile.ReadError:
                    return None
                
                # 获取所有文件列表
                all_files = tar.getnames()
                
                # 筛选图片文件
                image_files = []
                for f in all_files:
                    if any(f.lower().endswith(ext) for ext in image_extensions):
                        f_lower = f.lower()
                        if any(skip in f_lower for skip in ['logo', 'icon', 'author', 'affiliation']):
                            continue
                        image_files.append(f)
                
                if len(image_files) == 0:
                    return None
                
                # 优先查找包含方法图关键词的图片
                methodology_images = []
                other_images = []
                
                for img_file in image_files:
                    img_lower = img_file.lower()
                    if any(keyword in img_lower for keyword in methodology_keywords):
                        methodology_images.append(img_file)
                    else:
                        other_images.append(img_file)
                
                # 选择图片
                selected_image = None
                if len(methodology_images) > 0:
                    selected_image = methodology_images[0]
                elif len(other_images) > 0:
                    selected_image = other_images[0]
                
                if selected_image is None:
                    return None
                
                # 提取图片文件
                try:
                    tar_member = tar.getmember(selected_image)
                    extracted_file = tar.extractfile(tar_member)
                    if extracted_file is None:
                        return None
                    
                    image_data = extracted_file.read()
                    file_ext = os.path.splitext(selected_image)[1].lower()
                    if file_ext not in ['.png', '.jpg', '.jpeg']:
                        return None
                    
                    temp_file = NamedTemporaryFile(
                        suffix=file_ext,
                        prefix=f'arxiv_{self.arxiv_id}_',
                        delete=False
                    )
                    temp_file.write(image_data)
                    temp_file.close()
                    
                    file_size = os.path.getsize(temp_file.name)
                    if file_size > 1024 * 1024:
                        os.unlink(temp_file.name)
                        return None
                    
                    return temp_file.name
                    
                except Exception as e:
                    logger.debug(f"Failed to extract image in fallback method: {e}")
                    return None
                    
        except Exception as e:
            logger.debug(f"Error in fallback image extraction: {e}")
            return None