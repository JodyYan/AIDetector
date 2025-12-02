import streamlit as st
from transformers import pipeline

# 1. 頁面基礎設定
st.set_page_config(
    page_title="AI Detector by JustDone",
    page_icon="🤖",
    layout="centered"
)

# 自訂 CSS 讓介面更像原本的 React 版本
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        background-color: #F4F6F8;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 載入 AI 模型 (快取機制)
# @st.cache_resource 確保模型只會下載/載入一次，不會因為每次按按鈕就重跑
@st.cache_resource
def load_model():
    # 使用與 FastAPI 版本相同的 RoBERTa 模型
    return pipeline("text-classification", model="roberta-base-openai-detector")

# 3. 介面標題區
st.markdown("<div class='main-header'><h1>🤖 AI Detector by JustDone</h1><p>Maintain the authenticity of your writing by identifying AI-generated content.</p></div>", unsafe_allow_html=True)

# 4. 文字輸入區
user_input = st.text_area(
    "Enter text to analyze:", 
    height=250,
    placeholder="Paste your text here to check if it's written by AI...",
    help="For best results, enter at least 50 words."
)

# 建立兩欄佈局 (用來放按鈕)
col1, col2 = st.columns([1, 4])

with col1:
    check_button = st.button("Check for AI Content", type="primary", use_container_width=True)

# 5. 觸發檢測邏輯
if check_button:
    if not user_input or len(user_input.strip()) == 0:
        st.warning("⚠️ Please enter some text first.")
    elif len(user_input.strip()) < 20:
        st.warning("⚠️ Text is too short for accurate analysis. Please enter at least 20 characters.")
    else:
        with st.spinner("Analyzing patterns... (Loading model might take time on first run)"):
            try:
                # 載入模型
                pipe = load_model()
                
                # 執行推論 (限制 512 tokens 以防報錯)
                # RoBERTa 的限制通常是 512 tokens
                result = pipe(user_input[:512]) 
                
                # 解析結果: result = [{'label': 'Fake', 'score': 0.99}]
                label = result[0]['label'] # 'Fake' (AI) or 'Real' (Human)
                score = result[0]['score']
                
                # 轉換邏輯
                is_ai = (label == 'Fake')
                # 如果是 AI，分數即為 confidence；如果是 Human，AI 分數為 1 - confidence
                ai_probability = score if is_ai else (1.0 - score)
                
                # 轉成百分比
                final_score = round(ai_probability * 100, 1)
                
                st.divider() # 分隔線
                
                # 6. 顯示結果 (依照原本 README 的定義)
                col_res1, col_res2 = st.columns([2, 1])
                
                with col_res1:
                    if final_score > 50:
                        st.error(f"🚨 **AI Content Detected**")
                        st.write(f"Confidence: **{final_score}%**")
                        st.write("The analysis indicates this text likely contains AI-generated patterns.")
                    elif final_score < 20:
                        st.success(f"✅ **Likely Human Written**")
                        st.write(f"AI Probability: **{final_score}%** (Very Low)")
                        st.write("This text appears to be authentic and human-written.")
                    else:
                        st.warning(f"🟠 **Mixed / Uncertain**")
                        st.write(f"AI Probability: **{final_score}%**")
                        st.write("The text characteristics are ambiguous. It might be heavily edited or too short.")
                
                with col_res2:
                    # 顯示進度條視覺化
                    st.write("AI Probability Score:")
                    st.progress(final_score / 100)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# 頁尾資訊
st.markdown("---")
st.caption("Powered by HuggingFace Transformers & RoBERTa Model | Built with Streamlit")