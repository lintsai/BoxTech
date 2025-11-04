"""
Test MediaPipe Pose Estimation
成功標準:
- 關鍵點檢測率 > 95%
- 處理速度 > 30 FPS (平均處理幀率)
- 無錯誤或警告 (抑制 TensorFlow/Deprecation 輸出)
"""

import os
import warnings
import time
import cv2
import sys
from pathlib import Path

# 靜音 TensorFlow/Abseil 大量日誌與警告
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")  # 0=all, 1=filter INFO, 2=+WARNING, 3=+ERROR
warnings.filterwarnings("ignore", category=DeprecationWarning)

import mediapipe as mp  # noqa: E402

def test_mediapipe(video_path: str, target_width: int = 640):
    """測試 MediaPipe 姿態估計

    會將影格縮放到 target_width 以提升效能, 預設 640。
    """
    
    print(f"📹 Processing: {video_path}")
    
    mp_pose = mp.solutions.pose
    
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=0,  # lite 模型, 明顯加速
        smooth_landmarks=True,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
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
    t0 = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Optional: resize for speed (維持比例)
        if target_width and frame.shape[1] > target_width:
            scale = target_width / frame.shape[1]
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)), interpolation=cv2.INTER_AREA)

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
    
    elapsed = max(1e-6, time.time() - t0)
    processing_fps = frame_count / elapsed
    detection_rate = (detected_count / frame_count) * 100 if frame_count else 0.0
    
    print("\n" + "=" * 50)
    print("✅ Processing completed!")
    print(f"   Total frames: {frame_count}")
    print(f"   Detected frames: {detected_count}")
    print(f"   Detection rate: {detection_rate:.1f}%")
    print(f"   Processing FPS (avg): {processing_fps:.1f}")
    
    passed = (detection_rate > 95.0) and (processing_fps > 30.0)
    if passed:
        print("   ✅ Meets success criteria (keypoints > 95% and FPS > 30)")
    else:
        # 不輸出警告等級, 但清楚標示未達標準
        print("   ❗ Criteria not met. Try reducing target_width or improving video conditions.")

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
