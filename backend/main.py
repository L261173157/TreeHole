"""
TreeHole API主程序

这是一个匿名留言板API服务,提供留言的创建、查询、点赞和点踩功能。

主要功能:
- 创建新留言(最多140字符)
- 获取留言列表(支持分页)
- 获取单条留言详情
- 点赞/点踩留言
- 回复留言

技术栈:
- FastAPI: 高性能Web框架
- SQLAlchemy: ORM框架
- SQLite: 数据库
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from config import API_CONFIG, CORS_CONFIG, ERROR_MESSAGES
from logger import setupLogger, logInfo
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schemas
import crud
from database import engine, getDatabase, createTables
import models
from utils import sanitize_html

# ==================== 应用初始化 ====================

# 设置日志记录器
logger = setupLogger("main")

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用实例
# title: API文档标题
# description: API文档描述
# version: API版本号
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"]
)

# ==================== CORS配置 ====================

# 配置CORS中间件
# 使用config.py中的配置,可以通过环境变量CORS_ORIGINS设置允许的源
# 开发环境示例: CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
# 生产环境: CORS_ORIGINS=https://yourdomain.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],  # 从环境变量或配置文件读取
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"],   # 允许所有请求头
)

# ==================== 数据库依赖 ====================

from database import SessionLocal

# 数据库依赖注入函数
def getDb():
    """
    获取数据库会话的依赖注入函数

    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== 工具函数 ====================

def api_response(data=None, code=0, message="success"):
    """
    统一API响应格式

    所有API接口都使用此函数生成统一格式的响应

    Args:
        data: 响应数据,可以是任意类型
        code (int): 响应状态码,0表示成功,非0表示失败
        message (str): 响应消息,描述操作结果

    Returns:
        JSONResponse: JSON格式的响应对象

    Response Format:
        {
            "code": 0,
            "message": "success",
            "data": {...}
        }
    """
    return JSONResponse(content={"code": code, "message": message, "data": jsonable_encoder(data)})

# ==================== API路由 ====================

@app.get("/", tags=["基础"])
def readRoot():
    """
    API根路径

    返回API的基本信息

    Returns:
        dict: 包含API名称、版本和描述的字典
    """
    return {
        "name": API_CONFIG["title"],
        "version": API_CONFIG["version"],
        "description": API_CONFIG["description"]
    }

@app.get("/ping", tags=["基础"])
def ping():
    """
    健康检查接口

    用于检查服务是否正常运行

    Returns:
        dict: 包含状态信息的字典
    """
    return {"status": "ok", "message": "服务正常运行"}

@app.get("/messages/", tags=["留言"])
def readMessages(
    skip: int = 0,
    limit: Optional[int] = None,
    db: Session = Depends(getDb)
):
    """
    获取留言列表

    获取所有留言,支持分页功能

    Args:
        skip (int): 跳过的留言数量,用于分页,默认为0
        limit (Optional[int]): 返回的留言数量限制,默认使用配置文件中的值
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含留言列表的响应

    Example:
        GET /messages/?skip=0&limit=10
        Response: {
            "code": 0,
            "message": "success",
            "data": [
                {
                    "id": 2,
                    "content": "第二条留言",
                    "timestamp": "2025-12-30T11:00:00",
                    "like_count": 5,
                    "dislike_count": 1,
                    "reply_count": 0
                },
                ...
            ]
        }
    """
    messages = crud.getMessages(db, skip=skip, limit=limit)
    return api_response(messages)

@app.get("/messages/{messageId}", response_model=schemas.Message, tags=["留言"])
def readMessage(messageId: int, db: Session = Depends(getDb)):
    """
    获取单条留言详情

    根据留言ID获取完整的留言信息

    Args:
        messageId (int): 留言的唯一标识符
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含留言详情的响应

    Raises:
        HTTPException: 当留言不存在时返回404错误

    Example:
        GET /messages/1
        Response: {
            "code": 0,
            "message": "success",
            "data": {
                "id": 1,
                "content": "这是我的第一条留言",
                "timestamp": "2025-12-30T10:30:00",
                "like_count": 10,
                "dislike_count": 2,
                "reply_count": 0
            }
        }
    """
    message = crud.getMessage(db, messageId)
    if not message:
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])
    return api_response(message)

