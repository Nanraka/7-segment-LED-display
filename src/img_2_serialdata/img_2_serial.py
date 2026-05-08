from PIL import Image
import numpy as np


# === グローバル関数 ===
input_image         = "input.jpg"               # 入力画像ファイル名
output_image        = "output_target_heightx160_aki.jpg"   # 出力画像ファイル名
serial_CSV_data         = "serial_data.csv"         # 出力CSVファイル名
serial_TXT_data         = "serial_data.txt"         # 出力TXTファイル名
confirm_serial_data = "confirm_serial_data.csv" # 確認用CSVファイル名

# 変換後のサイズ（縦target_height × 横160）
target_height = 64
target_width = 96


# switch
img_flag = 1  # 1: 画像からシリアルデータ, 0: CSVからシリアルデータ



# === 画像を縦target_height × 横160にリサイズする関数 ===
def img_formatter():
    # 画像を読み込み
    img = Image.open(input_image)

    # 必要なら白黒（グレースケール）に変換
    img = img.convert("L")

    # リサイズ（アスペクト比は無視して強制変換）
    resized_img = img.resize((target_width, target_height), Image.NEAREST)

    # 保存
    resized_img.save(output_image)

    print(f"画像を {target_height}x{target_width} ピクセルに変換して保存しました: {output_image}")




# === 画像をシリアルデータに変換してCSVに保存する関数 ===
def img_2_serial():
    # 画像を読み込み（白黒に変換）
    img = Image.open(output_image).convert("L")  # L = grayscale

    width, height = img.size
    assert (height, width) == (target_height, target_width), "画像サイズがtarget_heightxtarget_widthではありません"

    # NumPy配列に変換
    img_array = np.array(img)

    # しきい値（必要に応じて調整）
    threshold = 128

    # 黒=1, 白=0 に変換
    binary = np.where(img_array < threshold, 1, 0)

    # 縦方向に読み出して1列のシリアルデータにする
    # （列→行の順で読み出し）
    serial_matrix = binary.flatten(order="C").reshape(-1, 1)

    # CSV，txtファイルに書き出し
    np.savetxt(serial_CSV_data, serial_matrix, fmt="%d", delimiter=",")
    np.savetxt(serial_TXT_data, serial_matrix, fmt="%d", delimiter=",")

    print(serial_matrix)
    print(serial_matrix.shape)  # (6target_height0, 1)




# === シリアルデータCSVを確認用に変換して保存する関数 ===
def confirm_serialdata():
    # CSVを読み込み（1列）
    data = np.loadtxt(serial_CSV_data, delimiter=",")

    # target_height行ごとに列へ変換
    assert len(data) % target_height == 0, "データ数がtarget_heightの倍数ではありません"

    matrix = data.reshape(-1, target_width)
    # ↑
    # reshape(-1, target_height) : target_height個ずつまとめる
    # .T              : 転置して「target_height行 × 列数」にする

    # CSVに保存
    np.savetxt(confirm_serial_data, matrix, fmt="%d", delimiter=",")

    print("CSVを書き出しました:", confirm_serial_data)
    print("出力サイズ:", matrix.shape)



# === 行列データを1列シリアルCSVに変換して保存する関数 ===
def save_matrix_to_serial_csv():
    # 行列CSVを読み込み
    matrix = np.loadtxt(confirm_serial_data, delimiter=",",encoding="utf-8-sig")

    # 行 → 行の順で1列にまとめる
    serial_data = matrix.flatten(order="C").reshape(-1, 1)
    # order="F" : 列優先（左の列から順に）

    # CSVに保存
    np.savetxt(serial_CSV_data, serial_data, fmt="%d", delimiter=",")
    np.savetxt(serial_TXT_data, serial_data, fmt="%d", delimiter=",")

    print("1列シリアルCSVを書き出しました:", serial_CSV_data)
    print("出力サイズ:", serial_data.shape)





# === メイン関数 ===
def main():
    if img_flag == 0:
        save_matrix_to_serial_csv()
    elif img_flag == 1:
        img_formatter()
        img_2_serial()
        confirm_serialdata()




# === エントリーポイント ===
if __name__ == "__main__":
    main()