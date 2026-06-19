import streamlit as st
import pandas as pd
import os

# 設定網頁標題與排版
st.set_page_config(page_title="AI 提示詞資料庫", layout="wide")

# 讀取剛剛抓下來的資料
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "verified_prompts_db.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# 網頁標題區塊
st.title("🛒 AI 繪圖黃金提示詞 (Prompt) 檢索市集")
st.markdown("### 企業級授權資料庫 Demo")
st.write("所有數據皆經過大數據長度與特徵清洗，保證高細節產出品質。")

if df.empty:
    st.error("找不到 verified_prompts_db.csv 檔案。請確認它與 app.py 在同一個資料夾。")
else:
    # 搜尋框
    search_query = st.text_input("🔍 搜尋部位或風格 (例如: hand, eye, lighting, realistic):", "")
    
    # 根據搜尋過濾資料
    if search_query:
        # 忽略大小寫進行模糊搜尋
        filtered_df = df[df['positive_prompt'].str.contains(search_query, case=False, na=False)]
        
        if len(filtered_df) > 0:
            st.success(f"找到 {len(filtered_df)} 筆相關的頂級提示詞：")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("沒有找到符合的提示詞，請嘗試其他關鍵字。")
    else:
        st.info(f"目前資料庫共有 {len(df)} 筆經過驗證的提示詞。以下隨機展示 50 筆：")
        st.dataframe(df.sample(min(50, len(df))), use_container_width=True)