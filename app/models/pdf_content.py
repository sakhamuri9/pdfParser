from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    
    headings = relationship("Heading", back_populates="topic", cascade="all, delete-orphan")

class Heading(Base):
    __tablename__ = "headings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    topic = relationship("Topic", back_populates="headings")
    subheadings = relationship("Subheading", back_populates="heading", cascade="all, delete-orphan")

class Subheading(Base):
    __tablename__ = "subheadings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    heading_id = Column(Integer, ForeignKey("headings.id"))
    
    heading = relationship("Heading", back_populates="subheadings")
