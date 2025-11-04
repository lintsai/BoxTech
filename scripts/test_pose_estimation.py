"""
Test MediaPipe Pose Estimation
"""

import cv2
import mediapipe as mp
import sys
from pathlib import Path

def test_mediapipe(video_path: str):
    """測試 MediaPipe 姿態估計"""
    
    print(f"📹 Processing: {video_path}")
    
    mp_pose = mp.solutions.pose
    
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
    
    print("\n" + "=" * 50)
    print("✅ Processing completed!")
    print(f"   Total frames: {frame_count}")
    print(f"   Detected frames: {detected_count}")
    print(f"   Detection rate: {detection_rate:.1f}%")
    
    if detection_rate > 80:
        print("   ✅ Detection rate is good!")
    else:
        print("   ⚠️  Detection rate is low. Check video quality.")

if __name__ == "__main__":
    def _find_default_video() -> str | None:
        base = Path("Midea")
        if not base.exists():
            return None
        video_exts = [".mp4", ".mov", ".MOV", ".avi"]
        candidates = []
        for ext in video_exts:
            candidates.extend(base.rglob(f"*{ext}"))
        if not candidates:
            return None
        # pick the most recently modified file
        try:
            newest = max(candidates, key=lambda p: p.stat().st_mtime)
            return str(newest)
        except Exception:
            return str(candidates[0])

    if len(sys.argv) < 2:
        auto = _find_default_video()
        if auto:
            print(f"ℹ️  No video_path provided. Using latest found video: {auto}")
            test_mediapipe(auto)
        else:
            print("Usage: python test_pose_estimation.py <video_path>")
            print("No video found under ./Midea. Please provide a path to a video file.")
            sys.exit(1)
    else:
        test_mediapipe(sys.argv[1])
