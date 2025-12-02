<!-- markdownlint-disable MD033 -->

<div align="center">

🤖 AI Content Detector

Next-Gen Text Analysis Powered by RoBERTa

<!-- Badges 徽章區：讓專案看起來更專業 -->

<br />

<!-- 專案簡介 -->

<p align="center">
<b>拒絕隨機瞎猜，使用真實 Transformer 模型進行推論。</b>




這是一個全端 AI 檢測應用，能夠分析文本規律，精準判斷內容是由人類撰寫還是 AI 生成。




已針對 <b>Streamlit Cloud</b> 進行優化，並內建強制亮色主題 (Force Light Theme)。
</p>

<!-- 🔴 重要：建議將你的網頁截圖命名為 demo.png 放根目錄，並將下方連結換成 ./demo.png -->

</div>

⚡️ 主要功能 (Features)

🕵️‍♂️ 真實 AI 核心： 整合 roberta-base-openai-detector 模型，非隨機數生成。

🚀 一鍵部署： 支援 Streamlit 架構，輕鬆部署至雲端。

🎨 現代化介面： 透過 CSS Injection 強制亮色卡片風格，解決深色模式下的閱讀問題。

⚠️ 智慧提示： 自動偵測字數過少的輸入並給予準確度警告。

🗑️ 智慧清空： 內建一鍵重置功能，優化測試體驗。

🛠 技術堆疊 (Tech Stack)

Component

Technology

Description

Frontend UI

Streamlit

Python 驅動的快速 Web 框架 (Custom CSS Enhanced)

Backend Logic

Python

處理核心邏輯與運算

Model Engine

PyTorch

深度學習計算框架

AI Model

Transformers

HuggingFace 預訓練模型載入器

Algorithm

RoBERTa

Robustly Optimized BERT Approach

🚀 快速啟動 (Quick Start)

1. 本地執行 (Local Development)

# 1. Clone 專案並進入目錄
git clone <your-repo-url>
cd <your-repo-folder>

# 2. 建立虛擬環境 (強烈建議)
python3 -m venv venv
source venv/bin/activate

# 3. 安裝依賴 (包含 AI 核心庫)
pip install -r requirements.txt

# 4. 啟動應用
streamlit run app.py


2. 雲端部署 (Streamlit Cloud)

本專案已針對 Streamlit Community Cloud 進行優化。
只需將本專案 (app.py 與 requirements.txt) 推送到 GitHub，並在 Streamlit Cloud 選擇 app.py 作為入口檔案即可。

Note: 首次啟動需下載約 500MB 模型檔案，請耐心等待 1-3 分鐘。

🧪 測試指南 (Testing Guide)

為了獲得最準確的檢測結果，請參考下表進行測試：

測試情境 (Scenario)

輸入範例 (Example)

預期結果 (Expected)

人類文章 🟢

複製一段真實新聞或 Wiki (50字以上)

Likely Human (<20%)

AI 生成 🔴

複製 ChatGPT 生成的長文

AI Detected (>50%)

過短/亂碼 🟠

"Hello" 或 "asdfg"

Uncertain / Human (附帶警告提示)

🔍 結果判讀

🔴 AI Content Detected: 模型發現了高度規律的語法結構。

🟠 Mixed / Uncertain: 文本特徵不明顯，可能是混合寫作或字數太少 (<50字)。

🟢 Likely Human Written: 文本充滿了人類特有的不規則性與創造性。

📝 開發歷程 (Development Journey)


<details>
<summary><b>點擊展開完整開發紀錄</b></summary>

Phase 1: Environment Setup 🏗️

Goal: 建立隔離且乾淨的 Python venv 環境。

Action: 解決了環境變數與路徑衝突問題，確保 python 指令正確指向虛擬環境。

Phase 2: Mock Prototype 🧪

Goal: 快速驗證前後端分離架構 (React + FastAPI)。

Action: 使用 random 模擬檢測數據，優先完成前端 UI 切版與互動邏輯。

Phase 3: Real AI Integration 🧠

Goal: 導入真實機器學習模型與 Streamlit 遷移。

Action:

引入 transformers 與 torch。

載入 roberta-base-openai-detector。

UI Polish: 透過 CSS 強制還原 React 版本的白色卡片風格，解決 Streamlit 預設 Dark Mode 的視覺問題。

UX Upgrade: 加入字數過少 (Low Perplexity) 的防呆提示。

</details>

<div align="center">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</div>