"""
Pose extraction and visualization

Features:
- Extract 33 MediaPipe Pose landmarks per frame (x, y, z, visibility)
- Generate an overlay video visualizing pose skeleton
- Print validation summary (detection rate, avg visibility, processing FPS)
- Optionally save landmarks to JSON and/or database (if VIDEO record exists)

Usage examples (PowerShell):
  python scripts/pose_extract_and_visualize.py
  python scripts/pose_extract_and_visualize.py --video "Midea\拳擊基地\20250323-體驗課01.mp4"
  python scripts/pose_extract_and_visualize.py --save-json --out-video
  python scripts/pose_extract_and_visualize.py --db --model-complexity 1 --target-width 960
"""

from __future__ import annotations

import os
import json
import time
import warnings
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import cv2  # noqa: E402
import mediapipe as mp  # noqa: E402


@dataclass
class Summary:
    total_frames: int
    detected_frames: int
    detection_rate: float
    processing_fps: float
    avg_visibility: float
    passed_detection: bool
    passed_fps: bool
    passed_visibility: bool


CRITICAL_IDXS = [
    11, 12, 13, 14, 15, 16,  # shoulders, elbows, wrists
    23, 24, 25, 26, 27, 28,  # hips, knees, ankles
]


def auto_find_video() -> Optional[str]:
    base = Path("Midea")
    if not base.exists():
        return None
    video_exts = [".mp4", ".mov", ".MOV", ".avi"]
    candidates = []
    for ext in video_exts:
        candidates.extend(base.rglob(f"*{ext}"))
    if not candidates:
        return None
    try:
        newest = max(candidates, key=lambda p: p.stat().st_mtime)
        return str(newest)
    except Exception:
        return str(candidates[0])


