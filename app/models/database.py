from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    dictionary_items = relationship("DictionaryItem", back_populates="user")

class DictionaryItem(Base):
    __tablename__ = "dictionary_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="dictionary_items")

# Create SQLite database
engine = create_engine("sqlite:///./dictionary.db")
Base.metadata.create_all(bind=engine) 