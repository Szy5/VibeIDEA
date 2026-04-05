"""
微信公众号排版渲染模块
提供学术正式风格的微信公众号图文消息渲染

注意：微信公众号草稿箱 API 要求：
1. content 字段只能使用内联样式（inline styles），不能使用 <style> 标签
2. 不能使用复杂的 CSS（如 position, flexbox 等）
3. 只返回 body 内容，不需要完整的 HTML 文档结构

参考 baoyu-post-to-wechat skill 的排版风格，采用简洁紧凑的格式
"""

from paper import ArxivPaper
import math
from tqdm import tqdm
import datetime
from loguru import logger
from typing import Optional, Dict


def get_relevance_text(score: float) -> tuple[str, str]:
    """
    根据相关度分数返回文字描述和对应的内联样式
    
    Args:
        score: 相关度分数
        
    Returns:
        tuple: (描述文字, 内联样式字符串)
    """
    low = 6
    high = 8
    
    if score <= low:
        return "一般相关", "color: #5bc0de;"
    elif score >= high:
        return "高度相关 ⭐⭐⭐", "color: #d9534f; font-weight: bold;"
    else:
        # 中等相关度，显示1-2颗星
        star_count = 1 if score < (low + high) / 2 else 2
        stars = "⭐" * star_count
        return f"中度相关 {stars}", "color: #f0ad4e; font-weight: bold;"


def get_paper_block(paper: ArxivPaper, index: int, image_url: Optional[str] = None) -> str:
    """
    渲染单篇论文的 HTML 块（简洁紧凑格式，参考微信公众号最佳实践）
    
    采用简洁的段落格式，避免复杂的 div 嵌套和过大的间距
    
    Args:
        paper: 论文对象
        index: 论文序号（从1开始）
        image_url: 方法图 URL（可选），如果提供则在 TLDR 之后显示
        
    Returns:
        str: 论文 HTML 块
    """
    # 处理作者信息
    authors = [a.name for a in paper.authors[:5]]
    authors_str = ', '.join(authors)
    if len(paper.authors) > 5:
        authors_str += ', et al.'
    
    # 处理单位信息
    if paper.affiliations is not None:
        affiliations = paper.affiliations[:5]
        affiliations_str = ', '.join(affiliations)
        if len(paper.affiliations) > 5:
            affiliations_str += ', ...'
    else:
        affiliations_str = 'Affiliation not available'
    
    # 获取相关度描述和样式
    relevance_text, relevance_style = get_relevance_text(paper.score)
    
    # arXiv 链接（微信公众号不支持外链，直接显示 URL）
    arxiv_url = f"https://arxiv.org/abs/{paper.arxiv_id}"
    
    # 确保 PDF URL 是完整的 URL
    pdf_url = paper.pdf_url
    if not pdf_url.startswith(('http://', 'https://')):
        pdf_url = f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"
    
    # Code URL（如果有）
    code_text = ''
    if paper.code_url:
        code_url = paper.code_url
        if not code_url.startswith(('http://', 'https://')):
            code_url = f"https://{code_url}" if not code_url.startswith('//') else f"https:{code_url}"
        code_text = f'<br/><strong style="color: #555555;">Code：</strong><span style="color: #5bc0de; word-break: break-all;">{code_url}</span>'
    
    # 图片 HTML（如果有）
    image_html = ''
    if image_url:
        image_html = f'<p style="margin: 12px 0; padding: 0; text-align: center;"><img src="{image_url}" style="max-width: 100%; height: auto; border-radius: 4px;" /></p>'
    
    # 构建 HTML（简洁紧凑格式，参考微信公众号排版最佳实践）
    # 使用段落和引用块，避免复杂的 div 嵌套
    # 注意：微信公众号不支持外链，所以直接显示 URL 文本
    html = f"""
<h3 style="margin: 0 0 8px 0; padding: 0; font-size: 17px; font-weight: bold; color: #1a1a1a; line-height: 1.5;">{paper.title} <span style="background-color: #4a90e2; color: #ffffff; padding: 2px 6px; border-radius: 2px; font-weight: bold; font-size: 12px; margin-left: 6px;">#{index}</span>
</h3>
<p style="margin: 0 0 4px 0; padding: 0; font-size: 14px; color: #595959; line-height: 1.6;">
{authors_str}</p>
<p style="margin: 0 0 8px 0; padding: 0; font-size: 13px; color: #3f3f3f; line-height: 1.6;">
<strong style="color: #555555;">相关度：</strong><span style="{relevance_style}">{relevance_text}</span> | <strong style="color: #555555;">arXiv：</strong><span style="color: #4a90e2; word-break: break-all;">{arxiv_url}</span></p>
<blockquote style="margin: 8px 0; padding: 10px 12px; border-left: 4px solid #4a90e2; background-color: #f5f5f5; border-radius: 0 4px 4px 0; font-size: 14px; color: #444444; line-height: 1.75;"><p style="margin: 0 0 4px 0; padding: 0; font-weight: bold; color: #4a90e2; font-size: 13px;">📝 核心要点</p><p style="margin: 0; padding: 0; line-height: 1.75;">{paper.tldr}</p></blockquote>
{image_html}
<p style="margin: 8px 0 16px 0; padding: 0; font-size: 13px; line-height: 1.6;"><strong style="color: #555555;">PDF：</strong><span style="color: #d9534f; word-break: break-all;">{pdf_url}</span>{code_text}
</p>

<hr style="margin: 16px 0; padding: 0; border: none; border-top: 1px solid #e0e0e0; height: 1px;" />
"""
    return html


