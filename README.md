🤖 AI Content Detector (AI 內容檢測器)

這是一個基於現代 Web 技術構建的 AI 內容檢測應用。它能夠分析使用者輸入的文字，並透過 HuggingFace 的 Transformer 模型判斷該內容是由 人類撰寫 還是由 AI (如 ChatGPT) 生成。

本專案採用 前後端分離 架構，前端使用 React 還原了精美的現代化 UI，後端則運行 FastAPI 並整合 PyTorch 進行即時推論。

🛠 技術堆疊 (Tech Stack)

Frontend (前端)

Framework: React (Vite)

Styling: Tailwind CSS (v3.4) - 用於快速構建響應式介面

Icons: Lucide React - 現代化圖示庫

HTTP Client: Axios - 處理 API 請求

Backend (後端)

Framework: FastAPI (Python) - 高效能的非同步 Web 框架

Server: Uvicorn - ASGI 伺服器

ML Core: PyTorch + Transformers (HuggingFace)

Model: roberta-base-openai-detector (RoBERTa) - 專門用於檢測生成式文本的模型

🚀 安裝與啟動 (Installation & Setup)

為了確保開發環境的乾淨與隔離，本專案嚴格使用虛擬環境。

1. 後端啟動 (Backend)

後端負責載入 AI 模型並處理檢測邏輯。

# 1. 進入專案根目錄

cd 5114056054_hw5

# 2. 建立與啟用虛擬環境 (Virtual Environment)

# macOS/Linux

python3 -m venv venv
source venv/bin/activate

# Windows

# python -m venv venv

# .\venv\Scripts\Activate

# 3. 安裝依賴套件

pip install -r requirements.txt

# (若無 requirements.txt，請執行: pip install fastapi uvicorn pydantic python-multipart torch transformers scipy)

# 4. 啟動伺服器

# 首次啟動會下載約 500MB 的模型檔案，請耐心等待直到出現 "Application startup complete"

uvicorn main:app --reload

後端服務位置：<http://127.0.0.1:8000>

2. 前端啟動 (Frontend)

前端負責提供使用者介面。

# 1. 開啟新的終端機視窗，進入 frontend 資料夾

cd frontend

# 2. 安裝依賴

npm install

# 3. 啟動開發伺服器

npm run dev

前端頁面位置：<http://localhost:5173>

🧪 正確測試指南 (Testing Guide)

⚠️ 重要：AI 模型的判斷準確度高度依賴於「輸入內容的長度」與「完整性」。
為了避免誤判，請遵循以下測試原則：

✅ 正確的測試方式 (Valid Scenarios)

測試人類文章：

請複製一段真實的新聞報導、學術論文摘要或維基百科內容。

長度建議： 至少 50 個英文單字 以上。

預期結果： 🟢 Likely Human Written

測試 AI 文章：

請使用 ChatGPT / Claude 生成一段文字（例如：Write a paragraph about the history of coffee）。

將生成的內容完整複製貼上。

預期結果： 🔴 AI Content Detected

❌ 容易導致誤判的情境 (Common Pitfalls)

字數過少 (Too Short)：

輸入："I am hungry" 或 "Hello world"。

原因： 模型缺乏足夠的語法特徵來判斷規律性，容易回傳不確定的中間值。

亂碼輸入 (Gibberish)：

輸入："asdfjkl;aljkdsf"。

原因： AI 模型通常不會生成無意義的亂碼，因此這類輸入通常會被判定為「非 AI (Likely Human)」，但這並無實際意義。

📊 數據結果解讀 (Result Interpretation)

系統會根據模型回傳的信心分數 (Probability Score)，將結果分類為三種狀態：

狀態 (Status)

顏色

分數區間

含義解釋

Likely Human Written

🟢 綠色

< 20%

極高機率為人類撰寫，文本缺乏機器生成的規律特徵。

Mixed / Uncertain

🟠 橘色

20% ~ 50%

不確定區域。通常發生在文本過短，或文章經過人類大幅潤飾與 AI 混合撰寫時。

AI Content Detected

🔴 紅色

> 50%

偵測到明顯的 AI 生成特徵（如過度工整的語法結構或特定的用詞頻率）。

📝 開發歷程與 Prompt 紀錄 (Development Process)

本專案是在資深程式設計師 (Archie) 的引導下，透過以下階段逐步迭代完成。

Phase 1: 環境建置與隔離 (Environment)

核心理念： 不污染全域環境，使用 venv 隔離依賴。

User Prompt: "因為你是一個資深工程師，所以在開發功能給程式前，請先給我一套指令來建立『虛擬環境 (venv)』並安裝 requirements.txt..."
Action: 建立了 Python 虛擬環境，並解決了 macOS zsh: command not found: python 的路徑問題。

Phase 2: 原型開發與 Mock 數據 (Prototyping)

核心理念： 優先打通前後端架構，邏輯暫時使用模擬數據 (Mock) 以加速 UI 開發。

User Prompt: "我想要做一個這樣的頁面然後加上符合該頁面的功能 (附圖)"
Action:

Backend: 使用 random.uniform() 建立模擬 API。

Frontend: 使用 React + Tailwind 還原設計稿 UI。

Issue Solved: 解決了 Tailwind CSS v4 版本衝突導致的紅字錯誤，降級至 v3 穩定版。

Phase 3: 真實 AI 模型整合 (Real Implementation)

核心理念： 將隨機的 Mock 邏輯替換為真實的機器學習模型。

User Prompt: "畫面中的字是我打得，這樣的數據正常嗎？... 那不需要(Mock)，但請在畫面上給我一個清空內容的按鈕及功能。"
Action:

引入 transformers 與 torch。

載入 roberta-base-openai-detector 模型。

Logic Upgrade: 從 random 升級為真實的 pipeline("text-classification")。

Feature: 新增了「清空內容 (Trash Icon)」功能。

📂 專案結構 (File Structure)

.
├── frontend/                # React 前端專案
│   ├── src/
│   │   ├── App.jsx          # 主應用程式邏輯 (UI + API整合)
│   │   ├── index.css        # Tailwind 樣式入口
│   │   └── main.jsx         # React 入口點
│   ├── tailwind.config.js   # Tailwind v3 設定檔
│   └── package.json         # 前端依賴清單
├── venv/                    # Python 虛擬環境 (由 git 忽略)
├── main.py                  # FastAPI 後端入口與 AI 檢測邏輯
├── requirements.txt         # 後端依賴清單
└── README.md                # 專案說明文件
