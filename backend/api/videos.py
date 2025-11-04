"""
Video-related API routes under /api/v1/videos
"""

from typing import List, Optional
from uuid import UUID
import threading

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

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
def list_videos(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    q = db.query(Video).order_by(Video.upload_date.desc()).offset(offset).limit(limit)
    items = [_video_to_dict(v) for v in q.all()]
    total = db.query(Video).count()
    return {"total": total, "count": len(items), "items": items}


@router.get("/{video_id}")
def get_video(video_id: UUID, db: Session = Depends(get_db)):
    v: Optional[Video] = db.query(Video).filter(Video.id == video_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    return _video_to_dict(v)


@router.post("/scan", status_code=202)
def trigger_scan(directory: str = Body(default="Midea", embed=True)):
    """Trigger a background scan of the media directory.

    Note: This launches the existing scripts.scan_videos.scan_videos function in a
    background thread to avoid blocking the API. Logs will appear in server output.
    """
    try:
        # Ensure scripts is importable and call its scan function in background
        import scripts.scan_videos as sv  # type: ignore

        t = threading.Thread(target=sv.scan_videos, kwargs={"directory": directory}, daemon=True)
        t.start()
        return {"status": "started", "directory": directory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")
