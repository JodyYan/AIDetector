import streamlit as st

# --- 關鍵修正：頁面設定必須放在最第一行 ---
st.set_page_config(
    page_title="AI Detector by JustDone",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 接著才做套件檢查
try:
    from transformers import pipeline
except ImportError:
    st.error("⚠️ 缺少必要的 AI 套件。請確認 requirements.txt 中包含 transformers 和 torch。")
    st.stop()

# 2. 進階視覺優化 (Custom CSS)
# 這段 CSS 負責強制亮色主題，並美化輸入框與按鈕
st.markdown("""
    <style>
    /* 強制設定背景為亮灰白，解決深色模式問題 */
    .stApp {
        background-color: #F8F9FA;
        color: #1A202C;
    }
    
    /* 隱藏 Streamlit 預設的漢堡選單與 Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 標題區域樣式 */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 1rem;
    }
    .main-header h1 {
        color: #1A202C;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main-header p {
        color: #718096;
        font-size: 1.1rem;
    }

    /* 輸入框美化：白色背景 + 陰影 + 圓角 */
    .stTextArea {
        background-color: #FFFFFF;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        padding: 1rem;
        border: 1px solid #E2E8F0;
    }
    
    /* 修正輸入框內的文字顏色 */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        font-size: 1.1rem;
        caret-color: #2D3748;
    }

    /* 按鈕樣式：深色圓角 */
    div.stButton > button {
        background-color: #2D3748;
        color: white;
        border-radius: 30px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #1A202C;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    
    /* 結果卡片樣式 */
    .result-box {
        padding: 24px;
        border-radius: 16px;
        margin-top: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .human-safe {
        background-color: #F0FFF4;
        border: 1px solid #C6F6D5;
        color: #276749;
    }
    .ai-warning {
        background-color: #FFF5F5;
        border: 1px solid #FED7D7;
        color: #9B2C2C;
    }
    .uncertain {
        background-color: #FFFFF0;
        border: 1px solid #FEEBC8;
        color: #975A16;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 載入 AI 模型 (Model Loading)
# @st.cache_resource 確保模型只下載一次
@st.cache_resource
def load_model():
    # 使用 HuggingFace 的 RoBERTa 檢測模型
    return pipeline("text-classification", model="roberta-base-openai-detector")

# --- UI 結構開始 ---

# 標題區
st.markdown("""
    <div class='main-header'>
        <h1>AI Detector by JustDone</h1>
        <p>Maintain the authenticity of your writing by identifying AI-generated content.</p>
    </div>
""", unsafe_allow_html=True)

# Session State 管理 (用於清空文字)
if 'user_text' not in st.session_state:
    st.session_state.user_text = ""

def clear_text():
    st.session_state.user_text = ""

# 輸入框區域
# 使用 Container 來控制寬度
with st.container():
    text_input = st.text_area(
        "Input Text",
        value=st.session_state.user_text,
        height=280,
        placeholder="Paste your text here to check if it's AI-generated...",
        label_visibility="collapsed"
    )

# 按鈕操作區
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 將按鈕並排顯示
    btn_c1, btn_c2 = st.columns([2, 1])
    with btn_c1:
        check_btn = st.button("✨ Check Content", use_container_width=True, type="primary")
    with btn_c2:
        # 只有當有文字時，清空按鈕才有意義 (但為了排版我們讓它一直存在或用條件顯示)
        if text_input:
            st.button("🗑️ Clear", on_click=clear_text, use_container_width=True)

# 4. 核心檢測邏輯
if check_btn and text_input:
    # 簡單驗證 - 將限制從 20 字降為 2 字，方便測試
    if len(text_input.strip()) < 2:
        st.warning("⚠️ Text is too short. Please enter at least 2 characters.")
    else:
        # 顯示載入動畫
        with st.spinner("Analyzing patterns..."):
            try:
                pipe = load_model()
                # 截斷過長文字
                result = pipe(text_input[:512])
                
                label = result[0]['label']
                score = result[0]['score']
                
                # 判斷邏輯: 'Fake' = AI, 'Real' = Human
                is_ai = (label == 'Fake')
                ai_prob = score if is_ai else (1.0 - score)
                final_score = round(ai_prob * 100, 1)
                
                # --- 結果顯示區 ---
                st.markdown("---")
                
                if final_score > 50:
                    # AI 判定
                    st.markdown(f"""
                        <div class='result-box ai-warning'>
                            <div style='font-size: 2rem;'>🚨</div>
                            <div>
                                <div style='font-size: 1.4rem; font-weight: 800;'>AI Content Detected</div>
                                <div style='font-size: 1.1rem;'>Confidence: <strong>{final_score}%</strong></div>
                                <div style='font-size: 0.9rem; opacity: 0.8;'>This text contains highly structured patterns typical of AI models.</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif final_score < 20:
                    # 人類 判定
                    st.markdown(f"""
                        <div class='result-box human-safe'>
                            <div style='font-size: 2rem;'>✅</div>
                            <div>
                                <div style='font-size: 1.4rem; font-weight: 800;'>Likely Human Written</div>
                                <div style='font-size: 1.1rem;'>AI Probability: <strong>{final_score}%</strong> (Very Low)</div>
                                <div style='font-size: 0.9rem; opacity: 0.8;'>This text shows natural variation and authentic human tone.</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                else:
                    # 不確定
                    st.markdown(f"""
                        <div class='result-box uncertain'>
                            <div style='font-size: 2rem;'>🟠</div>
                            <div>
                                <div style='font-size: 1.4rem; font-weight: 800;'>Mixed / Uncertain</div>
                                <div style='font-size: 1.1rem;'>AI Probability: <strong>{final_score}%</strong></div>
                                <div style='font-size: 0.9rem; opacity: 0.8;'>The text is ambiguous. It might be heavily edited or too short to determine.</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                # 視覺化進度條
                st.write("") # Spacer
                st.caption(f"Analysis based on RoBERTa model | Analyzed {len(text_input)} characters")
                st.progress(final_score / 100)

            except Exception as e:
                st.error(f"Analysis Failed: {str(e)}")

# 頁尾資訊
st.markdown("<div style='margin-top: 50px; text-align: center; color: #CBD5E0; font-size: 0.8em;'>Powered by HuggingFace Transformers</div>", unsafe_allow_html=True)