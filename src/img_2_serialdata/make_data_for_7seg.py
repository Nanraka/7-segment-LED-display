import csv


# === グローバル関数 ===
data_size = 3200 # 画素数を指定



# =========================
# 1. CSV読み込み関数
# =========================
def load_1column_csv(path):
    data = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 0:
                continue
            data.append(int(row[0]))
    return data


# =========================
# 2. 64要素ブロックごとに並び替える関数
# =========================
def reorder_by_64_blocks(data):
    BLOCK = 64
    ORDER_64 = [
        40,  0, 17, 16, 56, 41, 18,  1,
        42,  2, 20, 19, 57, 43, 21,  3,
        44,  4, 23, 22, 58, 45, 24,  5,
        46,  6, 26, 25, 59, 47, 27,  7,
        48,  8, 29, 28, 60, 49, 30,  9,
        50, 10, 32, 31, 61, 51, 33, 11,
        52, 12, 35, 34, 62, 53, 36, 13,
        54, 14, 38, 37, 63, 55, 39, 15
    ]

    assert len(data) % BLOCK == 0, "配列長は64の倍数である必要があります"

    reordered = []

    for base in range(0, len(data), BLOCK):
        block = data[base:base + BLOCK]
        reordered.extend(block[i] for i in ORDER_64)

    return reordered


# =========================
# 3. ファイルパス
# =========================
MASK_CSV_PATH = "mask_data.csv"
INPUT_CSV_PATH = "serial_data.csv"
OUTPUT_CSV_PATH = "output.csv"


# =========================
# 4. データ読み込み
# =========================
MASK_DATA = load_1column_csv(MASK_CSV_PATH)
input_data = load_1column_csv(INPUT_CSV_PATH)


# =========================
# 5. サイズチェック
# =========================
assert len(MASK_DATA) == data_size, f"MASK_DATAは{data_size}要素である必要があります"
assert len(input_data) == data_size, f"input_dataは{data_size}要素である必要があります"


# =========================
# 6. AND演算
# =========================
and_result = [
    input_data[i] & MASK_DATA[i]
    for i in range(data_size)
]

# =========================
# 7. MASK_DATAが1の要素のみ抽出
# =========================
extracted_data = [
    and_result[i]
    for i in range(data_size)
    if MASK_DATA[i] == 1
]


# =========================
# 8. 並べ替え
# =========================
result = reorder_by_64_blocks(extracted_data)


# =========================
# 9. TXT出力
# =========================
with open("output.txt", "w") as f:
    for v in result:
        f.write(f"{v}\n")


# =========================
# 10. CSV出力
# =========================
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for v in result:
        writer.writerow([v])


# =========================
# 11. 結果表示
# =========================
print("処理完了")
print(f"MASK_DATAの1の数      : {sum(MASK_DATA)}")
print(f"抽出されたデータ数   : {len(extracted_data)}")