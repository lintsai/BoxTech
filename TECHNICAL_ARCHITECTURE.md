# BoxTech 技術架構文件

## 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                        使用者層                              │
│  Web 前端 (Next.js)  │  Unity WebGL (3D 模擬)              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│                    (FastAPI + CORS)                          │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────┐    ┌─────────────┐
│   認證    │    │   業務邏輯   │
│  服務    │    │    服務      │
└──────────┘    └─────┬───────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌─────────┐
    │ 影片   │  │  AI    │  │  報表   │
    │ 處理   │  │  分析  │  │  生成   │
    └───┬────┘  └───┬────┘  └─────────┘
        │           │
        ▼           ▼
┌───────────────────────────────┐
│      Celery 任務隊列           │
│      (Redis Backend)          │
└───────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────┐
│            資料層                         │
│  PostgreSQL │ Redis │ S3 │ Pinecone    │
└──────────────────────────────────────────┘
```

---

## 核心模組設計

### 1. 影片處理模組 (Video Processing Service)

**職責**: 影片上傳、存儲、元數據提取、去重

```python
# services/video_processor.py

class VideoProcessor:
    def scan_new_videos(self, directory: str):
        """掃描指定目錄的新影片"""
        pass
    
    def extract_metadata(self, video_path: str):
        """提取影片元數據"""
        return {
            'duration': 120.5,
            'fps': 30,
            'resolution': '1920x1080',
            'file_size': 45_000_000,
            'hash': 'sha256...'
        }
    
    def check_duplicate(self, video_hash: str) -> bool:
        """檢查是否重複"""
        pass
    
    def upload_to_storage(self, video_path: str) -> str:
        """上傳至雲端儲存"""
        pass
```

**技術選擇**:
- **影片處理**: OpenCV + FFmpeg
- **雜湊計算**: hashlib (SHA-256) 或 videohash (影片指紋)
- **儲存**: 本地 + AWS S3 (備份)

---

### 2. 姿態估計模組 (Pose Estimation Service)

**職責**: 使用 MediaPipe 提取骨架數據

```python
# services/pose_estimator.py

import mediapipe as mp

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def extract_poses(self, video_path: str):
        """從影片提取每幀的姿態數據"""
        # 返回格式:
        # [
        #   {
        #     'frame_number': 0,
        #     'timestamp': 0.0,
        #     'landmarks': [
        #       {'x': 0.5, 'y': 0.3, 'z': -0.1, 'visibility': 0.99},
        #       ...  # 33 個關鍵點
        #     ]
        #   },
        #   ...
        # ]
        pass
    
    def normalize_landmarks(self, landmarks):
        """正規化座標 (以髖部為原點)"""
        pass
    
    def visualize_skeleton(self, video_path: str, poses_data):
        """在影片上繪製骨架"""
        pass
```

**輸出格式**:
```json
{
  "video_id": "uuid",
  "total_frames": 3600,
  "fps": 30,
  "poses": [
    {
      "frame": 0,
      "time": 0.0,
      "landmarks": {
        "nose": {"x": 0.5, "y": 0.2, "z": -0.05, "visibility": 0.99},
        "left_shoulder": {...},
        "right_shoulder": {...},
        ...
      }
    }
  ]
}
```

---

### 3. 動作識別模組 (Action Recognition Service)

**職責**: 識別拳擊動作類型

```python
# services/action_recognizer.py

import tensorflow as tf

class ActionRecognizer:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.action_classes = [
            'jab', 'cross', 'hook', 'uppercut', 
            'thai_kick', 'dodge', 'idle'
        ]
    
    def segment_actions(self, poses_sequence):
        """將連續姿態序列切割為單一動作"""
        # 使用速度變化檢測動作邊界
        pass
    
    def classify_action(self, pose_segment):
        """分類單一動作"""
        # 輸入: 30 幀的姿態序列
        # 輸出: {'action': 'jab', 'confidence': 0.95}
        pass
    
    def analyze_video(self, poses_data):
        """分析整支影片的動作序列"""
        # 返回:
        # [
        #   {
        #     'start_frame': 10,
        #     'end_frame': 40,
        #     'action': 'jab',
        #     'confidence': 0.92,
        #     'duration': 1.0
        #   },
        #   ...
        # ]
        pass
```

**模型訓練**:
```python
# ml_models/train_action_classifier.py

