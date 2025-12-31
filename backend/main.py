"""
TreeHole API主程序
内存模式，无数据库依赖

这是一个匿名留言板API服务,提供留言的创建、查询、点赞和点踩功能。
当前版本使用内存存储,数据在服务重启后会丢失。

主要功能:
- 创建新留言(最多140字符)
- 获取留言列表(支持分页)
- 获取单条留言详情
- 点赞/点踩留言

技术栈:
- FastAPI: 高性能Web框架
- 内存存储: 使用List存储留言数据
- 线程锁: 使用threading.Lock保证并发安全
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from config import API_CONFIG, CORS_CONFIG, ERROR_MESSAGES
from logger import setupLogger, logInfo
from fastapi.responses import JSONResponse
from datetime import datetime
from threading import Lock
from fastapi.encoders import jsonable_encoder
import schemas

# ==================== 应用初始化 ====================

# 设置日志记录器
logger = setupLogger("main")

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

# ==================== 数据存储 ====================

# 内存留言存储
# 使用列表存储所有留言对象
# 注意: 服务重启后数据会丢失
messages_store = []

# 线程锁,用于保证并发访问messages_store时的线程安全
# 防止多个请求同时修改数据导致竞态条件
store_lock = Lock()

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
    根路径接口

    用于测试API服务是否正常运行

    Returns:
        JSONResponse: 包含欢迎消息的响应

    Example:
        GET /
        Response: {"code": 0, "message": "success", "data": {"welcome": "欢迎来到树洞 API！"}}
    """
    logInfo(logger, "访问根路径")
    return api_response({"welcome": "欢迎来到树洞 API！"})

@app.get("/ping", tags=["基础"])
def health_check():
    """
    健康检查接口

    用于负载均衡器或监控系统检查服务健康状态

    Returns:
        JSONResponse: 包含服务状态的响应

    Example:
        GET /ping
        Response: {"code": 0, "message": "success", "data": {"status": "ok"}}
    """
    return api_response({"status": "ok"})

@app.post("/messages/", response_model=schemas.Message, tags=["留言"])
def createMessage(message: schemas.MessageCreate):
    """
    创建新留言

    接收用户提交的留言内容并保存到内存存储中

    Args:
        message (MessageCreate): 包含留言内容的请求体

    Returns:
        JSONResponse: 包含新创建留言对象的响应

    Raises:
        HTTPException: 当留言内容验证失败时

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
                "parent_id": null
            }
        }
    """
    with store_lock:
        # 自动生成新留言ID: 如果已有留言则使用最后一条ID+1,否则从1开始
        # 注意: 服务重启后ID会重新从1开始
        new_id = (messages_store[-1].id + 1) if messages_store else 1

        # 创建留言对象
        msg = schemas.Message(
            id=new_id,
            content=message.content,
            parent_id=None,  # 当前版本不支持回复功能
            timestamp=datetime.utcnow(),  # 使用UTC时间戳
            like_count=0,
            dislike_count=0
        )

        # 将留言添加到内存存储
        messages_store.append(msg)

    return api_response(msg.dict())

@app.get("/messages/", response_model=List[schemas.Message], tags=["留言"])
def readMessages(skip: int = 0, limit: int = 20):
    """
    获取留言列表

    支持分页查询留言列表,按时间倒序排列(最新的在前)

    Args:
        skip (int): 跳过的留言数量,用于分页。默认为0
        limit (int): 返回的留言数量上限。默认为20,最大100

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
                    "dislike_count": 1
                },
                ...
            ]
        }
    """
    with store_lock:
        # 使用切片实现分页: messages_store[skip:skip+limit]
        # 列表已在创建时按时间倒序排列(ID越大越新)
        data = [m.dict() for m in messages_store[skip:skip+limit]]
    return api_response(data)

@app.get("/messages/{messageId}", response_model=schemas.Message, tags=["留言"])
def readMessage(messageId: int):
    """
    获取单条留言详情

    根据留言ID获取完整的留言信息

    Args:
        messageId (int): 留言的唯一标识符

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
                "dislike_count": 2
            }
        }
    """
    with store_lock:
        # 遍历内存存储查找指定ID的留言
        # TODO: 当留言数量很大时,应考虑使用字典(dict)提高查找效率
        for m in messages_store:
            if m.id == messageId:
                return api_response(m.dict())

    # 未找到留言,返回404错误
    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

@app.post("/messages/{messageId}/like", response_model=schemas.Message, tags=["留言"])
def likeMessage(messageId: int):
    """
    给留言点赞

    增加指定留言的点赞计数

    Args:
        messageId (int): 要点赞的留言ID

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
    with store_lock:
        for m in messages_store:
            if m.id == messageId:
                # 增加点赞计数
                m.like_count += 1
                return api_response(m.dict())

    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

@app.post("/messages/{messageId}/dislike", response_model=schemas.Message, tags=["留言"])
def dislikeMessage(messageId: int):
    """
    给留言点踩

    增加指定留言的点踩计数

    Args:
        messageId (int): 要点踩的留言ID

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
    with store_lock:
        for m in messages_store:
            if m.id == messageId:
                # 增加点踩计数
                m.dislike_count += 1
                return api_response(m.dict())

    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

# ==================== 应用启动 ====================

if __name__ == "__main__":
    import uvicorn
    logInfo(logger, "启动TreeHole API服务器")
    # 启动开发服务器
    # host: 监听所有网络接口(0.0.0.0),可从外部访问
    # port: 监听端口8000
    # reload: 开启热重载,代码修改后自动重启服务
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
