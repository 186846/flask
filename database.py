# 创建 MySQL 数据库连接
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:1234@localhost/wechat_app?charset=utf8mb4', echo=True)

# 创建数据库会话
Session = sessionmaker(bind=engine)
Base = declarative_base()