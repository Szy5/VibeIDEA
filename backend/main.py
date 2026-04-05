import arxiv
import argparse
import os
import sys
import datetime
from dotenv import load_dotenv

# 从项目根目录加载 .env（支持从 repo 根或 backend 目录运行）
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_ROOT_DIR, ".env"), override=True)

# 代理：在 .env 中配置 HTTP_PROXY / HTTPS_PROXY 后，requests、huggingface_hub 等会自动使用
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from pyzotero import zotero
from recommender import rerank_paper
from construct_email import render_email, send_email
from construct_wechat import render_wechat
from construct_feishu import render_feishu
try:
    from wechat_publisher import WechatClient
except ImportError:
    WechatClient = None
from tqdm import trange, tqdm
from loguru import logger
from gitignore_parser import parse_gitignore
from tempfile import mkstemp
from paper import ArxivPaper
from llm import set_global_llm
import feedparser

def get_zotero_corpus(id:str,key:str) -> list[dict]:
    zot = zotero.Zotero(id, 'user', key)
    collections = zot.everything(zot.collections())
    collections = {c['key']:c for c in collections}
    corpus = zot.everything(zot.items(itemType='conferencePaper || journalArticle || preprint'))
    corpus = [c for c in corpus if c['data']['abstractNote'] != '']
    def get_collection_path(col_key:str) -> str:
        if p := collections[col_key]['data']['parentCollection']:
            return get_collection_path(p) + '/' + collections[col_key]['data']['name']
        else:
            return collections[col_key]['data']['name']
    for c in corpus:
        paths = [get_collection_path(col) for col in c['data']['collections']]
        c['paths'] = paths
    return corpus

def filter_corpus(corpus:list[dict], pattern:str) -> list[dict]:
    _,filename = mkstemp()
    with open(filename,'w') as file:
        file.write(pattern)
    matcher = parse_gitignore(filename,base_dir=_ROOT_DIR)
    new_corpus = []
    for c in corpus:
        match_results = [matcher(p) for p in c['paths']]
        if not any(match_results):
            new_corpus.append(c)
    os.remove(filename)
    return new_corpus


def get_arxiv_paper(query:str, debug:bool=False) -> list[ArxivPaper]:
    client = arxiv.Client(num_retries=10,delay_seconds=10)
    feed = feedparser.parse(f"https://rss.arxiv.org/atom/{query}")
    if 'Feed error for query' in feed.feed.title:
        raise Exception(f"Invalid ARXIV_QUERY: {query}.")
    if not debug:
        papers = []
        all_paper_ids = [i.id.removeprefix("oai:arXiv.org:") for i in feed.entries if i.arxiv_announce_type == 'new']
        bar = tqdm(total=len(all_paper_ids),desc="Retrieving Arxiv papers")
        for i in range(0,len(all_paper_ids),50):
            search = arxiv.Search(id_list=all_paper_ids[i:i+50])
            batch = [ArxivPaper(p) for p in client.results(search)]
            bar.update(len(batch))
            papers.extend(batch)
        bar.close()

    else:
        logger.debug("Retrieve 50 arxiv papers regardless of the date.")
        search = arxiv.Search(query='cat:cs.AI', sort_by=arxiv.SortCriterion.SubmittedDate)
        papers = []
        for i in client.results(search):
            papers.append(ArxivPaper(i))
            if len(papers) == 50:
                break

    return papers



parser = argparse.ArgumentParser(description='Recommender system for academic papers')

def add_argument(*args, **kwargs):
    def get_env(key:str,default=None):
        # handle environment variables generated at Workflow runtime
        # Unset environment variables are passed as '', we should treat them as None
        v = os.environ.get(key)
        if v == '' or v is None:
            return default
        return v
    parser.add_argument(*args, **kwargs)
    arg_full_name = kwargs.get('dest',args[-1][2:])
    env_name = arg_full_name.upper()
    env_value = get_env(env_name)
    if env_value is not None:
        #convert env_value to the specified type
        if kwargs.get('type') == bool:
            env_value = env_value.lower() in ['true','1']
        else:
            env_value = kwargs.get('type')(env_value)
        parser.set_defaults(**{arg_full_name:env_value})