def ensure_dirs(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def make_output_paths(video_path: str, write_video: bool, write_json: bool):
    vp = Path(video_path)
    stem = vp.stem
    vis_out = None
    json_out = None
    if write_video:
        vis_out = Path("output/visualizations") / f"{stem}_pose.mp4"
        ensure_dirs(vis_out)
    if write_json:
        json_out = Path("output/landmarks") / f"{stem}_landmarks.json"
        ensure_dirs(json_out)
    return vis_out, json_out


def extract_and_visualize(
    video_path: str,
    target_width: int = 640,
    model_complexity: int = 0,
    out_video_path: Optional[Path] = None,
    out_json_path: Optional[Path] = None,
    save_db: bool = False,
) -> Summary:
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=model_complexity,
        smooth_landmarks=True,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    orig_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    writer = None
    if out_video_path is not None:
        # we'll write at original fps
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # delay feature: determine size from first processed frame
        writer = (fourcc, orig_fps, None)  # temp placeholder

    frame_count = 0
    detected_count = 0
    vis_sum = 0.0
    per_frame_data: List[Dict] = []

    t0 = time.time()

    drawing = mp.solutions.drawing_utils
    styles = mp.solutions.drawing_styles

    # To resolve DB models lazily only when needed
    db_session = None
    video_model = pose_data_model = None
    video_record = None
    if save_db:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from backend.database.connection import SessionLocal
            from backend.models.schemas import Video as _Video, PoseData as _PoseData  # type: ignore

            video_model, pose_data_model = _Video, _PoseData
            db_session = SessionLocal()
            video_record = db_session.query(video_model).filter(video_model.file_path == str(Path(video_path))).first()
        except Exception as e:
            print(f"⚠️  DB unavailable or video not indexed: {e}")
            save_db = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        if target_width and frame.shape[1] > target_width:
            scale = target_width / frame.shape[1]
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)), interpolation=cv2.INTER_AREA)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        det = results.pose_landmarks is not None
        if det:
            detected_count += 1
            lms = results.pose_landmarks.landmark
            # average visibility across critical joints
            if lms:
                vis_vals = [max(0.0, min(1.0, getattr(lms[i], "visibility", 0.0))) for i in CRITICAL_IDXS]
                vis_sum += sum(vis_vals) / len(CRITICAL_IDXS)

            if out_json_path is not None or save_db:
                # Collect landmarks for JSON/DB
                lm_list = [
                    {
                        "x": lm.x,
                        "y": lm.y,
                        "z": lm.z,
                        "visibility": getattr(lm, "visibility", None),
                    }
                    for lm in lms
                ]
                per_frame_data.append(
                    {
                        "frame": frame_count,
                        "timestamp": cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0,
                        "landmarks": lm_list,
                    }
                )

        if out_video_path is not None:
            # Draw overlay
            annotated = frame.copy()
            if det:
                drawing.draw_landmarks(
                    annotated,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=styles.get_default_pose_landmarks_style(),
                )
            # Init writer with frame size once
            if isinstance(writer, tuple):
                fourcc, fps, _ = writer
                writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (annotated.shape[1], annotated.shape[0]))
            writer.write(annotated)

        if frame_count % 30 == 0:
            elapsed = max(1e-6, time.time() - t0)
            print(f"  Frame {frame_count} - DetRate: {detected_count / frame_count * 100:.1f}% | ProcFPS: {frame_count / elapsed:.1f}")

    cap.release()
    pose.close()
    if isinstance(writer, cv2.VideoWriter):
        writer.release()

    elapsed = max(1e-6, time.time() - t0)
    processing_fps = frame_count / elapsed
    detection_rate = (detected_count / frame_count) * 100 if frame_count else 0.0
    avg_visibility = (vis_sum / detected_count) if detected_count else 0.0

    # Save JSON
    if out_json_path is not None and per_frame_data:
        out_payload = {
            "video_path": str(Path(video_path)),
            "total_frames": frame_count,
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "data": per_frame_data,
        }
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(out_payload, f, ensure_ascii=False)
        print(f"💾 Saved landmarks JSON: {out_json_path}")

    # Save DB (bulk)
    if save_db and db_session and video_record and per_frame_data and pose_data_model is not None:
        rows = [
            pose_data_model(
                video_id=video_record.id,
                frame_number=fd["frame"],
                timestamp=fd["timestamp"],
                landmarks=fd["landmarks"],
            )
            for fd in per_frame_data
        ]
        db_session.bulk_save_objects(rows)
        db_session.commit()
        print(f"🗄️  Saved {len(rows)} frames to database (pose_data)")

    passed_detection = detection_rate > 95.0
    passed_fps = processing_fps > 30.0
    passed_visibility = avg_visibility >= 0.5

    return Summary(
        total_frames=frame_count,
        detected_frames=detected_count,
        detection_rate=detection_rate,
        processing_fps=processing_fps,
        avg_visibility=avg_visibility,
        passed_detection=passed_detection,
        passed_fps=passed_fps,
        passed_visibility=passed_visibility,
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", type=str, default=None, help="Path to input video; auto-pick latest from ./Midea if omitted")
    p.add_argument("--target-width", type=int, default=640, help="Resize frame width for processing speed (keep aspect ratio)")
    p.add_argument("--model-complexity", type=int, default=0, choices=[0, 1, 2], help="MediaPipe Pose model complexity (0=lite, 2=heavy)")
    p.add_argument("--out-video", action="store_true", help="Write visualization video to output/visualizations/")
    p.add_argument("--save-json", action="store_true", help="Save landmarks to output/landmarks/<name>_landmarks.json")
    p.add_argument("--db", action="store_true", help="Save per-frame landmarks into database pose_data table (if video indexed)")
    args = p.parse_args()

    video = args.video or auto_find_video()
    if not video:
        print("❌ No video provided and none found in ./Midea")
        return

    print(f"📹 Processing: {video}")
    out_video_path, out_json_path = make_output_paths(video, args.out_video, args.save_json)

    summary = extract_and_visualize(
        video,
        target_width=args.target_width,
        model_complexity=args.model_complexity,
        out_video_path=out_video_path,
        out_json_path=out_json_path,
        save_db=args.db,
    )

    print("\n" + "=" * 50)
    print("📊 Pose Extraction Summary")
    print(f"   Total frames: {summary.total_frames}")
    print(f"   Detected frames: {summary.detected_frames}")
    print(f"   Detection rate: {summary.detection_rate:.1f}%")
    print(f"   Processing FPS (avg): {summary.processing_fps:.1f}")
    print(f"   Avg visibility (critical joints): {summary.avg_visibility:.2f}")

    ok = summary.passed_detection and summary.passed_fps
    if ok:
        print("   ✅ Meets success criteria (keypoints > 95% and FPS > 30)")
    else:
        print("   ❗ Criteria not met")

    if not summary.passed_visibility:
        print("   ℹ️  Visibility is low (<0.5). Subject may be partially occluded or out of frame.")

    if out_video_path is not None:
        print(f"🎞️  Visualization saved to: {out_video_path}")
    if out_json_path is not None:
        print(f"💾 Landmarks saved to: {out_json_path}")


if __name__ == "__main__":
    main()