# 資料格式:
# - 輸入: (batch_size, 30, 33, 3)  # 30 幀, 33 個點, 3D 座標
# - 輸出: (batch_size, num_classes)

model = tf.keras.Sequential([
    tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(action_classes), activation='softmax')
])
```

---

### 4. 動作品質評估模組 (Quality Assessment Service)

**職責**: 評估動作正確性,檢測問題點

```python
# services/quality_assessor.py

class QualityAssessor:
    def __init__(self):
        self.standard_poses = self._load_standard_poses()
    
    def assess_action(self, user_action, action_type: str):
        """評估單一動作的品質"""
        standard = self.standard_poses[action_type]
        
        # 計算各項指標
        metrics = {
            'posture_score': self._check_posture(user_action),
            'trajectory_score': self._check_trajectory(user_action, standard),
            'power_transfer_score': self._check_power_chain(user_action),
            'guard_score': self._check_defensive_position(user_action),
            'speed_score': self._calculate_speed(user_action),
            'overall_score': 0.0
        }
        
        # 檢測問題點
        problems = self._detect_problems(user_action, standard)
        
        return {
            'metrics': metrics,
            'problems': problems,
            'overall_grade': self._calculate_grade(metrics)
        }
    
    def _check_posture(self, action):
        """檢查站姿 (重心、腳步)"""
        # 計算重心位置
        # 檢查雙腳距離
        pass
    
    def _check_trajectory(self, user_action, standard_action):
        """檢查出拳軌跡"""
        # 使用 DTW (Dynamic Time Warping) 對齊
        # 計算軌跡偏差
        pass
    
    def _check_power_chain(self, action):
        """檢查力量傳遞鏈 (腿→腰→肩→拳)"""
        # 檢查各關節啟動順序
        # 計算旋轉角度
        pass
    
    def _detect_problems(self, user_action, standard):
        """檢測具體問題點"""
        problems = []
        
        # 範例問題檢測
        if self._elbow_too_wide(user_action):
            problems.append({
                'type': 'elbow_position',
                'severity': 'high',
                'frame': 15,
                'description': '手肘外張過大',
                'angle_deviation': 25  # 度
            })
        
        return problems
```

**評分標準**:
```yaml
評分維度:
  姿勢正確性 (0-20):
    - 站姿寬度 (應為肩寬 1.2 倍)
    - 重心位置 (前腳 60%, 後腳 40%)
    - 膝蓋微彎 (15-20 度)
  
  出拳軌跡 (0-20):
    - 直線度 (偏差 < 5cm)
    - 最短路徑
    - 收拳路徑相同
  
  力量傳遞 (0-20):
    - 後腳蹬地啟動
    - 腰部旋轉 (30-45 度)
    - 肩膀前送
    - 拳頭最後到達
  
  防守姿態 (0-20):
    - 非出拳手護頭 (距離臉 < 10cm)
    - 下巴內收
    - 肩膀抬起保護下巴
  
  速度 (0-20):
    - 出拳速度 (< 0.2 秒)
    - 收拳速度 (< 0.15 秒)
    - 連擊間隔 (< 0.5 秒)
```

---

### 5. AI 建議生成模組 (Suggestion Generator)

**職責**: 使用 LLM 生成改善建議

```python
# services/suggestion_generator.py

from openai import OpenAI