def get_empty_content() -> str:
    """
    返回空内容提示（今日无新论文）
    
    Returns:
        str: 空内容 HTML
    """
    return """
<p style="text-align: center; padding: 40px 20px; color: #888888; font-size: 14px; line-height: 1.6;">
    <span style="font-size: 36px; display: block; margin-bottom: 12px;">📚</span>
    <strong style="font-size: 16px; display: block; margin-bottom: 8px;">今日无新论文</strong>
    休息一下，明天再来吧！
</p>
"""


def render_wechat(papers: list[ArxivPaper], image_urls: Optional[Dict[str, str]] = None) -> str:
    """
    渲染为微信公众号 HTML 格式（简洁紧凑风格）
    
    注意：返回的内容只包含 body 内的 HTML，不包含 <html>、<head>、<style> 等标签
    所有样式都使用内联样式（inline styles），符合微信公众号 API 要求
    
    参考微信公众号排版最佳实践：
    - 字号：正文14px，标题17-18px
    - 行间距：1.5-1.75倍
    - 段间距：紧凑，8-12px
    - 使用段落和引用块，避免复杂嵌套
    
    Args:
        papers: 论文列表
        image_urls: 论文图片 URL 字典，键为 arxiv_id，值为图片 URL
        
    Returns:
        str: HTML 内容（仅 body 内容，使用内联样式）
    """
    if image_urls is None:
        image_urls = {}
    # 生成日期
    today = datetime.datetime.now().strftime('%Y年%m月%d日')
    
    # 头部（简洁格式）
    header = f"""
<h1 style="text-align: center; margin: 0 0 6px 0; padding: 12px 0; border-bottom: 2px solid #e0e0e0; font-size: 18px; font-weight: bold; color: #1a1a1a; line-height: 1.5;">
    arXiv 每日论文推荐
</h1>

<p style="text-align: center; margin: 0 0 16px 0; padding: 0; font-size: 13px; color: #888888;">
    {today}
</p>
"""
    
    # 内容区
    if len(papers) == 0:
        logger.info("No papers to render for WeChat")
        content_blocks = [get_empty_content()]
    else:
        logger.info(f"Rendering {len(papers)} papers for WeChat...")
        content_blocks = []
        for i, paper in enumerate(tqdm(papers, desc='Rendering WeChat content'), start=1):
            # 获取该论文的图片 URL
            paper_image_url = image_urls.get(paper.arxiv_id)
            content_blocks.append(get_paper_block(paper, i, image_url=paper_image_url))
    
    content = '\n'.join(content_blocks)
    
    # 页脚（简洁格式）
    footer = f"""
<p style="text-align: center; margin: 16px 0 0 0; padding: 12px 0 8px 0; border-top: 1px solid #e0e0e0; font-size: 12px; color: #888888; line-height: 1.6;">
    共推荐 {len(papers)} 篇论文 · 基于 Zotero 文献库智能推荐<br>
    © arXiv Daily Recommender
</p>
"""
    body_content = f"""
<div style="max-width: 100%; padding: 12px 10px; background-color: #ffffff; font-family: -apple-system-font, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif; font-size: 14px; line-height: 1.75; color: #3f3f3f; letter-spacing: 0.3px;">
    {header}
    {content}
    {footer}
</div>
"""
    
    logger.success("WeChat content rendered successfully")
    return body_content.strip()