@app.get("/messages/{messageId}/replies", tags=["留言"])
def readReplies(messageId: int, db: Session = Depends(getDb)):
    """
    获取留言的所有回复

    根据父留言ID获取所有回复

    Args:
        messageId (int): 父留言的唯一标识符
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含回复列表的响应

    Example:
        GET /messages/1/replies
        Response: {
            "code": 0,
            "message": "success",
            "data": [
                {
                    "id": 2,
                    "content": "这是回复内容",
                    "timestamp": "2025-12-30T11:00:00",
                    "like_count": 0,
                    "dislike_count": 0,
                    "reply_count": 0,
                    "parent_id": 1
                },
                ...
            ]
        }
    """
    # 先检查父留言是否存在
    parent = crud.getMessage(db, messageId)
    if not parent:
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

    replies = crud.getReplies(db, messageId)
    return api_response(replies)

@app.post("/messages/", response_model=schemas.Message, tags=["留言"])
def createMessage(message: schemas.MessageCreate, db: Session = Depends(getDb)):
    """
    创建新留言或回复

    创建一条新的匿名留言,内容不能超过140个字符
    如果提供parent_id,则创建回复

    Args:
        message (MessageCreate): 留言创建请求,包含content和parent_id字段
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含新创建留言信息的响应

    Raises:
        HTTPException: 当内容验证失败时返回400错误

    Example:
        POST /messages/
        Body: {"content": "这是我的第一条留言"}
        Response: {
            "code": 0,
            "message": "success",
            "data": {
                "id": 1,
                "content": "这是我的第一条留言",
                "timestamp": "2025-12-30T10:30:00",
                "like_count": 0,
                "dislike_count": 0,
                "reply_count": 0,
                "parent_id": null
            }
        }
    """
    try:
        # XSS防护: 过滤用户输入中的HTML标签
        message.content = sanitize_html(message.content)

        dbMessage = crud.createMessage(db, message)
        if not dbMessage:
            raise HTTPException(status_code=400, detail="创建留言失败")
        return api_response(dbMessage)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/messages/{messageId}/like", response_model=schemas.Message, tags=["留言"])
def likeMessage(messageId: int, db: Session = Depends(getDb)):
    """
    给留言点赞

    增加指定留言的点赞计数

    Args:
        messageId (int): 要点赞的留言ID
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含更新后留言信息的响应

    Raises:
        HTTPException: 当留言不存在时返回404错误

    Example:
        POST /messages/1/like
        Response: {
            "code": 0,
            "message": "success",
            "data": {
                "id": 1,
                "like_count": 11,  # 点赞数+1
                "dislike_count": 2,
                ...
            }
        }

    Note:
        - 当前版本没有限制点赞次数,同一用户可以多次点赞
        - 建议生产环境添加IP限制或用户认证来防止刷票
    """
    message = crud.likeMessage(db, messageId)
    if not message:
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])
    return api_response(message)

@app.post("/messages/{messageId}/dislike", response_model=schemas.Message, tags=["留言"])
def dislikeMessage(messageId: int, db: Session = Depends(getDb)):
    """
    给留言点踩

    增加指定留言的点踩计数

    Args:
        messageId (int): 要点踩的留言ID
        db (Session): 数据库会话

    Returns:
        JSONResponse: 包含更新后留言信息的响应

    Raises:
        HTTPException: 当留言不存在时返回404错误

    Example:
        POST /messages/1/dislike
        Response: {
            "code": 0,
            "message": "success",
            "data": {
                "id": 1,
                "like_count": 11,
                "dislike_count": 3,  # 点踩数+1
                ...
            }
        }

    Note:
        - 当前版本没有限制点踩次数,同一用户可以多次点踩
        - 建议生产环境添加IP限制或用户认证来防止刷票
    """
    message = crud.dislikeMessage(db, messageId)
    if not message:
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])
    return api_response(message)

# ==================== 应用启动 ====================

if __name__ == "__main__":
    import uvicorn
    logInfo(logger, "启动TreeHole API服务器")
    # 启动开发服务器
    # host: 监听所有网络接口(0.0.0.0),可从外部访问
    # port: 监听端口8000
    # reload: 开启热重载,代码修改后自动重启服务
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
