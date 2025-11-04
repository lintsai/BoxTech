"""
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
    
    print("\n" + "=" * 50)
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
