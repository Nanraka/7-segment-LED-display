import pandas as pd

# Excelファイルのパス
excel_path = "mask_data.xlsx"

# Excelを読み取る
# header=None : 見出し行なしを想定
df = pd.read_excel(excel_path, header=None)

# 念のためサイズ確認（50 x 160 であることを期待）
rows, cols = df.shape
print(f"rows={rows}, cols={cols}")

# 行優先で並べ替え
row_major_data = []
for r in range(rows):
    for c in range(cols):
        row_major_data.append(df.iat[r, c])

# pandas DataFrame に変換（1列）
out_df = pd.DataFrame(row_major_data)

# CSVとして保存（必要な場合）
out_df.to_csv("mask_data.csv",
              index=False,
              header=False)

print("完了: mask_data.csv を生成しました")