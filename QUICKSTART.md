# 🚀 BoxTech 快速開始指南

## 第一步: 環境準備 (10 分鐘)

### 1. 檢查系統需求

打開 PowerShell,檢查是否已安裝:

```powershell
# 檢查 Python 版本 (需要 3.10+)
python --version

# 檢查 Docker (需要安裝 Docker Desktop)
docker --version

# 檢查 Git
git --version
```

如果缺少任何工具:

- **Python**: https://www.python.org/downloads/
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/
- **Git**: https://git-scm.com/download/win

---

## 第二步: 初始化專案 (15 分鐘)

### 1. 運行專案設置腳本

```powershell
# 在 BoxTech 目錄下運行
cd c:\Users\user\source\BoxTech
python scripts\setup_project.py
```

這會自動建立所有必要的目錄和檔案。

### 2. 設置環境變數

```powershell
# 複製環境變數範例
Copy-Item .env.example .env

# 使用記事本編輯 .env
notepad .env
```

**必須設置的變數**:

```env
OPENAI_API_KEY=sk-your-key-here
```

其他變數可以保持預設值。

### 3. 建立虛擬環境

```powershell
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 如果遇到執行策略錯誤,運行:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. 安裝 Python 套件

```powershell
# 升級 pip
python -m pip install --upgrade pip

# 安裝所有依賴 (需要 5-10 分鐘)
pip install -r requirements.txt
```

**注意**: 安裝 TensorFlow 可能需要較長時間。

---

## 第三步: 啟動資料庫 (5 分鐘)

### 1. 啟動 Docker 容器

```powershell
# 啟動 PostgreSQL 和 Redis
docker-compose up -d postgres redis

# 檢查容器狀態
docker-compose ps
```

應該看到兩個容器在運行:

- `boxtech_postgres` (port 5432)
- `boxtech_redis` (port 6379)

### 2. 初始化資料庫

```powershell
# 若腳本已移至專案根目錄
python .\init_database.py
# 若仍在 scripts/ 目錄
python .\scripts\init_database.py
```

看到 "✅ Database tables created" 表示成功。

---

## 第四步: 測試系統 (10 分鐘)

### 1. 掃描現有影片

```powershell
# 若腳本已移至專案根目錄
python .\scan_videos.py
# 若仍在 scripts/ 目錄
python .\scripts\scan_videos.py
```

這會掃描 `Midea` 資料夾中的所有影片並記錄到資料庫。

預期輸出:

```
📹 Found 40+ video files
✅ Added: 20251102-團課-打靶 01.MOV
✅ Added: 20251102-團課-沙包(one two side).MOV
...
📊 Scan Summary:
   New videos: 40
   Duplicates: 0
   Errors: 0
```

### 2. 測試 MediaPipe

選擇一支影片測試姿態估計:

```powershell
# 若腳本已移至專案根目錄
python .\test_pose_estimation.py "Midea\拳擊基地\20250323-體驗課01.mp4"
# 若仍在 scripts/ 目錄
python .\scripts\test_pose_estimation.py "Midea\拳擊基地\20250323-體驗課01.mp4"
```

預期輸出:

```
📹 Processing: Midea\拳擊基地\20250323-體驗課01.mp4
📊 Video info: 3600 frames, 30 FPS
🔄 Processing frames...
  Frame 30/3600 - Detection rate: 95.0%
  Frame 60/3600 - Detection rate: 93.3%
...
✅ Processing completed!
   Detection rate: 92.5%
   ✅ Detection rate is good!
```

**如果偵測率低於 80%**:

- 檢查影片品質
- 確保人物在畫面中清晰可見
- 嘗試其他影片

---

## 第五步: 啟動後端 (5 分鐘)

### 1. 運行 FastAPI 伺服器

```powershell
# 從專案根目錄啟動（建議）
uvicorn backend.main:app --reload --port 8000

