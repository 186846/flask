import hashlib
import uuid

from database import Base
from sqlalchemy import  Column, Integer, String

# 定义用户信息数据模型
class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(20))
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    token = Column(String(36), nullable=True)

    def __init__(self, username, phone_number, password, token):
        self.username = username
        self.phone_number = phone_number
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.token = token

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()