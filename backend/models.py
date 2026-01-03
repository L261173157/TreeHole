from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from config import MESSAGE_CONFIG
import datetime

class Message(Base):
    """
    留言数据模型

    Attributes:
        id (int): 留言唯一标识符
        content (str): 留言内容，最大长度由配置文件定义
        timestamp (datetime): 留言创建时间
        like_count (int): 点赞数量
        dislike_count (int): 踩数量
        reply_count (int): 回复数量
        parent_id (int): 父留言ID，用于回复功能
        ip_address (str): 留言者IP地址
        location (str): IP地理位置
        replies (List[Message]): 回复列表
        parent (Message): 父留言对象
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(MESSAGE_CONFIG["max_content_length"]), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey('messages.id'), nullable=True)
    ip_address = Column(String(45), nullable=True)  # 支持IPv6
    location = Column(String(100), nullable=True)  # 存储地理位置，如 "北京市"
    replies = relationship("Message", backref="parent", remote_side=[id])
