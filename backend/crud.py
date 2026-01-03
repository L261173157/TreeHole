from sqlalchemy.orm import Session
import models
import schemas
from config import ERROR_MESSAGES, MESSAGE_CONFIG
from logger import setupLogger, logError, logInfo
from typing import List, Optional
import datetime

# 设置日志
logger = setupLogger("crud")

def getMessage(db: Session, messageId: int) -> Optional[models.Message]:
    """
    根据ID获取留言
    
    Args:
        db (Session): 数据库会话
        messageId (int): 留言ID
        
    Returns:
        Optional[Message]: 留言对象，如果不存在则返回None
    """
    try:
        message = db.query(models.Message).filter(models.Message.id == messageId).first()
        if message:
            logInfo(logger, f"成功获取留言 ID: {messageId}")
        return message
    except Exception as e:
        logError(logger, e, f"获取留言失败 ID: {messageId}")
        return None

def getMessages(db: Session, skip: int = 0, limit: Optional[int] = None) -> List[models.Message]:
    """
    获取留言列表
    
    Args:
        db (Session): 数据库会话
        skip (int): 跳过的记录数，默认为0
        limit (Optional[int]): 限制返回的记录数，默认使用配置文件中的值
        
    Returns:
        List[Message]: 留言列表
    """
    try:
        if limit is None:
            limit = MESSAGE_CONFIG["default_page_size"]
        
        # 限制最大页面大小
        if limit > MESSAGE_CONFIG["max_page_size"]:
            limit = MESSAGE_CONFIG["max_page_size"]
            
        messages = (db.query(models.Message)
                   .filter(models.Message.parent_id == None)
                   .order_by(models.Message.id.desc())
                   .offset(skip)
                   .limit(limit)
                   .all())
        
        logInfo(logger, f"成功获取 {len(messages)} 条留言")
        return messages
    except Exception as e:
        logError(logger, e, "获取留言列表失败")
        return []

def createMessage(db: Session, message: schemas.MessageCreate, ip_address: str = None, location: str = None) -> Optional[models.Message]:
    """
    创建新留言

    Args:
        db (Session): 数据库会话
        message (MessageCreate): 留言创建数据
        ip_address (str): 留言者IP地址
        location (str): IP地理位置

    Returns:
        Optional[Message]: 创建的留言对象，失败时返回None

    Raises:
        ValueError: 当内容超过字符限制时
    """
    try:
        # 验证内容长度
        if len(message.content) > MESSAGE_CONFIG["max_content_length"]:
            raise ValueError(ERROR_MESSAGES["content_too_long"])

        dbMessage = models.Message(
            content=message.content,
            parent_id=message.parent_id,
            timestamp=datetime.datetime.utcnow(),
            ip_address=ip_address,
            location=location
        )

        db.add(dbMessage)
        db.commit()
        db.refresh(dbMessage)

        # 如果是回复，更新父留言的回复数
        if message.parent_id:
            parent = getMessage(db, message.parent_id)
            if parent:
                setattr(parent, 'reply_count', (getattr(parent, 'reply_count', 0) or 0) + 1)
                db.commit()
                logInfo(logger, f"更新父留言 {message.parent_id} 的回复数")

        logInfo(logger, f"成功创建留言 ID: {dbMessage.id}, IP: {ip_address}, 位置: {location}")
        return dbMessage

    except ValueError:
        # 重新抛出验证错误
        raise
    except Exception as e:
        logError(logger, e, "创建留言失败")
        db.rollback()
        return None

def likeMessage(db: Session, messageId: int) -> Optional[models.Message]:
    """
    给留言点赞
    
    Args:
        db (Session): 数据库会话
        messageId (int): 留言ID
        
    Returns:
        Optional[Message]: 更新后的留言对象，失败时返回None
    """
    try:
        message = getMessage(db, messageId)
        if message:
            setattr(message, 'like_count', (getattr(message, 'like_count', 0) or 0) + 1)
            db.commit()
            db.refresh(message)
            logInfo(logger, f"留言 {messageId} 点赞成功，当前点赞数: {message.like_count}")
            return message
        else:
            logError(logger, Exception(ERROR_MESSAGES["message_not_found"]), f"点赞失败，留言不存在 ID: {messageId}")
            return None
    except Exception as e:
        logError(logger, e, f"点赞失败 ID: {messageId}")
        db.rollback()
        return None

def dislikeMessage(db: Session, messageId: int) -> Optional[models.Message]:
    """
    给留言踩

    Args:
        db (Session): 数据库会话
        messageId (int): 留言ID

    Returns:
        Optional[Message]: 更新后的留言对象，失败时返回None
    """
    try:
        message = getMessage(db, messageId)
        if message:
            setattr(message, 'dislike_count', (getattr(message, 'dislike_count', 0) or 0) + 1)
            db.commit()
            db.refresh(message)
            logInfo(logger, f"留言 {messageId} 踩成功，当前踩数: {message.dislike_count}")
            return message
        else:
            logError(logger, Exception(ERROR_MESSAGES["message_not_found"]), f"踩失败，留言不存在 ID: {messageId}")
            return None
    except Exception as e:
        logError(logger, e, f"踩失败 ID: {messageId}")
        db.rollback()
        return None

def getReplies(db: Session, parentId: int) -> List[models.Message]:
    """
    获取指定留言的所有回复

    Args:
        db (Session): 数据库会话
        parentId (int): 父留言ID

    Returns:
        List[Message]: 回复列表
    """
    try:
        replies = (db.query(models.Message)
                   .filter(models.Message.parent_id == parentId)
                   .order_by(models.Message.id.asc())
                   .all())

        logInfo(logger, f"成功获取留言 {parentId} 的 {len(replies)} 条回复")
        return replies
    except Exception as e:
        logError(logger, e, f"获取回复失败 父留言ID: {parentId}")
        return []
