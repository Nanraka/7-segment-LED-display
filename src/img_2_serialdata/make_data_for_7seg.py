import csv


# === グローバル関数 ===
data_size = 6144
seg_num = 8
segments_per_column = 16
column = 16


# === Read CSV ===

def load_row_csv(path):
    data = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                data.append(int(cell))
    return data


# === 要素ブロックごとに並び替える関数 ===
def reorder_blocks(data):
    base_pattern = [16, 96, 49, 48, 0, 17, 50, 97]

    # 各要素のオフセット係数
    offset_weights = [2, 2, 3, 3, 1, 2, 3, 2]

    result = []

    for i in range(0,int(len(data)/(seg_num * segments_per_column))):
        for j in range(0,segments_per_column):
            for k in range(0,len(base_pattern)):
                result.append(data[ i * (seg_num * segments_per_column) + base_pattern[k] + j * offset_weights[k] ])
                #print(i * (seg_num * segments_per_column) + base_pattern[k] + j * offset_weights[k])
    return result


def reorder_stage2(data):
    segment_offset = 0
    column_offset = 0
    line_offset = 0

    upp_flag = 0
    line_flag = 0

    upp_element = 1024 - 8
    low_element = 1024 + 1024 - 8

    result = []

    for i in range(segments_per_column * column * seg_num):
        if upp_flag == 1:
            result.append(data[upp_element + segment_offset - column_offset * 8 - line_offset * 128])
        else:
            result.append(data[low_element + segment_offset - column_offset * 8 - line_offset * 128])

        segment_offset += 1

        if segment_offset >= seg_num:
            segment_offset = 0
            column_offset += 1

        if column_offset >= segments_per_column:
            column_offset = 0
            line_flag += 1
            upp_flag = not upp_flag
        
        if line_flag == 2:
            line_flag = 0
            line_offset += 1
            
    return result


# =========================
# 3. ファイルパス
# =========================
MASK_CSV_PATH = "mask_data.csv"
INPUT_CSV_PATH = "serial_data.csv"
OUTPUT_CSV_PATH = "output.csv"


# =========================
# 4. データ読み込み
# =========================
MASK_DATA = load_row_csv(MASK_CSV_PATH)
input_data = load_row_csv(INPUT_CSV_PATH)


# =========================
# 5. サイズチェック
# =========================
assert len(MASK_DATA) == data_size, "MASK_DATAはdata_size要素である必要があります"
assert len(input_data) == data_size, "input_dataはdata_size要素である必要があります"

# =========================
# 7. MASK_DATAが1の要素のみ抽出
# =========================
extracted_data = []

for i in range(data_size):
    if MASK_DATA[i] == 1:
        extracted_data.append(input_data[i])


# =========================
# 8. 並べ替え
# =========================
reorder_blocks_data = reorder_blocks(extracted_data)
result = reorder_stage2(reorder_blocks_data)
print(result)


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