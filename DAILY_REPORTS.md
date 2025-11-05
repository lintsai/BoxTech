# BoxTech 開發日誌

此文件記錄專案的每日進度、決策和問題。

---

## Day 0 報告 (2025-11-02)

### 📋 執行摘要

**階段**: 專案規劃與文檔審查
**狀態**: ✅ 完成
**投入時間**: 約 6 小時 (閱讀與批准)

---

### ✅ 已完成項目

#### 1. 文檔閱讀與理解

- [X] **README.md** - 專案總覽和導航
- [X] **PROJECT_SUMMARY.md** - 專案總結 (以此為中心展開閱讀)
- [X] **PRODUCT_ROADMAP.md** - 產品路線圖 (完整閱讀)
- [X] **TECHNICAL_ARCHITECTURE.md** - 技術架構 (詳細研究)
- [X] **EXECUTION_PLAN.md** - 執行計劃 (Week 1-4 重點)
- [X] **QUICKSTART.md** - 快速開始指南 (閱讀完畢,尚未執行)
- [X] **DOCS_INDEX.md** - 文檔索引

#### 2. 決策點回應 (PRODUCT_ROADMAP.md)

已回應 5 個關鍵決策點:

1. **預算上限**:

   - 決策: 初期規劃偏高,因無營利,會盡量使用免費或本地版本
   - 影響: 優先使用 MediaPipe (免費)、本地 PostgreSQL、減少 GPT-4 呼叫
2. **上線時間壓力**:

   - 決策: 沒有特別壓力,希望有階段性展示,可慢慢與拳館討論
   - 影響: 可以穩健開發,重質量而非速度
3. **技術偏好**:

   - 決策: 都可以,以 Vibe Coding 為主
   - 影響: AI 輔助開發為主,必要時手動 Coding
4. **部署環境**:

   - 決策: 初期本地 Docker,穩定上線後用 Cloud 服務
   - 影響: Week 1-16 專注本地開發,之後再考慮雲端部署
5. **隱私考量**:

   - 決策: 影片可上傳雲端,但要保護起來
   - 影響: 需實作加密存儲和訪問控制

#### 3. 批准簽核 (PRODUCT_ROADMAP.md)

- [X] 產品負責人確認需求
- [X] 技術負責人確認可行性
- [X] 預算負責人確認成本
- [X] 開始執行 Phase 0

#### 4. 文檔更新

- [X] **EXECUTION_PLAN.md**:

  - 更新 "立即行動" 章節
  - 改為 Day 0/1/2 格式 (更清晰)
  - 標記 Day 0 已完成
- [X] **DOCS_INDEX.md**:

  - 更新 "第一次閱讀" 檢查清單 (已完成項目)
  - 更新 "文檔檢查清單" (產品、技術、執行層面)
  - 新增版本記錄 v1.1

---

### 📊 理解確認

#### 產品層面 ✅

- ✅ **問題定義**: 拳擊訓練缺乏量化分析和個人化建議
- ✅ **目標用戶**: 拳擊學員 (自己) → 拳館學員 → 教練
- ✅ **核心功能**:
  - 影片分析 + 動作識別
  - AI 建議 + 品質評估
  - 進度追蹤 + 能力評級
  - RAG 知識庫 + 3D 對戰
- ✅ **開發時程**: 6-7 個月 (28 週)

#### 技術層面 ✅

- ✅ **系統架構**:

  - 前端: Next.js + React
  - 後端: FastAPI + PostgreSQL + Redis + Celery
  - AI: MediaPipe + GPT-4 + TensorFlow
  - 3D: Unity WebGL
- ✅ **核心模組**:

  1. 影片處理模組
  2. 姿態估計模組 (MediaPipe)
  3. 動作識別模組 (LSTM)
  4. 品質評估模組
  5. AI 建議生成模組 (GPT-4)
  6. RAG 知識庫模組 (Pinecone)
  7. 能力評估模組 (六角圖)
  8. 報表生成模組
- ✅ **資料庫設計**: 理解 7 個主要資料表結構
- ✅ **API 設計**: RESTful API 端點規劃

#### 執行層面 ✅

- ✅ **Week 1 任務**: 環境設置 + 專案初始化
- ✅ **環境設置步驟**: 已閱讀 QUICKSTART.md (Day 1 執行)
- ✅ **測試方法**: 理解如何測試各模組
- ✅ **問題排除**: 已知常見問題和解決方案

---

### 💡 關鍵洞察

1. **專案規模適中**:

   - 6 個月時程合理
   - 功能循序漸進
   - 可彈性調整
