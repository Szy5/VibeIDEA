from typing import Optional
from loguru import logger
from .paper import ArxivPaper


def render_feishu(papers: list[ArxivPaper], max_papers: int = 10) -> str:
    """
    构建飞书消息内容
    
    Args:
        papers: 论文列表
        max_papers: 最大展示论文数
        
    Returns:
        str: 飞书消息文本
    """
    if len(papers) == 0:
        return "今日暂无推荐论文 📭"
    
    # 限制展示数量
    display_papers = papers[:max_papers]
    
    # 构建消息头
    from datetime import datetime
    date_str = datetime.now().strftime('%Y/%m/%d')
    message_lines = [
        f"📚 **arXiv 每日推荐 - {date_str}**",
        f"",
        f"共推荐 **{len(papers)}** 篇论文，以下是精选 Top {len(display_papers)}：",
        ""
    ]
    
    # 构建每篇论文的信息
    for idx, paper in enumerate(display_papers, 1):
        # 标题
        title = paper.title.strip().replace('\n', ' ')
        
        # ArXiv ID 和链接
        arxiv_id = paper.arxiv_id
        pdf_url = paper.pdf_url
        
        # 作者（显示前3个）
        authors_list = paper.authors
        # 处理作者可能是对象或字符串的情况
        if authors_list and hasattr(authors_list[0], 'name'):
            authors = [a.name for a in authors_list[:3]]
        else:
            authors = list(authors_list[:3])
        authors_str = ', '.join(authors)
        if len(paper.authors) > 3:
            authors_str += f' 等{len(paper.authors)}位作者'
        
        # TLDR 一句话总结
        tldr = paper.tldr.strip() if paper.tldr else paper.summary[:200].strip()
        # 截断过长的 tldr
        if len(tldr) > 150:
            tldr = tldr[:147] + '...'
        
        # 代码链接
        code_info = ""
        if paper.code_url:
            code_info = f" | [代码]({paper.code_url})"
        
        # 构建论文块
        paper_block = [
            f"**{idx}. {title}**",
            f"📎 [{arxiv_id}]({pdf_url}){code_info}",
            f"👤 {authors_str}",
            f"💡 {tldr}",
            ""
        ]
        
        message_lines.extend(paper_block)
    
    # 添加底部信息
    message_lines.extend([
        "---",
        f"📌 共 {len(papers)} 篇论文，完整列表请查看微信订阅号或邮箱"
    ])
    
    return '\n'.join(message_lines)


def send_feishu_message(message: str, chat_id: str = None) -> bool:
    """
    发送飞书消息（通过 nanobot 的 message 工具）
    
    注意：这个函数需要外部调用 nanobot 的 message 工具来发送
    这里只返回消息内容，供外部使用
    
    Args:
        message: 消息内容
        chat_id: 聊天 ID（可选）
        
    Returns:
        bool: 返回 True，消息由调用方发送
    """
    logger.info(f"飞书消息已准备好，长度: {len(message)} 字符")
    return True
