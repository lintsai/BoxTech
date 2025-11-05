"""
Generate scan reports: duplicates, anomalies, coverage stats.
Outputs to output/scan_reports/.
"""
import sys
from pathlib import Path
from collections import Counter, defaultdict
import json
import csv
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import func
from backend.database.connection import SessionLocal
from backend.models.schemas import Video

OUT_DIR = Path("output/scan_reports")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    db = SessionLocal()
    try:
        rows = db.query(Video).all()
        by_hash = defaultdict(list)
        anomalies = []

        for v in rows:
            by_hash[v.file_hash].append(v)
            if (not v.fps or v.fps <= 0) or (not v.duration_seconds or v.duration_seconds <= 0):
                anomalies.append({
                    "id": str(v.id),
                    "file_path": v.file_path,
                    "fps": v.fps,
                    "duration": v.duration_seconds,
                    "resolution": v.resolution,
                })
            # 可能是圖片誤入
            low_name = (v.file_path or "").lower()
            if low_name.endswith((".heic",".jpg",".jpeg",".png")):
                anomalies.append({
                    "id": str(v.id),
                    "file_path": v.file_path,
                    "reason": "non-video-extension"
                })

        duplicates = [
            {"file_hash": h, "count": len(lst), "files": [x.file_path for x in lst]}
            for h, lst in by_hash.items() if len(lst) > 1
        ]

        meta_counts = {
            "by_location": Counter([v.location or "(unknown)" for v in rows]),
            "by_training_type": Counter([v.training_type or "(unknown)" for v in rows]),
        }

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        json_path = OUT_DIR / f"scan_report_{ts}.json"
        csv_dup_path = OUT_DIR / f"duplicates_{ts}.csv"
        csv_anom_path = OUT_DIR / f"anomalies_{ts}.csv"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "total": len(rows),
                "duplicates": duplicates,
                "anomalies": anomalies,
                "meta_counts": {
                    "by_location": dict(meta_counts["by_location"]),
                    "by_training_type": dict(meta_counts["by_training_type"]),
                }
            }, f, ensure_ascii=False, indent=2)

        with open(csv_dup_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["file_hash", "count", "files"])
            for d in duplicates:
                w.writerow([d["file_hash"], d["count"], " | ".join(d["files"])])

        with open(csv_anom_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "file_path", "fps", "duration", "resolution", "reason"])
            for a in anomalies:
                w.writerow([
                    a.get("id"), a.get("file_path"),
                    a.get("fps"), a.get("duration"), a.get("resolution"),
                    a.get("reason")
                ])

        print(f"✅ Report JSON: {json_path}")
        print(f"✅ Duplicates CSV: {csv_dup_path}")
        print(f"✅ Anomalies CSV: {csv_anom_path}")
    finally:
        db.close()

if __name__ == "__main__":
    main()