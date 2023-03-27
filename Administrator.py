import uuid

from database import Base
from sqlalchemy import Column, String

# 定义管理员数据模型
class Administrator(Base):
    __tablename__ = 'administrators'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(20), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    token = Column(String(36), nullable=True)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', password='{self.password}', token='{self.token}')>"

