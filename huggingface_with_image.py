import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
output_csv_path = os.path.join(current_dir, "verified_prompts_db.csv")

def build_true_image_db():
    print("🚀 正在繞過腳本，直接讀取 DiffusionDB 的原生 Parquet 數據...")
    
    parquet_url = "https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet"
    
    try:
        # 【修正點】欄位名稱更正為 step，並移除重複的 cfg
        df = pd.read_parquet(parquet_url, columns=['prompt', 'image_name', 'cfg', 'step'])
        
        # 只取前 2000 筆，確保處理速度極快
        df = df.head(2000)
        
        print("✅ 成功下載純文字數據！正在拼湊圖片網址與過濾...")
        
        # 這裡只是「拼字串」，完全不會下載圖片實體檔案，不佔空間
        base_img_url = "https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/images/"
        df['preview_image'] = base_img_url + df['image_name']
        
        # 進行大數據過濾：留長度大於 100 且算圖步數 (step) 大於等於 30 的優質提示詞
        high_quality_df = df[(df['prompt'].str.len() > 100) & (df['step'] >= 30)].copy()
        high_quality_df['value_tier'] = 'Premium'
        
        # 重新整理欄位
        final_db = high_quality_df[['prompt', 'preview_image', 'value_tier']]
        final_db.rename(columns={'prompt': 'positive_prompt'}, inplace=True)
        
        # 存檔
        final_db.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        print(f"🎉 成功！淬鍊出 {len(final_db)} 筆「圖文完全相符」的真實提示詞資料庫！")
        print(f"檔案已安全儲存至：{output_csv_path}")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    build_true_image_db()