2. **技術選型務實**:

   - MediaPipe 免費且高效
   - GPT-4 可用建議模板庫降低成本
   - 本地開發降低初期投入
3. **階段性交付**:

   - M1 (Week 8): 動作識別 - 可展示基礎功能
   - M3 (Week 16): Alpha 版 - 自己可完整使用
   - M5 (Week 28): 1.0 版 - 對外公開
4. **現有資源豐富**:

   - 40+ 支訓練影片是寶貴資產
   - 兩個拳館的多樣性有助模型訓練
   - 教練示範影片可作為標準參考

---

### 📝 決策記錄

| 決策項目 | 決策內容              | 理由              |
| -------- | --------------------- | ----------------- |
| 成本控制 | 初期使用免費/本地方案 | 無營利,控制成本   |
| 開發節奏 | 穩健開發,階段展示     | 無時間壓力,重質量 |
| 開發模式 | Vibe Coding 為主      | 提高開發效率      |
| 部署策略 | 先本地後雲端          | 降低初期複雜度    |
| 資料安全 | 加密存儲和訪問控制    | 保護隱私          |

---

### 🎯 下一步行動

#### Day 1 計劃 (預計執行項目)

1. **環境檢查** (30 分鐘)

   - [X] 確認 Python 3.10+ 已安裝
   - [X] 確認 Docker Desktop 已安裝
   - [X] 確認 Git 已安裝
   - [X] 確認 VS Code 已安裝
2. **專案初始化** (1 小時)

   - [X] 建立 Git Repository
   - [X] 運行 `python scripts/setup_project.py`
   - [X] 檢視生成的目錄結構
3. **環境設定** (1 小時)

   - [X] 複製 `.env.example` 到 `.env`
   - [X] 填入必要設定 (OPENAI_API_KEY 等)
   - [X] 建立虛擬環境
4. **套件安裝** (1-2 小時)

   - [X] 啟動虛擬環境
   - [X] `pip install -r requirements.txt`
   - [X] 驗證安裝成功
5. **驗證** (30 分鐘)

   - [X] 運行驗證腳本
   - [X] 確認所有套件可正常 import

#### Day 2 計劃 (預計執行項目)

1. **資料庫設置** (1 小時)

   - [X] `docker-compose up -d`
   - [X] `python scripts/init_database.py`
   - [X] 檢視資料表
2. **影片處理測試** (2 小時)

   - [X] 測試 MediaPipe 處理一支影片
   - [X] 掃描現有 40+ 支影片
   - [X] 檢視掃描結果
3. **API 測試** (1 小時)

   - [X] 啟動 FastAPI 後端
   - [X] 訪問 API 文檔
   - [X] 測試基礎端點

---

### 📚 參考文檔

- [EXECUTION_PLAN.md](./EXECUTION_PLAN.md) - Day 1/2 詳細步驟
- [QUICKSTART.md](./QUICKSTART.md) - 環境設置指南
- [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) - 技術細節

---

### 💭 問題與思考

#### 記錄的問題

- 無

#### 待確認事項

1. OpenAI API Key 是否已準備好?
2. 電腦配置是否符合需求? (特別是記憶體和 GPU)
3. 是否需要先測試一支影片確認 MediaPipe 效果?

#### 改進想法

- 考慮在 Week 2-3 就先處理幾支影片,早期驗證技術可行性
- 建議每週五寫一份週報,記錄進度和學習
- 可以建立一個 Notion 或 Trello 看板,視覺化追蹤進度

---

### 📊 時間統計

- **文檔閱讀**: 約 4 小時
- **決策討論**: 約 1 小時
- **文檔更新**: 約 1 小時
- **總計**: 約 6 小時

---

### ✅ Day 0 完成檢查清單

- [X] 閱讀所有核心規劃文檔
- [X] 理解產品定位和核心價值
- [X] 理解技術架構和模組設計
- [X] 理解執行計劃和時程安排
- [X] 回應所有決策點問題
- [X] 批准專案啟動
- [X] 更新相關文檔
- [X] 規劃 Day 1/2 行動項

---

**報告人**: 專案負責人
**日期**: 2025-11-02
**下次報告**: Day 1 完成後 (預計 2025-11-03)

---

## Day 1 報告 (2025-11-03)

### 📋 執行摘要

**階段**: 專案初始 + 環境設定及安裝
**狀態**: ✅ 完成
**投入時間**: 1.5 小時

---

### ✅ 已完成項目

#### 1. 環境確認與工具安裝

