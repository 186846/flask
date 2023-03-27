import datetime
import uuid

from database import Base
from sqlalchemy import Column, String, Date


# 定义公告表
class Notice(Base):
    __tablename__ = 'notices'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String(36), nullable=False)
    content = Column(String(3000), nullable=False)
    create_time = Column(Date, default=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return f"<Notice(id='{self.id}',title='{self.title}',content='{self.content}',create_time='{self.create_time}')>"
