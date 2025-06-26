from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_CONFIG
from logger import setupLogger, logInfo, logError
import os

# 设置日志
logger = setupLogger("database")

# 创建数据库引擎
engine = create_engine(
    DATABASE_CONFIG["url"], 
    connect_args=DATABASE_CONFIG["connect_args"]
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def createTables():
    """
    创建数据库表
    """
    try:
        # 确保logs目录存在
        os.makedirs("logs", exist_ok=True)
        
        Base.metadata.create_all(bind=engine)
        logInfo(logger, "数据库表创建成功")
    except Exception as e:
        logError(logger, e, "创建数据库表失败")
        raise

def getDatabase():
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logError(logger, e, "数据库会话错误")
        db.rollback()
        raise
    finally:
        db.close()