class SuggestionGenerator:
    def __init__(self):
        self.client = OpenAI()
        self.prompt_templates = self._load_templates()
    
    def generate_suggestions(self, assessment_result, action_type: str):
        """生成改善建議"""
        
        # 構建 Prompt
        prompt = self._build_prompt(assessment_result, action_type)
        
        # 呼叫 GPT-4
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # 解析回應
        suggestions = self._parse_response(response)
        
        return suggestions
    
    def _build_prompt(self, assessment, action_type):
        """構建提示詞"""
        problems_text = "\n".join([
            f"- {p['description']} (嚴重度: {p['severity']})"
            for p in assessment['problems']
        ])
        
        return f"""
你是一位專業的拳擊教練,正在分析學員的 {action_type} 動作。

動作評分:
- 姿勢正確性: {assessment['metrics']['posture_score']}/20
- 出拳軌跡: {assessment['metrics']['trajectory_score']}/20
- 力量傳遞: {assessment['metrics']['power_transfer_score']}/20
- 防守姿態: {assessment['metrics']['guard_score']}/20
- 速度: {assessment['metrics']['speed_score']}/20
總分: {assessment['metrics']['overall_score']}/100

發現的問題:
{problems_text}

請提供:
1. 問題分析 (2-3 句話說明主要問題)
2. 改善建議 (3-5 個具體的動作調整)
3. 推薦訓練 (2-3 個專項練習)
4. 進階提示 (1 個高階技巧)

請用專業但易懂的語言,具體且可執行。
"""
    
    def _get_system_prompt(self):
        return """
你是一位資深拳擊教練,有 20 年教學經驗。
你擅長用簡單明瞭的方式解釋技術動作。
你的建議總是具體、可執行、循序漸進。
你會根據學員的程度給予適當難度的建議。
"""
```

**輸出格式**:
```json
{
  "analysis": "您的 Jab 動作整體流暢,但手肘有外張的問題,這會降低出拳速度並容易被對手發現意圖。另外重心稍微偏後,導致力量傳遞不足。",
  
  "improvements": [
    {
      "priority": 1,
      "title": "修正手肘位置",
      "description": "出拳時保持手肘貼近身體中線,想像手肘沿著一條隱形的中央線移動。可以在鏡前練習,觀察手肘軌跡。",
      "visual_cue": "想像在身體前方有一片玻璃,手肘不能碰到玻璃"
    },
    {
      "priority": 2,
      "title": "調整重心分配",
      "description": "出拳瞬間將重心前移到前腳,比例約 70:30。出拳時感受前腳掌承受更多重量。"
    }
  ],
  
  "recommended_drills": [
    {
      "name": "牆邊 Jab 練習",
      "description": "站在距離牆壁 10cm 處練習 Jab,確保手肘不碰牆",
      "duration": "3 組 x 20 次",
      "focus": "手肘軌跡"
    },
    {
      "name": "重心轉移練習",
      "description": "慢動作出拳,專注感受重心從後腳轉移到前腳的過程",
      "duration": "5 分鐘",
      "focus": "力量傳遞"
    }
  ],
  
  "advanced_tip": "職業拳手在出拳時會微微內旋肩膀,這能增加觸及距離約 5-8cm,並且提升力量。試著在動作末端加入這個細節。"
}
```

---

### 6. RAG 知識庫模組 (RAG Knowledge Base)

**職責**: 檢索相似專家動作,增強 AI 建議

```python
# services/rag_service.py

from pinecone import Pinecone

class RAGService:
    def __init__(self):
        self.pc = Pinecone(api_key="your-api-key")
        self.index = self.pc.Index("boxing-expert-actions")
    
    def add_expert_video(self, video_id: str, poses_data, metadata: dict):
        """添加專家影片到知識庫"""
        # 提取特徵向量
        feature_vector = self._extract_features(poses_data)
        
        # 上傳到 Pinecone
        self.index.upsert(
            vectors=[{
                'id': video_id,
                'values': feature_vector,
                'metadata': {
                    'action_type': metadata['action_type'],
                    'skill_level': metadata['skill_level'],  # beginner/intermediate/pro
                    'athlete_name': metadata.get('athlete_name'),
                    'key_points': metadata.get('key_points', [])
                }
            }]
        )
    
    def find_similar_expert_actions(self, user_poses, action_type: str, top_k=3):
        """尋找相似的專家動作"""
        # 提取用戶動作特徵
        user_vector = self._extract_features(user_poses)
        
        # 搜尋
        results = self.index.query(
            vector=user_vector,
            filter={'action_type': action_type},
            top_k=top_k,
            include_metadata=True
        )
        
        return results
    
    def enhance_suggestion_with_rag(self, user_action, base_suggestion):
        """使用 RAG 增強建議"""
        # 找到相似的專家動作
        expert_actions = self.find_similar_expert_actions(
            user_action['poses'],
            user_action['type']
        )
        
        # 構建增強的 Prompt
        expert_references = "\n".join([
            f"專家範例 {i+1}: {match['metadata']['key_points']}"
            for i, match in enumerate(expert_actions['matches'])
        ])
        
        enhanced_prompt = f"""
{base_suggestion}

以下是相似動作的專家示範重點:
{expert_references}

請參考這些專家技巧,提供更具體的建議。
"""
        
        return enhanced_prompt
```

---

### 7. 能力評估模組 (Ability Assessment Service)

**職責**: 計算六角圖、等級評定

```python
# services/ability_assessor.py

