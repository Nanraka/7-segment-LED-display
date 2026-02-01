import pandas as pd

# Excelファイルのパス
excel_path = "mask_data.xlsx"


# Excelを読み取る
df = pd.read_excel(excel_path, header=None)


# サイズ確認
rows, cols = df.shape
print(f"rows={rows}, cols={cols}")


# 列優先（column-major）で並べ替え
# 1列目 上→下 → 2列目 上→下 → ...
column_major_data = []

for c in range(cols):
    for r in range(rows):
        column_major_data.append(df.iat[r, c])

# pandas DataFrame に変換
out_df = pd.DataFrame(column_major_data)

# CSVとして保存
out_df.to_csv("mask_data.csv",
              index=False,
              header=False)
print("完了: mask_data.csv を生成しました")