import os
import pandas as pd
from datasets import load_dataset

current_dir = os.path.dirname(os.path.abspath(__file__))
output_csv_path = os.path.join(current_dir, "verified_prompts_db.csv")

def build_verified_prompt_db():
    print("🚀 啟動資料庫建置：切換至標準 Parquet 格式 (Lexica.art 策展數據)...")
    
    try:
        # 直接讀取原生支援的資料集，免除任何腳本資安阻擋
        dataset = load_dataset("Gustavosta/Stable-Diffusion-Prompts", split="train")
        df = pd.DataFrame(dataset)
        
        print(f"✅ 成功載入 {len(df)} 筆來自 Lexica.art 的頂級 Prompt！")

        # 【處理層 Processing：大數據過濾】
        # 1. 確保 Prompt 長度足夠 (長詠唱通常包含對解剖學、光影的精細控制)
        high_quality_df = df[df['Prompt'].str.len() > 150].copy()
        
        # 2. 定義我們的商業價值標籤
        high_quality_df['value_tier'] = 'Premium'
        
        # 3. 欄位重新命名以符合我們後端系統的格式
        high_quality_df = high_quality_df[['Prompt', 'value_tier']]
        high_quality_df.rename(columns={'Prompt': 'positive_prompt'}, inplace=True)
        
        # 4. 抽取 1000 筆最頂級的長咒語作為我們 Demo 系統的商品資料庫
        final_db = high_quality_df.head(1000)
        
        final_db.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        
        print(f"🎉 成功淬鍊出 {len(final_db)} 筆具備商業價值的高細節 Prompt！")
        print(f"📁 您的核心資料庫已儲存至：\n{output_csv_path}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    build_verified_prompt_db()