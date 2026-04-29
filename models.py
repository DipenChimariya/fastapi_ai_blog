from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="Anonymous")
    category = Column(String, default="General")
    date_posted = Column(DateTime, default=datetime.utcnow)