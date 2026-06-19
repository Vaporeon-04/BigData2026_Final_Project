import os
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# 1. 自動動態取得「當前 .py 檔案所在」的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 定義輸出 CSV 檔案的絕對路徑 (保證統一存進當前資料夾)
output_csv_path = os.path.join(current_dir, "local_ai_art_data_bulk.csv")

# 設定 Header 模擬瀏覽器 (遵守資料倫理與合規性要求)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
}

def get_ptt_ai_art_data(pages_to_scrape=50):
    print(f"準備擷取 PTT AI_Art 版的 {pages_to_scrape} 頁數據...")
    
    base_url = "https://www.ptt.cc"
    # 從首頁開始
    current_url = base_url + "/bbs/AI_Art/index.html"
    data = []

    for i in range(pages_to_scrape):
        print(f"正在抓取第 {i+1} 頁...")
        
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print(f"連線失敗，錯誤代碼: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 擷取當前頁面的文章資料
        articles = soup.find_all('div', class_='r-ent')
        for article in articles:
            title_element = article.find('div', class_='title')
            if title_element and title_element.a:
                title = title_element.a.text.strip()
                data.append({
                    'title': title,
                    'url': base_url + title_element.a['href'],
                    'nrec': article.find('div', class_='nrec').text.strip() # 推文熱度
                })
        
        # 2. 尋找「上一頁」的按鈕並更新 URL
        paging_div = soup.find('div', class_='btn-group btn-group-paging')
        # PTT 的分頁按鈕順序通常是：首頁、上頁、下頁、末頁，取第二個 <a> 標籤（索引值為 1）
        prev_page_a = paging_div.find_all('a')[1] 
        
        if 'href' in prev_page_a.attrs:
            current_url = base_url + prev_page_a['href']
        else:
            print("找不到上一頁，可能已到達最舊的文章。")
            break
            
        # 3. 資料倫理防線：每抓完一頁，隨機休息 1.5 到 3.5 秒 (Rate Limiting)
        sleep_time = random.uniform(1.5, 3.5)
        print(f"休息 {sleep_time:.2f} 秒...")
        time.sleep(sleep_time)

    # 3. 轉成 DataFrame 並精確存入當前資料夾
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"\n任務完成！共擷取 {len(df)} 筆資料。")
    print(f"CSV 檔案已成功存入當前資料夾位置：\n{output_csv_path}")

if __name__ == "__main__":
    # 預設直接跑 50 頁獲取大量數據，你也可以視情況修改此數值
    get_ptt_ai_art_data(pages_to_scrape=50)