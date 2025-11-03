"""
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
    pattern = r"(\d{8})-(.+?)[\.\s]"
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
    
    print("\n" + "=" * 50)
    print(f"📊 Scan Summary:")
    print(f"   New videos: {new_count}")
    print(f"   Duplicates: {duplicate_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total processed: {len(video_files)}")

if __name__ == "__main__":
    print("🔍 BoxTech Video Scanner")
    print("=" * 50)
    scan_videos()