- [X] 確認 Python 3.10+ 已安裝
- [X] 確認 Docker Desktop 已安裝
- [X] 確認 Git 已安裝
- [X] 電腦配置確認:
  - 記憶體: 64GB
  - GPU: RTX 3060
  - 硬碟空間: 1TB (剩餘 188GB)

#### 2. 專案初始化

- [X] 建立 Git Repository
- [X] 運行 `python scripts/setup_project.py` 建立專案結構
- [X] 檢視生成的目錄結構

#### 3. 環境配置

- [X] 複製 `.env.example` 到 `.env`
- [X] 填入 OpenAI API Key
- [X] 填入必要配置 (資料庫連線等)

#### 4. Docker 環境設置

- [X] 啟動 Docker Compose 服務:
  - PostgreSQL (資料庫)
  - Redis (任務隊列)
  - PGAdmin (資料庫管理工具)

#### 5. Python 套件安裝

- [X] 建立虛擬環境
- [X] 安裝 requirements.txt 依賴套件
- [X] 驗證核心套件安裝成功:
  - MediaPipe ✅
  - FastAPI ✅
  - OpenCV ✅

#### 6. 文檔更新

- [X] **QUICKSTART.md**: 標記 "第一天目標檢查清單" 已完成項目
- [X] **DAILY_REPORTS.md**: 新增 Day 1 報告
- [X] **EXECUTION_PLAN.md**: 更新 Week 1 任務完成狀態
- [X] **DOCS_INDEX.md**: 更新文檔版本和完成狀態
- [X] **PROJECT_SUMMARY.md**: 更新專案進度

---

### 🚧 進行中項目

- 無,按照計劃執行中

---

### ❌ 遇到的問題

#### 問題 1: requirements.txt 套件版本衝突

- **問題描述**: 部分套件版本不相容導致安裝失敗
- **解決方案**: 使用 AI 調整套件版本,確保相容性
- **狀態**: ✅ 已解決
- **學習**: 套件版本管理很重要,未來可能需要使用 Poetry 或 pipenv

#### 問題 2: Docker PGAdmin4 啟動失敗

- **問題描述**: PGAdmin 容器無法啟動
- **根本原因**: Email 配置使用 `.local` 尾碼不被接受
- **解決方案**: 將 email 尾碼改為 `.com`
- **狀態**: ✅ 已解決
- **修改位置**: `docker-compose.yml` 中的 `PGADMIN_DEFAULT_EMAIL`

---

### 💡 學習與洞察

1. **環境設置比想像中順利**:

   - 大部分工具已安裝,只需要配置
   - Docker 大幅簡化資料庫設置
2. **套件管理需要注意**:

   - 不同套件的依賴版本可能衝突
   - AI 輔助調整版本很有效率
3. **硬體配置充足**:

   - 64GB RAM 對影片處理很有幫助
   - RTX 3060 可支援 TensorFlow GPU 加速
   - 硬碟空間需要注意 (188GB 剩餘,需要定期清理)

---

### 📝 決策記錄

#### 問題 1: OpenAI API Key 是否已準備好?

- **決策**: 是,已經更新到 `.env` 檔案
- **用途**: GPT-4 建議生成 (Phase 2)

#### 問題 2: 電腦配置如何?

- **記憶體**: 64GB (充足,可同時運行多個服務)
- **GPU**: RTX 3060 (支援 CUDA,可加速模型訓練)
- **硬碟空間**: 1TB (剩餘 188GB,需要監控)
- **評估**: 配置良好,滿足開發需求

#### 問題 3: 是否先測試一支影片?

- **決策**: 可以,按照計劃在 Day 2 進行
- **理由**: Day 1 專注環境設置,Day 2 開始實際測試

---

### 🎯 下一步行動

#### Day 2 計劃 (明日執行)

1. **資料庫初始化** (30 分鐘)

   - [X] 運行 `python scripts/init_database.py`
   - [X] 檢查資料表是否正確建立
   - [X] 使用 PGAdmin 查看資料庫結構
2. **MediaPipe 測試** (1 小時)

   - [X] 運行 `python scripts/test_pose_estimation.py`
   - [X] 選擇一支測試影片
   - [X] 驗證姿態估計效果
   - [X] 檢視關鍵點數據
3. **影片掃描測試** (1 小時)

   - [X] 運行 `python scripts/scan_videos.py`
   - [X] 掃描 40+ 支現有影片
   - [X] 檢視掃描結果和元數據
   - [X] 驗證去重功能
4. **API 服務啟動** (30 分鐘)

   - [X] 啟動 FastAPI 後端
   - [X] 訪問 Swagger API 文檔
   - [X] 測試基礎端點

---

### 📊 時間統計

