"""
Check Scan Results
Summarize videos indexed in the database.
"""

import sys
from pathlib import Path
from collections import Counter
from datetime import datetime

# Ensure backend is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import func
from backend.database.connection import SessionLocal
from backend.models.schemas import Video


def human_size(num_bytes: int) -> str:
    try:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if num_bytes < 1024:
                return f"{num_bytes:.1f} {unit}"
            num_bytes /= 1024
    except Exception:
        return "-"
    return f"{num_bytes:.1f} PB"


essentials = (
    ("Total videos", lambda db: db.query(Video).count()),
    ("By location", lambda db: db.query(Video.location, func.count(Video.id)).group_by(Video.location).all()),
    ("By training type", lambda db: db.query(Video.training_type, func.count(Video.id)).group_by(Video.training_type).all()),
)


def main():
    print("📋 BoxTech Scan Results")
    print("=" * 50)

    db = SessionLocal()

    try:
        total = db.query(Video).count()
        print(f"✅ Total videos: {total}")

        # By location
        rows = db.query(Video.location, func.count(Video.id)).group_by(Video.location).all()
        if rows:
            print("\n📍 By location:")
            for loc, cnt in rows:
                loc_disp = loc or "(unknown)"
                print(f"  - {loc_disp}: {cnt}")

        # By training type
        rows = db.query(Video.training_type, func.count(Video.id)).group_by(Video.training_type).all()
        if rows:
            print("\n🏷️ By training type:")
            for t, cnt in rows:
                t_disp = t or "(unknown)"
                print(f"  - {t_disp}: {cnt}")

        # Files that look like images (e.g., .heic) mistakenly indexed
        suspicious_exts = {".heic", ".jpg", ".jpeg", ".png"}
        sus = (
            db.query(Video)
            .filter(func.lower(func.right(Video.file_path, 5)).like("%.heic"))
            .all()
        )
        if sus:
            print("\n⚠️ Non-video entries (possible images):")
            for v in sus:
                print(f"  - {Path(v.file_path).name} | res={v.resolution} | fps={v.fps}")

        # Recent 10
        recent = db.query(Video).order_by(Video.upload_date.desc()).limit(10).all()
        if recent:
            print("\n🕒 Recent 10:")
            for v in recent:
                dt = v.upload_date.strftime("%Y-%m-%d %H:%M") if v.upload_date else "-"
                print(
                    f"  - {Path(v.file_path).name} | {v.resolution} @ {v.fps}fps | {human_size(v.file_size_bytes or 0)} | {dt}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
