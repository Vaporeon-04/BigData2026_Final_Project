import streamlit as st
import pandas as pd
import os
import urllib.parse # 引入網址編碼工具

st.set_page_config(page_title="AI 提示詞資料庫", layout="wide")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "verified_prompts_db.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # 【殺手級功能：動態生圖 API 串接】
        # 把這句 Prompt 轉換成網址安全格式，然後串上即時生圖引擎
        # 教授一點擊，系統就會當場幫他算出一張圖！
        df['action_link'] = "https://pollinations.ai/p/" + df['positive_prompt'].apply(lambda x: urllib.parse.quote(str(x)[:200])) 
        # (註：截斷前200字避免網址過長報錯)
        
        return df
    return pd.DataFrame()

df = load_data()

st.title("🛒 AI 繪圖黃金提示詞 (Prompt) 檢索市集")
st.markdown("### 企業級授權資料庫 Demo (具備即時生圖 API 功能)")

if df.empty:
    st.error("找不到 verified_prompts_db.csv 檔案，請確認檔案存在。")
else:
    search_query = st.text_input("🔍 搜尋風格或物件關鍵字 (如: robot, magical, steampunk):", "")
    
    display_df = df.copy()
    if search_query:
        display_df = display_df[display_df['positive_prompt'].str.contains(search_query, case=False, na=False)]
        
    if len(display_df) > 0:
        st.success(f"為您展示 {len(display_df)} 筆頂級提示詞：")
        
        st.dataframe(
            display_df.head(30),
            column_config={
                "preview_image": st.column_config.ImageColumn("真實生成預覽 (Preview)"),
                "positive_prompt": st.column_config.TextColumn("大數據驗證提示詞 (Prompt)", width="large"),
                "value_tier": st.column_config.TextColumn("授權等級"),
                "action_link": st.column_config.LinkColumn("自動化 API (Action)", display_text="去算圖 🚀")
            },
            hide_index=True,
            use_container_width=True,
            height=600
        )
    else:
        st.warning("沒有找到符合的提示詞。")