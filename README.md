# BoxTech - AI 拳擊訓練分析系統

## 📖 專案概述

BoxTech 是一個使用 AI 技術分析拳擊訓練影片的智能系統,能夠:

- 🎯 自動識別拳擊動作
- 📊 評估動作品質並檢測問題
- 🤖 提供 AI 教練建議
- 📈 追蹤訓練進度和能力成長
- 🎮 提供 3D 對戰模擬訓練

---

## 📚 文檔導覽

### 核心文檔

1. **[產品路線圖](./PRODUCT_ROADMAP.md)** - 完整的產品規劃、功能定義、里程碑
2. **[技術架構](./TECHNICAL_ARCHITECTURE.md)** - 系統架構、模組設計、API 設計
3. **[執行計劃](./EXECUTION_PLAN.md)** - 6 個月開發時程表、每週任務
4. **[README.md](./README.md)** (本文件) - 專案總覽和快速開始

### 閱讀順序建議

1. 先讀 `README.md` (本文件) 了解專案全貌
2. 詳讀 `PRODUCT_ROADMAP.md` 理解產品定位和功能
3. 研究 `TECHNICAL_ARCHITECTURE.md` 掌握技術細節
4. 依照 `EXECUTION_PLAN.md` 開始執行

---

## 🎯 MVP 核心功能

### Phase 1-2: 基礎分析 (前 3 個月)

- ✅ 影片自動掃描和管理
- ✅ MediaPipe 姿態估計
- ✅ 動作自動識別 (Jab, Cross, Hook, Uppercut, 泰拳踢)
- ✅ 動作品質評估
- ✅ AI 建議生成

### Phase 3: 進度追蹤 (第 4 個月)

- ✅ 六角圖能力分析
- ✅ 等級評價系統
- ✅ 日/週/月報表
- ✅ Web 前端儀表板

### Phase 4: 知識庫 (第 5 個月)

- ✅ 專家影片資料庫
- ✅ RAG 檢索增強
- ✅ 相似動作對比

### Phase 5: 遊戲化 (第 6 個月)

- ✅ Unity 3D 對戰模擬
- ✅ 5 等級 AI 對手
- ✅ 策略分析

---

## 🛠️ 技術棧

### 後端

- **語言**: Python 3.10+
- **框架**: FastAPI
- **資料庫**: PostgreSQL + Redis
- **任務隊列**: Celery
- **影片處理**: OpenCV + FFmpeg
- **姿態估計**: MediaPipe
- **機器學習**: TensorFlow / PyTorch
- **AI 服務**: OpenAI GPT-4

### 前端

- **框架**: Next.js 14 (React + TypeScript)
- **樣式**: TailwindCSS
- **圖表**: Chart.js / Recharts
- **影片**: Video.js

### 3D 模擬

- **引擎**: Unity 2022 LTS
- **部署**: Unity WebGL

### 資料存儲

- **影片**: 本地 + AWS S3
- **結構化**: PostgreSQL
- **向量資料**: Pinecone / Chroma

---

## 📦 專案結構

```
BoxTech/
├── backend/                    # FastAPI 後端
│   ├── api/                   # API 路由
│   │   ├── videos.py
│   │   ├── analysis.py
│   │   ├── users.py
│   │   └── reports.py
│   ├── services/              # 業務邏輯
│   │   ├── video_processor.py
│   │   ├── pose_estimator.py
│   │   ├── action_recognizer.py
│   │   ├── quality_assessor.py
│   │   ├── suggestion_generator.py
│   │   ├── rag_service.py
│   │   └── report_generator.py
│   ├── models/                # 資料庫模型
│   │   └── schemas.py
│   ├── database/              # 資料庫設定
│   │   └── connection.py
│   ├── tasks/                 # Celery 任務
│   │   └── video_tasks.py
│   ├── utils/                 # 工具函數
│   └── main.py                # 應用入口
├── frontend/                   # Next.js 前端
│   ├── app/                   # App Router
│   ├── components/            # React 元件
│   ├── lib/                   # 工具函數
│   └── public/                # 靜態資源
├── ml_models/                  # 機器學習模型
│   ├── action_classifier/     # 動作分類模型
│   ├── quality_model/         # 品質評估模型
│   └── training_scripts/      # 訓練腳本
├── unity/                      # Unity 3D 專案
│   └── BoxingSimulator/
├── scripts/                    # 工具腳本
│   ├── scan_videos.py         # 影片掃描
│   ├── init_database.py       # 資料庫初始化
│   └── process_batch.py       # 批次處理
├── Midea/                      # 影片資料夾
│   ├── LeYuan 樂嫄運動空間/
│   └── 拳擊基地/
├── docs/                       # 文檔
│   ├── PRODUCT_ROADMAP.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   └── EXECUTION_PLAN.md
├── tests/                      # 測試
├── docker-compose.yml          # Docker 配置
├── requirements.txt            # Python 依賴
├── .env.example               # 環境變數範例
├── .gitignore
└── README.md                   # 本文件
```

