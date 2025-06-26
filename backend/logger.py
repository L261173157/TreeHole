"""
日志系统配置
"""

import logging
import sys
from datetime import datetime

def setupLogger(name: str = "treehole") -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name (str): 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # 创建控制台处理器
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.INFO)
    
    # 创建文件处理器
    fileHandler = logging.FileHandler(
        f"logs/treehole_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    fileHandler.setLevel(logging.INFO)
    
    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    
    return logger

def logError(logger: logging.Logger, error: Exception, context: str = ""):
    """
    记录错误日志
    
    Args:
        logger (logging.Logger): 日志记录器
        error (Exception): 异常对象
        context (str): 错误上下文信息
    """
    errorMessage = f"{context}: {str(error)}" if context else str(error)
    logger.error(errorMessage, exc_info=True)

def logInfo(logger: logging.Logger, message: str):
    """
    记录信息日志
    
    Args:
        logger (logging.Logger): 日志记录器
        message (str): 日志消息
    """
    logger.info(message)
