import random
from database import Base
from sqlalchemy import Column, Integer, String


# 定义短信认证码的数据模型
class Verification_code(Base):
    __tablename__ = 'verification_codes'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    verification_code = Column(String(6))

    def generate_verification_code(self):
        code = ''.join(random.choices('0123456789', k=6))
        self.verification_code = code
        return code
