"""
pytest配置文件
定义测试夹具(Fixtures)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, getDatabase

# ==================== 测试数据库配置 ====================

# 使用内存数据库进行测试
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ==================== Fixtures ====================

@pytest.fixture(scope="function")
def db():
    """
    创建测试数据库会话

    每个测试函数都会使用一个新的数据库
    测试结束后自动回滚,保持测试隔离
    """
    # 创建测试表
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # 清理:删除所有表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    创建测试客户端

    使用测试数据库覆盖依赖
    """
    def overrideGetDatabase():
        try:
            yield db
        finally:
            pass

    # 覆盖数据库依赖
    app.dependency_overrides[getDatabase] = overrideGetDatabase

    # 创建测试客户端
    testClient = TestClient(app)

    try:
        yield testClient
    finally:
        # 清理依赖覆盖
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def clean_db(db):
    """
    清空数据库的fixture
    用于需要空数据库的测试
    """
    # 在测试前清空所有表
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

    yield db
