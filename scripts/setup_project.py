"""
BoxTech Project Setup Script
自動建立專案目錄結構和初始化文件
"""

import os
from pathlib import Path

def create_directory(path: str):
    """建立目錄"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {path}")

def create_file(path: str, content: str = ""):
    """建立檔案"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")

def main():
    """主函數 - 建立專案結構"""
    
    print("🚀 BoxTech Project Setup")
    print("=" * 50)
    
    # 將專案結構建立在專案根目錄（非 scripts/ 內）
    base_dir = Path(__file__).parent.parent
    
    # 後端目錄結構
    backend_dirs = [
        "backend",
        "backend/api",
        "backend/services",
        "backend/models",
        "backend/database",
        "backend/tasks",
        "backend/utils",
        "backend/tests",
    ]
    
    # 前端目錄結構
    frontend_dirs = [
        "frontend",
        "frontend/app",
        "frontend/components",
        "frontend/lib",
        "frontend/public",
    ]
    
    # 機器學習目錄
    ml_dirs = [
        "ml_models",
        "ml_models/action_classifier",
        "ml_models/quality_model",
        "ml_models/training_scripts",
        "ml_models/datasets",
    ]
    
    # 其他目錄
    other_dirs = [
        "scripts",
        "docs",
        "tests",
        "temp",
        "output",
        "logs",
    ]
    
    # 確保影片目錄存在 .gitkeep
    media_dirs = [
        "Midea",
        "Midea/LeYuan 樂嫄運動空間",
        "Midea/拳擊基地",
    ]
    
    all_dirs = backend_dirs + frontend_dirs + ml_dirs + other_dirs + media_dirs
    
    print("\n📁 Creating directories...")
    for dir_path in all_dirs:
        create_directory(base_dir / dir_path)
    
    print("\n📄 Creating initial files...")
    
    # Backend __init__.py files
    backend_modules = [
        "backend",
        "backend/api",
        "backend/services",
        "backend/models",
        "backend/database",
        "backend/tasks",
        "backend/utils",
    ]
    
    for module in backend_modules:
        create_file(base_dir / module / "__init__.py", "")
    
    # Backend main.py
    main_py_content = '''"""
BoxTech FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BoxTech API",
    description="AI Boxing Training Analysis System",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BoxTech API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    create_file(base_dir / "backend" / "main.py", main_py_content)
    
    # Database models
    models_content = '''"""
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
'''
    create_file(base_dir / "backend" / "models" / "schemas.py", models_content)
    
    # Database connection
    db_connection_content = '''"""
Database Connection and Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DB_ECHO", "False") == "True",
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from backend.models.schemas import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
'''
    create_file(base_dir / "backend" / "database" / "connection.py", db_connection_content)
    
    # Script: Initialize database
    init_db_script = '''"""
Initialize Database Script
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database.connection import init_db

if __name__ == "__main__":
    print("🗄️  Initializing BoxTech Database...")
    try:
        init_db()
        print("✅ Database initialization completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
'''
    create_file(base_dir / "scripts" / "init_database.py", init_db_script)
    
    # Script: Scan videos
    scan_videos_script = '''"""
