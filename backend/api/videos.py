"""
Video-related API routes under /api/v1/videos
"""

from typing import List, Optional
from uuid import UUID
import threading
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from backend.database.connection import get_db
from backend.models.schemas import Video


router = APIRouter(prefix="/api/v1/videos", tags=["videos"])


def _video_to_dict(v: Video) -> dict:
    return {
        "id": str(v.id),
        "file_path": v.file_path,
        "file_hash": v.file_hash,
        "upload_date": v.upload_date.isoformat() if v.upload_date else None,
        "duration_seconds": v.duration_seconds,
        "fps": v.fps,
        "resolution": v.resolution,
        "file_size_bytes": v.file_size_bytes,
        "processing_status": v.processing_status,
        "training_date": v.training_date.isoformat() if v.training_date else None,
        "training_type": v.training_type,
        "location": v.location,
    }


@router.get("")
def list_videos(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    training_type: Optional[str] = None,
    location: Optional[str] = None,
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    q: Optional[str] = Query(None, description="filename substring"),
    order_by: str = Query("upload_date", pattern="^(upload_date|training_date|file_size_bytes|fps)$"),
    order_dir: str = Query("desc", pattern="^(asc|desc)$"),
):
    qset = db.query(Video)

    if training_type:
        qset = qset.filter(Video.training_type == training_type)
    if location:
        qset = qset.filter(Video.location == location)
    if date_from:
        try:
            dt = datetime.strptime(date_from, "%Y-%m-%d")
            qset = qset.filter(Video.upload_date >= dt)
        except ValueError:
            raise HTTPException(400, detail="Invalid date_from")
    if date_to:
        try:
            dt = datetime.strptime(date_to, "%Y-%m-%d")
            qset = qset.filter(Video.upload_date <= dt)
        except ValueError:
            raise HTTPException(400, detail="Invalid date_to")
    if q:
        # 檔名片段搜尋
        like = f"%{q}%"
        qset = qset.filter(Video.file_path.ilike(like))

    # 排序
    col = getattr(Video, order_by)
    qset = qset.order_by(desc(col) if order_dir == "desc" else asc(col))

    total = qset.count()
    items = [_video_to_dict(v) for v in qset.offset(offset).limit(limit).all()]
    return {"total": total, "count": len(items), "items": items}


@router.get("/{video_id}")
def get_video(video_id: UUID, db: Session = Depends(get_db)):
    v: Optional[Video] = db.query(Video).filter(Video.id == video_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    return _video_to_dict(v)


@router.post("/scan", status_code=202)
def trigger_scan(
    directory: str = Body(default="Midea", embed=True),
    mode: str = Body(default="incremental", embed=True)  # 'incremental' or 'full'
):
    """
    觸發背景掃描。
    mode:
      - incremental: 跳過 DB 已存在的檔案（現行行為）
      - full: 重新處理（傳遞旗標給掃描器）
    """
    try:
        import scripts.scan_videos as sv  # type: ignore
        kwargs = {"directory": directory, "mode": mode}
        t = threading.Thread(target=sv.scan_videos, kwargs=kwargs, daemon=True)
        t.start()
        return {"status": "started", "directory": directory, "mode": mode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")
    