"""
TreeHole API主程序
内存模式，无数据库依赖
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

# 设置日志
logger = setupLogger("main")

# 创建FastAPI应用
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"]
)

# 配置CORS中间件（开发环境全放开）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存留言存储
messages_store = []
store_lock = Lock()

# 统一API响应结构
def api_response(data=None, code=0, message="success"):
    return JSONResponse(content={"code": code, "message": message, "data": jsonable_encoder(data)})

@app.get("/", tags=["基础"])
def readRoot():
    logInfo(logger, "访问根路径")
    return api_response({"welcome": "欢迎来到树洞 API！"})

@app.get("/ping", tags=["基础"])
def health_check():
    return api_response({"status": "ok"})

@app.post("/messages/", response_model=schemas.Message, tags=["留言"])
def createMessage(message: schemas.MessageCreate):
    with store_lock:
        new_id = (messages_store[-1].id + 1) if messages_store else 1
        msg = schemas.Message(
            id=new_id,
            content=message.content,
            parent_id=message.parent_id,
            timestamp=datetime.utcnow(),
            like_count=0,
            dislike_count=0,
            reply_count=0,
            replies=[]
        )
        messages_store.append(msg)
    return api_response(msg.dict())

@app.get("/messages/", response_model=List[schemas.Message], tags=["留言"])
def readMessages(skip: int = 0, limit: int = 20):
    with store_lock:
        data = [m.dict() for m in messages_store[skip:skip+limit]]
    return api_response(data)

@app.get("/messages/{messageId}", response_model=schemas.Message, tags=["留言"])
def readMessage(messageId: int):
    with store_lock:
        for m in messages_store:
            if m.id == messageId:
                return api_response(m.dict())
    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

@app.post("/messages/{messageId}/like", response_model=schemas.Message, tags=["留言"])
def likeMessage(messageId: int):
    with store_lock:
        for m in messages_store:
            if m.id == messageId:
                m.like_count += 1
                return api_response(m.dict())
    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

@app.post("/messages/{messageId}/dislike", response_model=schemas.Message, tags=["留言"])
def dislikeMessage(messageId: int):
    with store_lock:
        for m in messages_store:
            if m.id == messageId:
                m.dislike_count += 1
                return api_response(m.dict())
    raise HTTPException(status_code=404, detail=ERROR_MESSAGES["message_not_found"])

if __name__ == "__main__":
    import uvicorn
    logInfo(logger, "启动TreeHole API服务器")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
