from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import uvicorn

# 1. 初始化 App
app = FastAPI(title="Real AI Detector API")

# 2. 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextCheckRequest(BaseModel):
    text: str

# --- 全域載入模型 (App 啟動時執行) ---
print("正在初始化 AI 模型... (第一次執行會下載約 500MB，請耐心等待)")

# 我們使用全域變數來儲存模型，避免每次請求都重新載入
ai_model_pipe = None

try:
    # 這裡載入 HuggingFace 上的 "roberta-base-openai-detector"
    # 這是一個經典的 AI 檢測模型
    ai_model_pipe = pipeline("text-classification", model="roberta-base-openai-detector")
    print("✅ 模型載入完成！")
except Exception as e:
    print(f"❌ 模型載入失敗: {e}")
    print("請確認網路連線，或嘗試 pip install scipy")

# --- 真實 AI 檢測邏輯 ---
def real_ai_detection(text: str) -> dict:
    # 如果模型沒載入成功，回傳錯誤
    if not ai_model_pipe:
        return {"is_ai": False, "score": 0, "message": "Backend Error: Model not loaded"}
    
    # 截斷過長的文字 (模型通常限制 512 tokens)
    truncated_text = text[:512] 
    
    # 進行推論 (Inference)
    try:
        result = ai_model_pipe(truncated_text)
        # result 格式範例: [{'label': 'Fake', 'score': 0.99}]
        # 在這個模型中: 'Fake' = AI 生成, 'Real' = 人類
        
        label = result[0]['label']
        confidence = result[0]['score']
        
        # 邏輯轉換
        is_ai = (label == 'Fake')
        
        # 如果是 AI，分數就是信心分數；如果是人類，AI 分數就是 (1 - 信心分數)
        ai_probability = confidence if is_ai else (1.0 - confidence)
        
        final_score = round(ai_probability * 100, 1)
        
        # 設定回傳訊息
        if final_score > 50:
            message = "AI Content Detected"
        elif final_score < 20:
            message = "Likely Human Written"
        else:
            message = "Mixed / Uncertain"

        return {
            "is_ai": final_score > 50,
            "score": final_score,
            "message": message
        }
        
    except Exception as e:
        print(f"推論錯誤: {e}")
        return {"is_ai": False, "score": 0, "message": "Analysis Failed"}

@app.post("/api/detect")
async def detect_content(request: TextCheckRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # 呼叫真的 AI 函式
    result = real_ai_detection(request.text)
    return result

# 讓這個檔案可以直接用 python main.py 執行
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)