"""
SQLAlchemy Database Models
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    current_level = Column(Integer, default=1)
    
    videos = relationship("Video", back_populates="user")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    file_path = Column(Text, nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Float)
    fps = Column(Integer)
    resolution = Column(String(20))
    file_size_bytes = Column(Integer)
    processing_status = Column(String(20), default="pending")
    s3_url = Column(Text)
    
    # Metadata
    training_date = Column(DateTime)
    training_type = Column(String(50))
    location = Column(String(100))
    
    user = relationship("User", back_populates="videos")
    actions = relationship("Action", back_populates="video")

class Action(Base):
    __tablename__ = "actions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"))
    action_type = Column(String(50), nullable=False)
    start_frame = Column(Integer, nullable=False)
    end_frame = Column(Integer, nullable=False)
    duration_seconds = Column(Float)
    confidence = Column(Float)
    
    # Assessment results
    quality_score = Column(JSON)
    problems = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    video = relationship("Video", back_populates="actions")
    suggestion = relationship("Suggestion", uselist=False, back_populates="action")

class Suggestion(Base):
    __tablename__ = "suggestions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_id = Column(UUID(as_uuid=True), ForeignKey("actions.id", ondelete="CASCADE"))
    analysis = Column(Text)
    improvements = Column(JSON)
    recommended_drills = Column(JSON)
    advanced_tip = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    action = relationship("Action", back_populates="suggestion")
