from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime
from config import MESSAGE_CONFIG, ERROR_MESSAGES

class MessageBase(BaseModel):
    """
    留言基础模型
    
    Attributes:
        content (str): 留言内容
        parent_id (Optional[int]): 父留言ID，用于回复功能
    """
    content: str
    parent_id: Optional[int] = None

    @validator('content')
    def validateContent(cls, value):
        """
        验证留言内容
        
        Args:
            value (str): 留言内容
            
        Returns:
            str: 验证通过的内容
            
        Raises:
            ValueError: 当内容为空或超过长度限制时
        """
        if not value or not value.strip():
            raise ValueError("留言内容不能为空")
        
        if len(value) > MESSAGE_CONFIG["max_content_length"]:
            raise ValueError(ERROR_MESSAGES["content_too_long"])
        
        return value.strip()

class MessageCreate(MessageBase):
    """
    创建留言的请求模型
    继承自MessageBase，用于API请求验证
    """
    pass

class Message(MessageBase):
    """
    留言响应模型
    
    Attributes:
        id (int): 留言唯一标识符
        timestamp (datetime): 留言创建时间
        like_count (int): 点赞数量
        dislike_count (int): 踩数量
    """
    id: int
    timestamp: datetime
    like_count: int
    dislike_count: int

    class Config:
        orm_mode = True