if __name__ == '__main__':
    # 所有配置均可通过 .env 或环境变量覆盖，敏感信息请只写在 .env 中（参考 .env.example）
    add_argument('--zotero_id', type=str, default=None, help='Zotero user ID (env: ZOTERO_ID)')
    add_argument('--zotero_key', type=str, default=None, help='Zotero API key (env: ZOTERO_KEY)')
    add_argument('--zotero_ignore', type=str, default=None, help='Zotero collection to ignore, gitignore-style (env: ZOTERO_IGNORE)')
    add_argument('--send_empty', type=bool, default=False, help='If no arxiv paper, send empty email (env: SEND_EMPTY)')
    add_argument('--max_paper_num', type=int, default=15, help='Max papers to recommend (env: MAX_PAPER_NUM)')
    add_argument('--arxiv_query', type=str, default='cs.AI+cs.LG+cs.CL+cs.IR', help='Arxiv search query (env: ARXIV_QUERY)')
    add_argument('--smtp_server', type=str, default='smtp.qq.com', help='SMTP server (env: SMTP_SERVER)')
    add_argument('--smtp_port', type=int, default=465, help='SMTP port (env: SMTP_PORT)')
    add_argument('--sender', type=str, default=None, help='Sender email (env: SENDER)')
    add_argument('--receiver', type=str, default=None, help='Receiver email (env: RECEIVER)')
    add_argument('--sender_password', type=str, default=None, help='Sender SMTP password (env: SENDER_PASSWORD)')
    add_argument('--use_llm_api', type=bool, default=True, help='Use OpenAI API for TLDR (env: USE_LLM_API)')
    add_argument('--openai_api_key', type=str, default=None, help='OpenAI API key (env: OPENAI_API_KEY)')
    add_argument('--openai_api_base', type=str, default='https://api.openai.com/v1', help='OpenAI API base URL (env: OPENAI_API_BASE)')
    add_argument('--model_name', type=str, default='gpt-4o-mini', help='LLM model name (env: MODEL_NAME)')
    add_argument('--language', type=str, default='Chinese', help='TLDR language (env: LANGUAGE)')
    add_argument('--wechat_appid', type=str, default=None, help='WeChat AppID (env: WECHAT_APPID)')
    add_argument('--wechat_secret', type=str, default=None, help='WeChat AppSecret (env: WECHAT_SECRET)')
    add_argument('--wechat_author', type=str, default='AI Paper Daily', help='WeChat article author (env: WECHAT_AUTHOR)')
    add_argument('--enable_wechat', type=bool, default=True, help='Enable WeChat push (env: ENABLE_WECHAT)')
    add_argument('--enable_email', type=bool, default=True, help='Enable email push (env: ENABLE_EMAIL)')
    add_argument('--enable_feishu', type=bool, default=True, help='Enable Feishu push (env: ENABLE_FEISHU)')
    parser.add_argument('--debug', default=False, action='store_true', help='Debug mode')
    args = parser.parse_args()

    # 启动时校验：必要配置缺失时提示从 .env 配置
    if not args.zotero_id or not args.zotero_key:
        logger.error("ZOTERO_ID 和 ZOTERO_KEY 未设置，请在 .env 中配置（可参考 .env.example）")
        sys.exit(1)
    if args.enable_email and (not args.sender or not args.receiver or not args.sender_password):
        logger.error("启用邮件推送需在 .env 中配置 SENDER、RECEIVER、SENDER_PASSWORD")
        sys.exit(1)
    assert (
        not args.use_llm_api or args.openai_api_key is not None
    ), "USE_LLM_API=true 时请在 .env 中配置 OPENAI_API_KEY"
    if args.debug:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
        logger.debug("Debug mode is on.")
    else:
        logger.remove()
        logger.add(sys.stdout, level="INFO")


    # ================1. 检索Zotero文献库=================
    logger.info("检索Zotero文献库...")
    corpus = get_zotero_corpus(args.zotero_id, args.zotero_key)
    logger.info(f"Retrieved {len(corpus)} papers from Zotero.")
    if args.zotero_ignore:
        logger.info(f"Ignoring papers in:\n {args.zotero_ignore}...")
        corpus = filter_corpus(corpus, args.zotero_ignore)
        logger.info(f"Remaining {len(corpus)} papers after filtering.")
    

    # ================2. 检索Arxiv论文=================
    logger.info("检索Arxiv论文...")
    papers = get_arxiv_paper(args.arxiv_query, args.debug)
    if len(papers) == 0:
        logger.info("No new papers found. Yesterday maybe a holiday and no one submit their work :). If this is not the case, please check the ARXIV_QUERY.")
        if not args.send_empty:
          exit(0)
    else:
        # ================3. 对论文进行重新排序=================
        logger.info("对论文进行重新排序...")
        papers = rerank_paper(papers, corpus)
        if args.max_paper_num != -1:
            papers = papers[:args.max_paper_num]
        if args.use_llm_api:
            logger.info("Using OpenAI API as global LLM.")
            set_global_llm(api_key=args.openai_api_key, base_url=args.openai_api_base, model=args.model_name, lang=args.language)
        else:
            logger.info("Using Local LLM as global LLM.")
            set_global_llm(lang=args.language)

    # ================Web 信息推送=================
    # 将每日推荐论文写入 JSON，供前端「每日 ArXiv 推荐」展示（路径相对于项目根）
    RECOMMENDATIONS_DIR = os.path.join(_ROOT_DIR, "public", "recommendations")
    if len(papers) > 0:
        os.makedirs(RECOMMENDATIONS_DIR, exist_ok=True)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        payload = {
            "date": date_str,
            "count": len(papers),
            "papers": [p.to_web_dict() for p in papers],
        }
        import json
        latest_path = os.path.join(RECOMMENDATIONS_DIR, "latest.json")
        dated_path = os.path.join(RECOMMENDATIONS_DIR, f"papers_{date_str}.json")
        for path in (latest_path, dated_path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        logger.success(f"推荐论文已写入 {latest_path} 与 {dated_path}，共 {len(papers)} 篇。")
    else:
        logger.info("无推荐论文，跳过 Web 数据写入。")

    # ================3. Email推送=================
    if args.enable_email:
        logger.info("Rendering email...")
        html = render_email(papers)
        logger.info("Sending email...")
        send_email(args.sender, args.receiver, args.sender_password, args.smtp_server, args.smtp_port, html)
        logger.success("Email sent successfully! If you don't receive the email, please check the configuration and the junk box.")
    
    # ================4. 微信公众号推送=================
    if args.enable_wechat:
        if WechatClient is None:
            logger.warning("WeChat push enabled but wechat_publisher not installed. Skipping WeChat push.")
        elif not args.wechat_appid or not args.wechat_secret:
            logger.error("WeChat push enabled but credentials not provided. Skipping WeChat push.")
        else:
            try:
                # 初始化微信客户端
                client = WechatClient(args.wechat_appid, args.wechat_secret)
                
                # 提取并上传论文图片
                logger.info("Extracting and uploading methodology images...")
                image_urls = {}
                temp_image_files = []  # 跟踪临时文件，用于后续清理
                
                try:
                    for paper in tqdm(papers, desc='Processing images'):
                        try:
                            # 提取图片
                            image_path = paper.methodology_image
                            if image_path is None:
                                logger.debug(f"No methodology image found for {paper.arxiv_id}")
                                continue
                            
                            temp_image_files.append(image_path)  # 记录临时文件
                            
                            # 上传图片到微信公众号
                            try:
                                image_url = client.upload_content_image(image_path)
                                image_urls[paper.arxiv_id] = image_url
                                logger.success(f"Image uploaded for {paper.arxiv_id}")
                            except Exception as e:
                                logger.warning(f"Failed to upload image for {paper.arxiv_id}: {e}")
                                # 继续处理其他论文，不中断流程
                                continue
                                
                        except Exception as e:
                            logger.warning(f"Failed to extract image for {paper.arxiv_id}: {e}")
                            # 继续处理其他论文，不中断流程
                            continue
                    
                    logger.info(f"Successfully processed {len(image_urls)} images out of {len(papers)} papers")
                    
                    # 渲染 WeChat 内容（包含图片）
                    logger.info("Rendering WeChat article...")
                    wechat_content = render_wechat(papers, image_urls=image_urls)
                    
                    # 创建草稿
                    logger.info("Creating WeChat draft...")
                    result = client.create_draft(
                        title=f"arXiv 每日推荐 {datetime.datetime.now().strftime('%Y/%m/%d')}",
                        content=wechat_content,
                        author=args.wechat_author
                    )
                    logger.success(f"WeChat draft created successfully! Draft ID: {result.get('media_id')}")
                    
                finally:
                    # 清理临时图片文件（无论成功或失败都要清理）
                    for temp_file in temp_image_files:
                        try:
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                                logger.debug(f"Cleaned up temporary image file: {temp_file}")
                        except Exception as e:
                            logger.debug(f"Failed to clean up {temp_file}: {e}")
                
            except Exception as e:
                logger.error(f"Failed to create WeChat draft: {e}")
                logger.warning("WeChat push failed, but the workflow will continue.")
    
    # ================4. 飞书通知推送=================
    if args.enable_feishu:
        try:
            logger.info("Rendering Feishu message...")
            feishu_content = render_feishu(papers)
            logger.success(f"Feishu message rendered! Length: {len(feishu_content)} chars")
            logger.info("请使用 nanobot 的 message 工具发送飞书消息")
            # 将消息保存到项目根目录，供定时任务调用
            feishu_path = os.path.join(_ROOT_DIR, "feishu_message.txt")
            with open(feishu_path, 'w', encoding='utf-8') as f:
                f.write(feishu_content)
            logger.success(f"飞书消息已保存到 {feishu_path}")
        except Exception as e:
            logger.error(f"Failed to render Feishu message: {e}")