---

## 🚀 快速開始

### 前置需求

- Python 3.10 或以上
- Docker Desktop (用於 PostgreSQL 和 Redis)
- Node.js 18+ (用於前端開發)
- Git

### 1. 克隆專案

```bash
# 如果還沒有建立 Git Repository
cd c:\Users\user\source\BoxTech
git init
git add .
git commit -m "Initial commit: Project documentation"
```

### 2. 設置 Python 環境

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境 (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 安裝依賴
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 設置環境變數

```bash
# 複製範例配置
cp .env.example .env

# 編輯 .env 填入必要的 API Key
# OPENAI_API_KEY=your-key-here
# DATABASE_URL=postgresql://boxtech:password@localhost:5432/boxtech
# REDIS_URL=redis://localhost:6379
```

### 4. 啟動資料庫 (Docker)

```bash
# 啟動 PostgreSQL 和 Redis
docker-compose up -d postgres redis

# 初始化資料庫 (若腳本在根目錄)
python init_database.py
# 若仍在 scripts/ 目錄,請改用: python scripts/init_database.py

# 使用 Alembic 進行資料庫遷移（Day 3 起）
# 需先確認專案根目錄有 alembic.ini 與 alembic/ 目錄
# 升級到最新版本：
alembic upgrade head
# 如需回滾上一版（驗證用）：
alembic downgrade -1
```

### 5. 執行第一個測試

```bash
# 掃描現有影片 (若腳本在根目錄)
python scan_videos.py
# 若仍在 scripts/ 目錄,請改用: python scripts/scan_videos.py

# 處理一支測試影片 (若腳本在根目錄)
python test_pose_estimation.py Midea/拳擊基地/20250323-體驗課01.mp4
# 若仍在 scripts/ 目錄,請改用: python scripts/test_pose_estimation.py Midea/拳擊基地/20250323-體驗課01.mp4
```

### 6. 啟動開發伺服器

```bash
# 啟動 FastAPI 後端（建議做法，從專案根目錄）
uvicorn backend.main:app --reload --port 8000

# 啟動 Celery Worker (另一個終端)
celery -A tasks worker --loglevel=info

# 啟動前端 (另一個終端)
cd frontend
npm install
npm run dev
```

### 7. 訪問應用

- 後端 API: http://localhost:8000
- API 文檔: http://localhost:8000/docs
- 前端: http://localhost:3000

常用端點（v1）:

- GET /api/v1/health — 健康檢查
- GET /api/v1/videos — 影片列表（分頁/篩選/排序）
  - Query 參數：
    - limit (1-200，預設 50)、offset (>=0)
    - training_type、location、q（檔名片段）
    - date_from、date_to（YYYY-MM-DD）
    - order_by（upload_date|training_date|file_size_bytes|fps）、order_dir（asc|desc）
- GET /api/v1/videos/{id} — 影片詳情（包含 metadata）
- POST /api/v1/videos/scan — 觸發背景掃描
  - Body JSON：{"directory":"Midea","mode":"incremental|full"}

---

## 📊 開發狀態

### 已完成 ✅

- [X] 專案規劃文檔
- [X] 技術架構設計
- [X] 執行計劃制定
- [X] Day 0: 閱讀並批准所有規劃文檔 (2025-11-02)

### 進行中 🚧

- [X] Phase 0: 基礎建設 - 規劃完成 ✅
- [X] Day 1: 開發環境設置 (準備執行)
- [ ] Week 1: 影片管理系統基礎

### 待開始 📋

- [ ] Phase 1: 姿態分析 (Week 5-8)
- [ ] Phase 2: 品質評估 (Week 9-12)
- [ ] Phase 3: 報表系統 (Week 13-16)
- [ ] Phase 4: RAG 知識庫 (Week 17-20)
- [ ] Phase 5: 3D 對戰 (Week 21-28)

---

## 🎯 里程碑時間表

| 里程碑       | 預計完成 | 主要成果            |
| ------------ | -------- | ------------------- |
| **M0** | Week 4   | 基礎架構 + 影片管理 |
| **M1** | Week 8   | 動作識別系統        |
| **M2** | Week 12  | AI 建議系統         |
| **M3** | Week 16  | Alpha 版本 (自用)   |
| **M4** | Week 20  | Beta 版本 (封測)    |
| **M5** | Week 28  | 1.0 正式版          |

---

## 📈 當前優先級

### Day 3 完成 (2025-11-05) ✅

1. ✅ Alembic 初始化與遷移/索引建立（可升級/降級）
2. ✅ 影片掃描器：排除 .heic、大小寫安全副檔名過濾、full 模式支援
3. ✅ API 擴充：GET /api/v1/videos 支援分頁/篩選/排序；POST /api/v1/videos/scan 支援 mode
4. ✅ 新增掃描報告腳本 scripts/generate_scan_report.py（重複/異常報告）
5. ✅ 最小測試：tests/test_api_videos.py、tests/test_utils_parse_filename.py
6. ✅ 驗證腳本 scripts/verify_day3_api.py 通過四項檢查

### 下一步（Day 4：2025-11-11）

- 資料表/ORM 欄位再校準與索引微調（依查詢熱點）
- 擴充掃描報告欄位（影片長度分佈、FPS 異常閾值統計）
- 補齊更多 API 端點測試與錯誤處理
- 以 10 支影片做 E2E 規範檢驗（產出一份 Day 4 驗收小結）

### 本週目標 (Week 1)

1. ✅ 完成開發環境設置
2. ✅ 建立專案基礎結構 (初版)
3. ⏳ 測試核心技術棧 → 進一步完善
4. ⏳ 處理 10 支測試影片

---

## 🤝 貢獻指南

### Git Workflow

```bash
# 功能開發
git checkout -b feature/video-scanning
git add .
git commit -m "feat: implement video scanning script"
git push origin feature/video-scanning

# 修復 Bug
git checkout -b fix/pose-estimation-error
git commit -m "fix: correct coordinate transformation"
```

### Commit Message 規範

- `feat:` 新功能
- `fix:` 修復 Bug
- `docs:` 文檔更新
- `style:` 代碼格式
- `refactor:` 重構
- `test:` 測試
- `chore:` 維護任務

---

## 📝 開發日誌

### 2025-11-02 (Day 0)

**規劃階段完成** ✅

- ✅ 建立專案規劃文檔 (7 份核心文檔 + 3 份配置文件)
- ✅ 設計系統架構和技術選型
- ✅ 制定 6 個月 (28 週) 執行計劃
- ✅ 閱讀並批准所有規劃文檔
- ✅ 回應產品路線圖決策點:
  - **預算**: 初期以免費/本地方案為主,降低成本
  - **時程**: 無特定壓力,階段性展示給拳館
  - **技術**: Vibe Coding 為主,必要時 Coding
  - **部署**: 初期本地 Docker,穩定後上 Cloud
  - **隱私**: 影片可上傳雲端但需加密保護
- 📄 現有資源: 40+ 支訓練影片 (來自兩個拳館)
- 📋 更新文檔: DOCS_INDEX.md, EXECUTION_PLAN.md

**下一步**: Day 1 開始環境設置

### 2025-11-03 (Day 1)

**環境設置完成** ✅

- ✅ 環境確認 (Python 3.10+, Docker Desktop, Git)
- ✅ 電腦配置確認 (64GB RAM, RTX 3060, 188GB 可用空間)
- ✅ 專案初始化 (運行 setup_project.py)
- ✅ 環境變數配置 (OpenAI API Key)
- ✅ Docker 容器啟動 (PostgreSQL, Redis, PGAdmin)
- ✅ Python 虛擬環境建立
- ✅ 依賴套件安裝 (MediaPipe, FastAPI, OpenCV)
- 🐛 問題排除:
  - 套件版本衝突 → AI 輔助調整版本
  - PGAdmin email 配置 → 改用 .com 尾碼
- 📋 更新文檔: QUICKSTART.md, DAILY_REPORTS.md, EXECUTION_PLAN.md

**投入時間**: 1.5 小時
**下一步**: Day 2 初始化資料庫和測試 MediaPipe

### 2025-11-04 (Day 2)

**資料庫 + 視覺化 + 掃描完成** ✅

- ✅ 資料庫初始化 (新增/更新資料表、索引與約束)
- ✅ MediaPipe 測試 (33 關鍵點提取、視覺化輸出)
- ✅ 影片掃描 40+ 支並修正去重邏輯
- ✅ FastAPI 後端啟動與端點補齊 (`/`, `/health`, `/api/v1/health`, `/api/v1/videos`, `/api/v1/videos/{id}`, `/api/v1/videos/scan`)
- 🐛 問題排除:
  - 資料表缺失 → 新增 `pose_data`, `training_sessions`, `ability_assessments`
  - pgAdmin 不顯示 → 調整 compose 並手動新增伺服器
  - 腳本層級錯誤 → `init_database.py`, `scan_videos.py`, `test_pose_estimation.py` 上移至根目錄
  - `check_scan_results.py` 缺失 → 已新增
- 📋 更新文檔: DOCS_INDEX.md, PRODUCT_ROADMAP.md, EXECUTION_PLAN.md, PROJECT_SUMMARY.md, QUICKSTART.md, DAILY_REPORTS.md

**投入時間**: 3.5 小時  
**下一步**: Day 3 完善遷移、API 與測試

### 2025-11-05 (Day 3)

**遷移與 API 擴充完成** ✅

- ✅ Alembic 初始化並建立版本，驗證 upgrade/downgrade
- ✅ 影片掃描器：排除 .heic、大小寫安全副檔名過濾，支援 full 模式重新處理
- ✅ API：/api/v1/videos 加入分頁/篩選/排序；/api/v1/videos/scan 支援 mode
- ✅ 報告：scripts/generate_scan_report.py 產出 duplicates/anomalies/metadata 統計
- ✅ 測試：tests/test_api_videos.py、tests/test_utils_parse_filename.py
- ✅ 驗證：scripts/verify_day3_api.py 四項檢查通過

**投入時間**: 2.5 小時  
**下一步**: 11/11（Day 4）E2E 校準與報告細化

---

## 🐛 已知問題

目前無已知問題。

---

## 📞 聯絡資訊

- **專案負責人**: Lin Tsai
- **拳館合作**: 樂嫄運動空間、拳擊基地
- **技術諮詢**: GitHub Issues

---

## 📄 授權

本專案為個人專案,暫不開源。

---

## 🎉 致謝

- MediaPipe (Google) - 姿態估計技術
- OpenAI GPT-4 - AI 建議生成
- 拳擊教練們的專業指導
- 所有測試用戶的寶貴反饋

---

## 🔗 相關連結

- [MediaPipe Pose Documentation](https://google.github.io/mediapipe/solutions/pose.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Unity Documentation](https://docs.unity3d.com/)

---

**最後更新**: 2025-11-05
**版本**: 0.1.0-alpha
**狀態**: 規劃階段 → 準備開發

---

## 🚀 下一步

準備好開始了嗎?

```bash
# 執行初始化腳本
python scripts/setup_project.py

# 開始第一個任務
# 請查看 EXECUTION_PLAN.md Week 1 章節
```

讓我們開始這段激動人心的開發之旅! 💪🥊