class AbilityAssessor:
    def calculate_hexagon_stats(self, user_id: str, period='month'):
        """計算六角圖數據"""
        # 從資料庫拉取該期間所有訓練記錄
        records = self._get_training_records(user_id, period)
        
        stats = {
            'power': self._calculate_power(records),      # 0-100
            'speed': self._calculate_speed(records),      # 0-100
            'technique': self._calculate_technique(records),
            'defense': self._calculate_defense(records),
            'stamina': self._calculate_stamina(records),
            'footwork': self._calculate_footwork(records)
        }
        
        return stats
    
    def _calculate_power(self, records):
        """計算力量分數"""
        # 基於出拳速度、動作幅度
        scores = []
        for record in records:
            avg_punch_speed = record['metrics']['speed_score']
            motion_amplitude = record['metrics']['amplitude']
            scores.append((avg_punch_speed + motion_amplitude) / 2)
        return np.mean(scores)
    
    def calculate_level(self, hexagon_stats):
        """計算等級"""
        total_score = sum(hexagon_stats.values()) / len(hexagon_stats)
        
        levels = [
            (0, 30, 1, "初學者"),
            (31, 45, 2, "新手"),
            (46, 60, 3, "進階"),
            (61, 75, 4, "中階"),
            (76, 85, 5, "高階"),
            (86, 95, 6, "專業"),
            (96, 100, 7, "菁英")
        ]
        
        for min_score, max_score, level, name in levels:
            if min_score <= total_score <= max_score:
                return {
                    'level': level,
                    'name': name,
                    'score': total_score,
                    'next_level_score': max_score + 1
                }
```

---

### 8. 報表生成模組 (Report Generator)

**職責**: 生成日/週/月報表

```python
# services/report_generator.py

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class ReportGenerator:
    def generate_daily_report(self, user_id: str, date: datetime):
        """生成日報表"""
        data = self._collect_daily_data(user_id, date)
        
        report = {
            'date': date.isoformat(),
            'summary': {
                'total_videos': len(data['videos']),
                'total_actions': data['total_actions'],
                'training_duration': data['duration_minutes']
            },
            'action_breakdown': data['action_counts'],  # {'jab': 50, 'cross': 30, ...}
            'improvement_highlights': data['improvements'],
            'problem_areas': data['problems'],
            'today_recommendation': self._generate_daily_tips(data)
        }
        
        return report
    
    def generate_weekly_report(self, user_id: str, week_start: datetime):
        """生成週報表"""
        week_end = week_start + timedelta(days=7)
        data = self._collect_weekly_data(user_id, week_start, week_end)
        
        report = {
            'week': f"{week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}",
            'training_frequency': data['training_days'],  # 本週訓練 X 天
            'progress_chart': self._generate_progress_chart(data),
            'hexagon_comparison': {
                'this_week': data['hexagon_this_week'],
                'last_week': data['hexagon_last_week'],
                'changes': self._calculate_changes(
                    data['hexagon_this_week'],
                    data['hexagon_last_week']
                )
            },
            'best_action_this_week': data['best_action'],
            'focus_next_week': self._suggest_focus_areas(data)
        }
        
        return report
    
    def generate_pdf_report(self, report_data, output_path: str):
        """生成 PDF 報表"""
        # 使用 reportlab 或 weasyprint
        pass
```

---

## 資料庫 Schema

### PostgreSQL Tables

```sql
-- 使用者表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_level INT DEFAULT 1
);

-- 影片表
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    file_path TEXT NOT NULL,
    file_hash VARCHAR(64) UNIQUE NOT NULL,  -- SHA-256
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_seconds FLOAT,
    fps INT,
    resolution VARCHAR(20),
    file_size_bytes BIGINT,
    processing_status VARCHAR(20),  -- 'pending', 'processing', 'completed', 'failed'
    s3_url TEXT,
    
    -- 元數據
    training_date DATE,
    training_type VARCHAR(50),  -- '團課', '一對一', '自主訓練'
    location VARCHAR(100),  -- '樂嫄運動空間', '拳擊基地'
    
    INDEX idx_user_id (user_id),
    INDEX idx_processing_status (processing_status),
    INDEX idx_training_date (training_date)
);

