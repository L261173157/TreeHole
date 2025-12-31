"""
输入验证和过滤工具
"""
import re
import html


def sanitize_html(content: str) -> str:
    """
    过滤用户输入中的HTML标签,防止XSS攻击

    Args:
        content (str): 用户输入的内容

    Returns:
        str: 过滤后的安全内容
    """
    if not content:
        return content

    # 方法1: 使用html.escape转义特殊字符
    # 这会将 <script> 变成 &lt;script&gt;
    sanitized = html.escape(content)

    # 方法2: 直接移除所有HTML标签
    # 使用正则表达式移除HTML标签
    # tag_pattern = re.compile(r'<[^>]+>')
    # sanitized = tag_pattern.sub('', content)

    return sanitized


def validate_content(content: str) -> tuple[bool, str]:
    """
    验证用户输入内容是否安全

    Args:
        content (str): 用户输入的内容

    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    if not content or not content.strip():
        return False, "内容不能为空"

    # 检查是否包含潜在的恶意脚本
    dangerous_patterns = [
        r'<script',  # script标签
        r'javascript:',  # javascript:协议
        r'on\w+\s*=',  # 事件处理器如 onclick=
        r'<iframe',  # iframe标签
        r'<object',  # object标签
        r'<embed',  # embed标签
    ]

    content_lower = content.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, content_lower):
            return False, "内容包含不允许的字符"

    return True, ""