- **環境檢查與工具確認**: 0.5 小時
- **專案初始化與 Docker 設置**: 0.5 小時
- **套件安裝與問題排除**: 0.5 小時
- **文檔更新**: 0.5 小時 (包含本報告)
- **總計**: 2 小時

> **Note**: 實際投入 1.5 小時,比預期稍快 (因為環境已大部分就緒)

---

### ✅ Day 1 完成檢查清單

- [X] Python 3.10+ 確認
- [X] Docker Desktop 確認
- [X] Git 確認
- [X] 專案結構建立
- [X] 環境變數配置
- [X] Docker 容器啟動
- [X] Python 虛擬環境建立
- [X] 依賴套件安裝
- [X] 核心套件驗證 (MediaPipe, FastAPI, OpenCV)
- [X] 文檔更新

---

### 📚 參考文檔

- [EXECUTION_PLAN.md](./EXECUTION_PLAN.md) - Week 1 詳細任務
- [QUICKSTART.md](./QUICKSTART.md) - 環境設置步驟
- [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) - 系統架構參考

---

**報告人**: Lin Tsai
**日期**: 2025-11-03
**下次報告**: Day 2 完成後 (預計 2025-11-04)

---

## Day 2 報告 (2025-11-04)

### 📋 執行摘要

**階段**: 資料庫初始化 + MediaPipe 測試 + 影片掃描  
**狀態**: ✅ 完成  
**投入時間**: 3.5 小時

---

### ✅ 已完成項目

1. 資料庫初始化完成 (新增/更新資料表、索引與約束)
2. MediaPipe 姿態估計測試通過 (33 關鍵點提取、視覺化輸出)
3. 影片掃描測試完成 (掃描 40+ 支影片、元數據提取、Hash 去重修正)
4. FastAPI 後端啟動與測試完成 (健康檢查與影片端點)
5. 新增驗證腳本: `pose_extract_and_visualize.py` (MediaPipe 視覺化)
6. 文檔同步更新: DOCS_INDEX、PRODUCT_ROADMAP、README、DAILY_REPORTS、EXECUTION_PLAN、PROJECT_SUMMARY、QUICKSTART

---

### 🚧 進行中項目

- 無, 依計劃執行

---

### ❌ 遇到的問題與解決

1) 缺少資料表: `pose_data`, `training_sessions`, `ability_assessments`
   - 解決: 透過 AI 協助補充/更新資料表設計與建立
   - 狀態: ✅ 已解決

2) pgAdmin 無法顯示資料庫資訊
   - 解決: 調整 `docker-compose.yml` 設定並於 pgAdmin 手動新增伺服器
   - 狀態: ✅ 已解決

3) 腳本路徑層級不正確 (多了一層 `scripts/`)
   - 檔案: `init_database.py`, `scan_videos.py`, `test_pose_estimation.py`
   - 解決: 將三個檔案上移至專案根目錄
   - 狀態: ✅ 已解決

4) 掃描重複判定邏輯誤判
   - 解決: 修正掃描邏輯 (Hash/Metadata 去重流程)
   - 狀態: ✅ 已解決

5) 缺少 `check_scan_results.py` 腳本
   - 症狀: 執行 `python scripts/check_scan_results.py` 找不到檔案
   - 解決: 生成腳本後問題排除
   - 狀態: ✅ 已解決

6) API 端點缺失
   - 缺少端點: `/api/v1/videos`, `/api/v1/videos/{id}`, `/api/v1/videos/scan`
   - 解決: 依規劃新增端點 (目前 `/` 與 `/health` 亦可用)
   - 狀態: ✅ 已解決

7) `test_pose_estimation.py` 使用方式錯誤
   - 症狀: 未提供 `video_path` 導致用法提示
   - 解決: 修正程式碼與使用方式, 依參數運行
   - 狀態: ✅ 已解決

---

### 💡 學習與洞察

- 目前皆在熟悉範圍內, 依計劃推進

---

### 📝 決策記錄

- 本日無新增決策

---

### 🎯 下一步行動 (Day 3 概要)

1. 完善資料庫遷移與模型同步 (補齊欄位/索引)
2. 完整化掃描器的 Metadata Parser 與去重報告
3. 擴充 API: `GET /api/v1/videos` 支援篩選/分頁, `POST /api/v1/videos/scan` 增加參數
4. 撰寫基本單元測試 (影片掃描與 API)
5. 挑選 10 支影片進行標準化處理 (建立 Day 3 驗收標準)

---

### 📊 時間統計

- 開發: 1.5 小時  
- 測試: 1 小時  
- 文檔: 1 小時  
- 總計: 3.5 小時