-- 姿態數據表 (JSONB 存儲)
CREATE TABLE pose_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    frame_number INT NOT NULL,
    timestamp FLOAT NOT NULL,
    landmarks JSONB NOT NULL,  -- 33 個關鍵點
    
    INDEX idx_video_id (video_id)
);

-- 動作表
CREATE TABLE actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,  -- 'jab', 'cross', 'hook', ...
    start_frame INT NOT NULL,
    end_frame INT NOT NULL,
    duration_seconds FLOAT,
    confidence FLOAT,
    
    -- 評估結果
    quality_score JSONB,  -- {'posture': 18, 'trajectory': 15, ...}
    problems JSONB,       -- [{'type': 'elbow_position', ...}]
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_video_id (video_id),
    INDEX idx_action_type (action_type)
);

-- AI 建議表
CREATE TABLE suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_id UUID REFERENCES actions(id) ON DELETE CASCADE,
    analysis TEXT,
    improvements JSONB,
    recommended_drills JSONB,
    advanced_tip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 訓練記錄表 (聚合)
CREATE TABLE training_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_date DATE NOT NULL,
    total_duration_minutes INT,
    total_actions INT,
    action_breakdown JSONB,  -- {'jab': 50, 'cross': 30}
    average_scores JSONB,
    
    INDEX idx_user_date (user_id, session_date)
);

-- 能力評估表 (六角圖歷史)
CREATE TABLE ability_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    assessment_date DATE NOT NULL,
    period VARCHAR(20),  -- 'day', 'week', 'month'
    
    power_score FLOAT,
    speed_score FLOAT,
    technique_score FLOAT,
    defense_score FLOAT,
    stamina_score FLOAT,
    footwork_score FLOAT,
    
    overall_score FLOAT,
    level INT,
    level_name VARCHAR(50),
    
    INDEX idx_user_date (user_id, assessment_date)
);

-- 專家影片表 (RAG)
CREATE TABLE expert_videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_url TEXT,
    athlete_name VARCHAR(100),
    skill_level VARCHAR(20),  -- 'pro', 'olympic', 'world_champion'
    action_type VARCHAR(50),
    key_points TEXT[],
    pinecone_vector_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API 設計

### RESTful API Endpoints

```yaml
# 影片管理
POST   /api/v1/videos/upload          # 上傳影片
GET    /api/v1/videos                 # 列出所有影片
GET    /api/v1/videos/{id}            # 取得單一影片資訊
DELETE /api/v1/videos/{id}            # 刪除影片
POST   /api/v1/videos/scan            # 掃描新影片 (手動觸發)

# 分析
POST   /api/v1/analyze/video/{id}     # 分析單一影片
GET    /api/v1/analyze/status/{id}    # 查詢分析狀態
GET    /api/v1/actions                # 列出所有動作
GET    /api/v1/actions/{id}           # 取得動作詳情 + 評估 + 建議

# 能力評估
GET    /api/v1/users/{id}/stats       # 取得六角圖數據
GET    /api/v1/users/{id}/level       # 取得當前等級
GET    /api/v1/users/{id}/progress    # 取得進度曲線

# 報表
GET    /api/v1/reports/daily          # 日報表
GET    /api/v1/reports/weekly         # 週報表
GET    /api/v1/reports/monthly        # 月報表
GET    /api/v1/reports/pdf            # 下載 PDF

# RAG
POST   /api/v1/rag/expert-videos      # 添加專家影片
GET    /api/v1/rag/similar            # 尋找相似動作

# WebSocket
WS     /ws/analysis/{video_id}        # 即時分析進度推送
```

### 請求/回應範例

```bash
# 上傳影片
POST /api/v1/videos/upload
Content-Type: multipart/form-data

file: video.mp4
training_date: 2025-11-02
training_type: 團課
location: 樂嫄運動空間

# 回應
{
  "video_id": "uuid",
  "status": "uploaded",
  "message": "影片已上傳,正在排隊分析"
}

---

# 取得動作詳情
GET /api/v1/actions/uuid

# 回應
{
  "id": "uuid",
  "video_id": "uuid",
  "action_type": "jab",
  "duration": 1.2,
  "quality_assessment": {
    "overall_score": 72,
    "breakdown": {
      "posture": 18,
      "trajectory": 14,
      "power_transfer": 15,
      "guard": 16,
      "speed": 19
    },
    "grade": "B",
    "problems": [
      {
        "type": "elbow_position",
        "severity": "medium",
        "description": "手肘外張約 15 度"
      }
    ]
  },
  "suggestions": {
    "analysis": "...",
    "improvements": [...],
    "drills": [...]
  },
  "visualization": {
    "skeleton_video_url": "https://...",
    "problem_frames": ["https://...", "https://..."],
    "comparison_video_url": "https://..."
  }
}
```

