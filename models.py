from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    track_code = Column(String, unique=True, nullable=False)
    status = Column(Integer, nullable=False)
    flight = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///crm.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
