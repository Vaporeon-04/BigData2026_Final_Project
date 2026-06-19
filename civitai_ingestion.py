import os
import requests
import time
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
output_csv_path = os.path.join(current_dir, "civitai_prompts_data.csv")

def fetch_civitai_prompts(limit_per_page=100, max_pages=5):
    print(f"啟動 Civitai API 資料擷取管道 (針對特定知名模型)...")
    
    base_url = "https://civitai.com/api/v1/images"
    
    # 改變策略：針對知名的開源模型 (例如 modelId=4384 是 DreamShaper, 122422 是 GhostMix)
    # 這裡我們使用 4384 作為穩定抓取參數的資料源
    params = {
        "limit": limit_per_page,
        "modelId": 4384,          
        "sort": "Most Reactions", 
        "period": "AllTime"       # 改抓歷史上最受歡迎的，確保參數品質
    }
    
    extracted_data = []
    
    for page in range(1, max_pages + 1):
        print(f"正在擷取第 {page} 頁資料...")
        params["page"] = page
        
        try:
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                print(f"  ❌ API 請求失敗，狀態碼: {response.status_code}")
                break
                
            data = response.json()
            items = data.get('items', [])
            print(f"  👉 本頁共抓取到 {len(items)} 張圖片的原始資料")
            
            # 計算本頁有幾個公開參數的圖片
            meta_count = 0 
            
            for item in items:
                meta = item.get('meta')
                
                # 嚴格檢查 meta 是否存在，且包含 prompt
                if meta and isinstance(meta, dict) and 'prompt' in meta:
                    meta_count += 1
                    extracted_data.append({
                        "image_id": item.get('id'),
                        "url": item.get('url'),
                        "like_count": item.get('stats', {}).get('likeCount', 0),
                        "positive_prompt": meta.get('prompt'),
                        "negative_prompt": meta.get('negativePrompt', ''),
                        "sampler": meta.get('sampler', ''),
                        "cfg_scale": meta.get('cfgScale', ''),
                        "steps": meta.get('steps', '')
                    })
            
            print(f"  ✨ 本頁成功萃取出 {meta_count} 筆公開的提示詞參數")
                    
        except Exception as e:
            print(f"  ❌ 發生錯誤: {e}")
            break
            
        time.sleep(1.5) # 友善爬蟲延遲

    # 資料儲存
    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df = df.sort_values(by='like_count', ascending=False)
        df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ 任務完成！共成功萃取 {len(df)} 筆黃金提示詞數據！")
        print(f"檔案已儲存至：{output_csv_path}")
    else:
        print("\n⚠️ 仍然未擷取到任何有效的參數資料，可能 API 暫時阻擋了無金鑰的 Metadata 請求。")

if __name__ == "__main__":
    fetch_civitai_prompts(limit_per_page=100, max_pages=5)