---

## 部署架構

### 開發環境
```
Local Machine
├── PostgreSQL (Docker)
├── Redis (Docker)
├── FastAPI (localhost:8000)
└── Next.js (localhost:3000)
```

### 生產環境 (AWS 範例)
```
AWS Cloud
├── EC2 (t3.xlarge)
│   ├── FastAPI + Gunicorn
│   ├── Celery Workers (影片處理)
│   └── Nginx (反向代理)
├── RDS PostgreSQL
├── ElastiCache Redis
├── S3 (影片儲存)
├── CloudFront (CDN)
└── Lambda (排程任務)
```

### Docker Compose 配置
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: boxtech
      POSTGRES_USER: boxtech
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./Midea:/app/media/videos
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://boxtech:secure_password@postgres:5432/boxtech
      REDIS_URL: redis://redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
  
  celery_worker:
    build: ./backend
    command: celery -A tasks worker --loglevel=info
    volumes:
      - ./backend:/app
      - ./Midea:/app/media/videos
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000

volumes:
  postgres_data:
```

---

## 效能優化策略

### 1. 影片處理優化
- 使用 GPU 加速 (CUDA) MediaPipe 推論
- 批次處理多支影片
- 降採樣: 30fps → 15fps (動作識別仍準確)
- 多進程並行處理

### 2. 資料庫優化
- 為常查詢欄位建立索引
- 使用 JSONB 的 GIN 索引
- 定期清理舊資料 (超過 1 年的原始姿態數據)
- 讀寫分離 (主從架構)

### 3. 快取策略
```python
# Redis 快取架構
cache_keys = {
    'user_stats:{user_id}:{period}': 3600,  # 1 小時
    'video_analysis:{video_id}': 86400,     # 1 天
    'hexagon_data:{user_id}': 1800,         # 30 分鐘
}
```

### 4. API 限流
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/videos/upload")
@limiter.limit("10/hour")  # 每小時最多上傳 10 支影片
async def upload_video():
    pass
```

---

## 安全性考量

### 1. 資料隱私
- 影片加密存儲 (AES-256)
- 資料庫連線使用 SSL
- 敏感資料遮罩 (日誌中不顯示完整檔案路徑)

### 2. 認證授權
- JWT Token 認證
- OAuth 2.0 (未來支援 Google/Facebook 登入)
- RBAC (角色權限控制)

### 3. API 安全
- HTTPS only
- CORS 設定
- Rate Limiting
- Input Validation

---

## 監控與日誌

### 監控指標
```yaml
系統健康:
  - CPU/記憶體使用率
  - 磁碟空間
  - 資料庫連線池狀態

業務指標:
  - 影片處理成功率
  - 平均處理時間
  - API 回應時間 (P50, P95, P99)
  - 錯誤率

用戶指標:
  - 每日活躍用戶 (DAU)
  - 每日上傳影片數
  - 功能使用率
```

### 日誌系統
```python
import logging
from pythonjsonlogger import jsonlogger

# 結構化日誌
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logger.info("Video processed", extra={
    'video_id': 'uuid',
    'duration': 120.5,
    'actions_detected': 45,
    'processing_time': 32.1
})
```

---

## 下一步: 開始實作

### 已完成任務 ✅

1. **設置開發環境** (Day 1 - 2025-11-03)
   - ✅ 安裝 Python 3.10+, Docker Desktop, Git
   - ✅ 建立虛擬環境
   - ✅ 安裝依賴套件 (requirements.txt)
   - ✅ 啟動 Docker 容器 (PostgreSQL, Redis, PGAdmin)
   - ✅ 配置環境變數 (.env)

### 立即開始的任務 (Day 2)

2. **建立專案骨架** (1 天)
   - 初始化 Git
   - 建立目錄結構
   - 設定 Docker Compose

3. **實作第一個功能: 影片掃描** (2-3 天)
   - 掃描 Midea 資料夾
   - 提取元數據
   - 存入資料庫

準備好開始了嗎?我可以幫您建立初始專案結構和第一個腳本!