---

### ✅ 檢查清單

- [X] 7 個資料表建立成功  
- [X] 索引和約束設置完成  
- [X] 測試資料插入成功  
- [X] 驗證 MediaPipe 可正確載入影片  
- [X] 提取 33 個身體關鍵點  
- [X] 生成姿態估計視覺化影片  
- [X] 驗證關鍵點準確度  
- [X] 成功掃描 40+ 支影片  
- [X] 元數據正確提取 (時長、解析度、fps)  
- [X] 檔案 hash 計算完成  
- [X] 去重邏輯運作正常  
- [X] 資料寫入資料庫  
- [X] 所有端點回應正常  
- [X] Swagger UI 可正常訪問  
- [X] 資料庫查詢無錯誤

---

**報告人**: Lin Tsai  
**日期**: 2025-11-04  
**下次報告**: 2025-11-05

---

## 報告模板 (供未來使用)

```markdown
## Day X 報告 (YYYY-MM-DD)

### 📋 執行摘要
**階段**: 
**狀態**: 
**投入時間**: 

### ✅ 已完成項目
1. 
2. 

### 🚧 進行中項目
1. 
2. 

### ❌ 遇到的問題
1. **問題**: 
   **解決方案**: 
   **狀態**: 

### 💡 學習與洞察
1. 
2. 

### 📝 決策記錄
| 決策項目 | 決策內容 | 理由 |
|---------|---------|------|
|         |         |      |

### 🎯 下一步行動
1. 
2. 

### 📊 時間統計
- **開發**: X 小時
- **測試**: X 小時
- **文檔**: X 小時
- **總計**: X 小時

### ✅ 檢查清單
- [ ] 
- [ ] 

**報告人**: 
**日期**: 
**下次報告**: 
```

---
 
## Day 3 報告 (2025-11-05)

### 📋 執行摘要

**階段**: API功能及基礎設施開發中
**狀態**: 完成
**投入時間**: 2.5 Hour

### ✅ 已完成項目

1. 完成 資料庫：遷移與索引，使用 Alembic 初始化
2. 新增掃描報告腳本，generate_scan_report.py
3. scan_videos.py 移除 “.heic”，避免把圖片當影片索引（改為允許 .mp4/.mov/.avi 並以副檔名小寫判斷）
4. API 擴充：篩選、排序、分頁，在 GET /api/v1/videos 加入篩選與排序；POST /api/v1/videos/scan 支援 mode（incremental/full）
5. 完成最小測試（API + utils）: tests/test_api_videos.py & tests/test_utils_parse_filename.py
6. 新增 verify_day3_api.py 驗證腳本，並驗證以下四項皆通過：
   - ✅ 資料庫遷移可反覆執行（head ↔ downgrade）
   - ✅ 影片掃描有重複/異常報告（可追蹤原因）
   - ✅ API videos 列表可分頁、詳情正確呈現 metadata
   - ✅ 10 支影片全流程通過（掃描 → 寫庫 → API 查）

### 🚧 進行中項目

1. 無, 依照計劃

### ❌ 遇到的問題

1. 問題: 修正服務啟動錯誤
   (venv) PS C:\Users\user\source\BoxTech> uvicorn main:app --reload --host 0.0.0.0 --port 8000
   INFO:     Will watch for changes in these directories: ['C:\\Users\\user\\source\\BoxTech']
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [61836] using WatchFiles
   ERROR:    Error loading ASGI app. Could not import module "main".
   解決方案: 透過 AI 進行程式碼修正（改用 backend.main:app 啟動）
   狀態: 已解決

### 💡 學習與洞察

1. 學習 Alembic 的使用方式（初始化、產生版本、升降級流程）

### 📝 決策記錄

1. 無

### 🎯 下一步行動

1. 依照計劃（下次 Day 4 於 11/11）

### 📊 時間統計

- 開發: 1 小時
- 測試: 1 小時
- 文檔: 0.5 小時
- 總計: 2.5 小時

### ✅ 檢查清單

✅ 資料庫遷移可反覆執行（head ↔ downgrade）
✅ 影片掃描有重複/異常報告（可追蹤原因）
✅ API videos 列表可分頁、詳情正確呈現 metadata
✅ 10 支影片全流程通過（掃描 → 寫庫 → API 查）

**報告人**: Lin Tsai
**日期**: 2025-11-05
**下次報告**: 2025-11-11 (中間時間有事情休息一下，Day 4 會是 11/11)

---

**文檔建立**: 2025-11-02
**最後更新**: 2025-11-05
**版本**: 1.3
