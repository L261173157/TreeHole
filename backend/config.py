"""
TreeHole项目配置文件
包含所有常量和配置项
"""

# 数据库配置
DATABASE_CONFIG = {
    "url": "sqlite:///./treehole.db",
    "connect_args": {"check_same_thread": False}
}

# 留言相关配置
MESSAGE_CONFIG = {
    "max_content_length": 140,  # 留言最大字符数
    "default_page_size": 20,    # 默认分页大小
    "max_page_size": 100        # 最大分页大小
}

# CORS配置
CORS_CONFIG = {
    "allow_origins": ["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端开发服务器地址
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
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