Video Scanning Script
掃描 Midea 資料夾中的所有影片並記錄到資料庫
"""

import sys
from pathlib import Path
import hashlib
import cv2
from datetime import datetime
import re

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database.connection import SessionLocal
from backend.models.schemas import Video

def calculate_file_hash(file_path: str) -> str:
    """計算檔案 SHA-256 hash"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_video_info(file_path: str) -> dict:
    """提取影片資訊"""
    cap = cv2.VideoCapture(file_path)
    
    info = {
        'fps': int(cap.get(cv2.CAP_PROP_FPS)),
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    
    info['duration_seconds'] = info['total_frames'] / info['fps'] if info['fps'] > 0 else 0
    info['resolution'] = f"{info['width']}x{info['height']}"
    
    cap.release()
    return info

def parse_filename(filename: str) -> dict:
    """從檔名解析日期和類型"""
    # 範例: 20251102-團課-打靶 01.MOV
    pattern = r"(\\d{8})-(.+?)[\\.\\s]"
    match = re.match(pattern, filename)
    
    metadata = {}
    if match:
        date_str = match.group(1)
        type_str = match.group(2)
        
        try:
            metadata['training_date'] = datetime.strptime(date_str, "%Y%m%d")
        except:
            pass
        
        metadata['training_type'] = type_str
    
    return metadata

def scan_videos(directory: str = "./Midea"):
    """掃描影片資料夾"""
    db = SessionLocal()
    
    video_extensions = ['.mp4', '.mov', '.MOV', '.avi', '.HEIC', '.heic']
    base_path = Path(directory)
    
    video_files = []
    for ext in video_extensions:
        video_files.extend(base_path.rglob(f"*{ext}"))
    
    print(f"📹 Found {len(video_files)} video files")
    
    new_count = 0
    duplicate_count = 0
    error_count = 0
    
    for video_path in video_files:
        try:
            # 計算 hash
            file_hash = calculate_file_hash(str(video_path))
            
            # 檢查是否已存在
            existing = db.query(Video).filter(Video.file_hash == file_hash).first()
            if existing:
                print(f"⏭️  Skip (duplicate): {video_path.name}")
                duplicate_count += 1
                continue
            
            # 提取影片資訊
            print(f"📊 Processing: {video_path.name}")
            video_info = extract_video_info(str(video_path))
            file_metadata = parse_filename(video_path.name)
            
            # 判斷位置
            location = "未知"
            if "LeYuan" in str(video_path) or "樂嫄" in str(video_path):
                location = "樂嫄運動空間"
            elif "拳擊基地" in str(video_path):
                location = "拳擊基地"
            
            # 建立記錄
            video = Video(
                file_path=str(video_path),
                file_hash=file_hash,
                duration_seconds=video_info['duration_seconds'],
                fps=video_info['fps'],
                resolution=video_info['resolution'],
                file_size_bytes=video_path.stat().st_size,
                processing_status="pending",
                training_date=file_metadata.get('training_date'),
                training_type=file_metadata.get('training_type'),
                location=location
            )
            
            db.add(video)
            db.commit()
            
            print(f"✅ Added: {video_path.name}")
            new_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {video_path.name}: {e}")
            error_count += 1
            continue
    
    db.close()
    
    print("\\n" + "=" * 50)
    print(f"📊 Scan Summary:")
    print(f"   New videos: {new_count}")
    print(f"   Duplicates: {duplicate_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total processed: {len(video_files)}")

if __name__ == "__main__":
    print("🔍 BoxTech Video Scanner")
    print("=" * 50)
    scan_videos()
'''
    create_file(base_dir / "scripts" / "scan_videos.py", scan_videos_script)
    
    # Test script for MediaPipe
    test_mediapipe = '''"""
Test MediaPipe Pose Estimation
"""

import cv2
import mediapipe as mp
import sys

def test_mediapipe(video_path: str):
    """測試 MediaPipe 姿態估計"""
    
    print(f"📹 Processing: {video_path}")
    
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("❌ Cannot open video file")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"📊 Video info: {total_frames} frames, {fps} FPS")
    
    frame_count = 0
    detected_count = 0
    
    print("🔄 Processing frames...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Detect pose
        results = pose.process(image)
        
        if results.pose_landmarks:
            detected_count += 1
        
        # Show progress every 30 frames
        if frame_count % 30 == 0:
            detection_rate = (detected_count / frame_count) * 100
            print(f"  Frame {frame_count}/{total_frames} - Detection rate: {detection_rate:.1f}%")
    
    cap.release()
    pose.close()
    
    detection_rate = (detected_count / frame_count) * 100
    
    print("\\n" + "=" * 50)
    print(f"✅ Processing completed!")
    print(f"   Total frames: {frame_count}")
    print(f"   Detected frames: {detected_count}")
    print(f"   Detection rate: {detection_rate:.1f}%")
    
    if detection_rate > 80:
        print("   ✅ Detection rate is good!")
    else:
        print("   ⚠️  Detection rate is low. Check video quality.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pose_estimation.py <video_path>")
        sys.exit(1)
    
    test_mediapipe(sys.argv[1])
'''
    create_file(base_dir / "scripts" / "test_pose_estimation.py", test_mediapipe)
    
    # .gitkeep for media directories
    for media_dir in media_dirs:
        gitkeep_path = base_dir / media_dir / ".gitkeep"
        if not gitkeep_path.exists():
            create_file(gitkeep_path, "")
    
    # README for ml_models
    ml_readme = '''# Machine Learning Models

This directory contains:
- Trained models (action classifier, quality assessor)
- Training scripts
- Model configurations
- Dataset preparation scripts

## Directory Structure

- `action_classifier/` - Action recognition model
- `quality_model/` - Action quality assessment model
- `training_scripts/` - Scripts for training models
- `datasets/` - Prepared datasets (not in Git)

## Note

Large model files (.h5, .pth, .pt) are excluded from Git.
Download pre-trained models from [link to be added].
'''
    create_file(base_dir / "ml_models" / "README.md", ml_readme)
    
    print("\n" + "=" * 50)
    print("✅ Project setup completed!")
    print("\n📝 Next steps:")
    print("1. Copy .env.example to .env and fill in your API keys")
    print("2. Start Docker containers: docker-compose up -d")
    print("3. Install Python dependencies: pip install -r requirements.txt")
    print("4. Initialize database: python scripts/init_database.py")
    print("5. Scan videos: python scripts/scan_videos.py")
    print("6. Start backend (choose one):")
    print("   - cd backend && python main.py")
    print("   - uvicorn backend.main:app --reload --port 8000")
    print("\n🚀 Happy coding!")

if __name__ == "__main__":
    main()