# 或傳統做法（進入 backend 再啟動）
cd backend
python main.py
```

### 2. 測試 API

打開瀏覽器訪問:

- API 首頁: [http://localhost:8000](http://localhost:8000)
- API 文檔: [http://localhost:8000/docs](http://localhost:8000/docs)
- 健康檢查: [http://localhost:8000/health](http://localhost:8000/health)
- v1 健康檢查: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- 列出影片: [http://localhost:8000/api/v1/videos](http://localhost:8000/api/v1/videos)

應該看到 Swagger UI 文檔介面。

---

## 🎯 第一天目標檢查清單

- [X] Python 3.10+ 已安裝
- [X] Docker Desktop 運行中
- [X] 虛擬環境已建立並啟動
- [X] 所有 Python 套件已安裝
- [X] PostgreSQL 和 Redis 容器運行中
- [X] 資料庫表格已建立
- [X] 掃描到 40+ 支影片
- [X] MediaPipe 測試成功 (偵測率 > 80%)
- [X] FastAPI 後端運行中
- [X] 可以訪問 API 文檔

---

## 🐛 常見問題排除

### 問題 1: 無法啟動虛擬環境

**錯誤**: `無法載入檔案...因為這個系統上已停用指令碼執行`

**解決**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 問題 2: pip 安裝套件失敗

**錯誤**: `error: Microsoft Visual C++ 14.0 or greater is required`

**解決**: 安裝 Visual Studio Build Tools

- 下載: https://visualstudio.microsoft.com/downloads/
- 選擇 "Desktop development with C++"

### 問題 3: Docker 容器無法啟動

**錯誤**: `Cannot connect to the Docker daemon`

**解決**:

1. 確保 Docker Desktop 已啟動
2. 檢查系統托盤是否有 Docker 圖示
3. 重新啟動 Docker Desktop

### 問題 4: 資料庫連線失敗

**錯誤**: `could not connect to server: Connection refused`

**解決**:

```powershell
# 檢查容器狀態
docker-compose ps

# 重啟容器
docker-compose restart postgres

# 查看容器日誌
docker-compose logs postgres
```

### 問題 5: MediaPipe 偵測率低

**原因**:

- 影片中人物太小或不清晰
- 背景雜亂
- 光線不足

**解決**:

- 選擇更清晰的影片測試
- 確保攝影角度能看到全身
- 改善訓練時的拍攝環境

### 問題 6: OpenCV 無法讀取影片

**錯誤**: `Cannot open video file`

**解決**:

```powershell
# 安裝 ffmpeg
# 使用 Chocolatey (Windows 套件管理器)
choco install ffmpeg

# 或從官網下載: https://ffmpeg.org/download.html
```

---

## 📊 驗證安裝成功

運行這個簡單的驗證腳本:

```powershell
python -c "
import cv2
import mediapipe
import fastapi
import sqlalchemy
import redis
print('✅ All core packages imported successfully!')
print(f'OpenCV: {cv2.__version__}')
print(f'MediaPipe: {mediapipe.__version__}')
print(f'FastAPI: {fastapi.__version__}')
print(f'SQLAlchemy: {sqlalchemy.__version__}')
"
```

---

## 🎉 恭喜!

如果所有步驟都完成了,您已經成功設置好 BoxTech 開發環境!

### 下一步:

1. **閱讀文檔**

   - 詳讀 `EXECUTION_PLAN.md` Week 2 的任務
   - 了解第一個功能的實作細節
2. **開始開發**

   - 實作第一個 API 端點
   - 處理一支完整的訓練影片
   - 提取姿態數據
3. **學習資源**

   - MediaPipe 文檔: https://google.github.io/mediapipe/
   - FastAPI 教學: https://fastapi.tiangolo.com/tutorial/
   - SQLAlchemy 文檔: https://docs.sqlalchemy.org/

---

## 💡 開發技巧

### 推薦的開發流程

1. **每天早上**:

   - 啟動虛擬環境
   - 啟動 Docker 容器
   - 運行 FastAPI 後端
2. **開發時**:

   - 使用 API 文檔測試端點 (http://localhost:8000/docs)
   - 頻繁 commit 代碼
   - 保持測試腳本可運行
3. **每天結束**:

   - 記錄今天完成的項目
   - 記錄遇到的問題和解決方案
   - 規劃明天的任務

### 推薦的 VS Code 插件

- Python (Microsoft)
- Pylance
- Docker
- PostgreSQL
- Thunder Client (API 測試)
- GitLens

---

## 📞 需要協助?

遇到問題時:

1. 檢查本文檔的「常見問題排除」章節
2. 查看相關技術的官方文檔
3. 搜尋錯誤訊息
4. 記錄問題和解決方案到專案文檔

---

**準備好開始開發了嗎? Let's build something amazing! 🚀🥊**
