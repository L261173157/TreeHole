"""
TreeHole项目配置文件
包含所有常量和配置项

支持环境变量配置,如果未设置环境变量则使用默认值
"""

import os
from typing import List

# ==================== 环境变量读取辅助函数 ====================

def getEnv(key: str, default: str = "") -> str:
    """
    读取环境变量,如果不存在则返回默认值

    Args:
        key (str): 环境变量名称
        default (str): 默认值

    Returns:
        str: 环境变量的值或默认值
    """
    return os.getenv(key, default)

def getEnvInt(key: str, default: int = 0) -> int:
    """
    读取整数类型的环境变量

    Args:
        key (str): 环境变量名称
        default (int): 默认值

    Returns:
        int: 环境变量的值或默认值
    """
    value = os.getenv(key)
    return int(value) if value and value.isdigit() else default

def getEnvBool(key: str, default: bool = False) -> bool:
    """
    读取布尔类型的环境变量

    Args:
        key (str): 环境变量名称
        default (bool): 默认值

    Returns:
        bool: 环境变量的值或默认值
    """
    value = os.getenv(key, "").lower()
    return value in ("true", "1", "yes") if value else default

# ==================== 数据库配置 ====================

DATABASE_CONFIG = {
    "url": getEnv("DATABASE_URL", "sqlite:///./treehole.db"),
    "connect_args": {"check_same_thread": False}
}

# ==================== 留言相关配置 ====================

MESSAGE_CONFIG = {
    "max_content_length": getEnvInt("MAX_CONTENT_LENGTH", 140),  # 留言最大字符数
    "default_page_size": getEnvInt("DEFAULT_PAGE_SIZE", 20),     # 默认分页大小
    "max_page_size": getEnvInt("MAX_PAGE_SIZE", 100)             # 最大分页大小
}

# ==================== CORS配置 ====================

# 从环境变量读取允许的源,多个源用逗号分隔
def parseCorsOrigins(originsStr: str) -> List[str]:
    """
    解析CORS允许的源列表

    Args:
        originsStr (str): 逗号分隔的源字符串

    Returns:
        List[str]: 源列表
    """
    if not originsStr or originsStr.strip() == "*":
        return ["*"]  # 开发环境允许所有源
    return [origin.strip() for origin in originsStr.split(",") if origin.strip()]

CORS_CONFIG = {
    "allow_origins": parseCorsOrigins(getEnv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")),
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "OPTIONS"],  # 限制HTTP方法
    "allow_headers": ["Content-Type"]  # 限制请求头
}

# API配置
API_CONFIG = {
    "title": "TreeHole API",
    "description": "树洞留言板API接口",
    "version": "1.0.0"
}

# 错误消息
ERROR_MESSAGES = {
    "content_too_long": f"内容不能超过{MESSAGE_CONFIG['max_content_length']}字",
    "message_not_found": "留言不存在",
    "invalid_input": "输入数据无效",
    "database_error": "数据库操作失败"
}

# 成功消息
SUCCESS_MESSAGES = {
    "message_created": "留言创建成功",
    "message_liked": "点赞成功",
    "message_disliked": "踩成功"
}
