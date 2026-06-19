import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 自動動態取得路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
input_csv_path = os.path.join(current_dir, "local_ai_art_data_bulk.csv")
output_freq_chart = os.path.join(current_dir, "keyword_frequency.png")
output_heat_chart = os.path.join(current_dir, "keyword_heat.png")

# 設定支援中文的字體
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

try:
    # 2. 讀取資料
    df = pd.read_csv(input_csv_path)

    # 3. 處理 PTT 獨特的推文數 (nrec) 格式
    def parse_nrec(x):
        x = str(x).strip()
        if x == '爆': return 100
        if x.startswith('X'): return -10  # 噓文
        if not x or x == 'nan': return 0
        try: return int(x)
        except: return 0

    df['nrec_score'] = df['nrec'].apply(parse_nrec)

    # 4. 擴充後的大型關鍵字庫
    keywords = {
        '解剖痛點': ['手', '手指', '腳', '眼睛', '臉', '肢體', '骨架', '關節', '瞳孔', '比例'],
        '技術求助': ['崩', '壞', '問題', '求救', '幫忙', '怎麼', '請教', '求助', '失敗', '請益', '教學', '修正', '咒語', 'prompt']
    }
    
    all_keywords = keywords['解剖痛點'] + keywords['技術求助']

    # 5. 統計每個關鍵字的「出現次數」與「平均推文熱度」
    stats = []
    for kw in all_keywords:
        # 找出標題包含該關鍵字的文章
        mask = df['title'].str.contains(kw, na=False, case=False)
        count = int(mask.sum())
        
        if count > 0:
            # 計算這些文章的平均推文數
            avg_heat = df[mask]['nrec_score'].mean()
            stats.append({'Keyword': kw, 'Count': count, 'Avg_Heat': avg_heat})

    # 轉為 DataFrame 方便排序與畫圖
    stats_df = pd.DataFrame(stats).sort_values(by='Count', ascending=False)

    # ---------------------------------------------------------
    # 繪圖 A：關鍵字出現頻率 (看普遍性)
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 7))
    sns.barplot(data=stats_df, x='Count', y='Keyword', palette="Blues_r")
    plt.title('AI 繪圖論壇痛點分析：出現頻率 (需求普遍性)', fontsize=16, fontweight='bold')
    plt.xlabel('出現次數 (篇)', fontsize=12)
    plt.ylabel('關鍵字', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_freq_chart, dpi=300)

    # ---------------------------------------------------------
    # 繪圖 B：關鍵字討論熱度 (看痛點深度)
    # ---------------------------------------------------------
    # 依照熱度重新排序
    stats_df_heat = stats_df.sort_values(by='Avg_Heat', ascending=False)
    
    plt.figure(figsize=(12, 7))
    sns.barplot(data=stats_df_heat, x='Avg_Heat', y='Keyword', palette="Oranges_r")
    plt.title('AI 繪圖論壇痛點分析：平均討論熱度 (付費解決意願)', fontsize=16, fontweight='bold')
    plt.xlabel('平均推文數 (互動熱度)', fontsize=12)
    plt.ylabel('關鍵字', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_heat_chart, dpi=300)

    print(f"\n分析完成！共分析 {len(df)} 篇文章。")
    print(f"圖表已成功存入當前資料夾：\n1. {output_freq_chart}\n2. {output_heat_chart}")

    # 印出文字總結供報告使用
    print("\n--- 報告數據摘要 (供複製) ---")
    print(f"在 {len(df)} 篇樣本中，最常被提及的痛點是「{stats_df.iloc[0]['Keyword']}」(出現 {stats_df.iloc[0]['Count']} 次)。")
    print(f"而引發最熱烈討論的技術問題是關於「{stats_df_heat.iloc[0]['Keyword']}」(平均每篇獲得 {stats_df_heat.iloc[0]['Avg_Heat']:.1f} 次互動)。")

except FileNotFoundError:
    print(f"錯誤：找不到輸入檔案，請確認 {input_csv_path} 是否存在！(請先執行爬蟲)")
except Exception as e:
    print(f"執行時發生錯誤: {e}")