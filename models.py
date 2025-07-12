from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Создание базы данных
engine = create_engine('sqlite:///crm.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
