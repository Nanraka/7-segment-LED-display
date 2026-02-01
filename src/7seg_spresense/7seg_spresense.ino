#include <SDHCI.h>
#include <File.h>
#include <SPI.h>


#define DATA_SIZE 2560
#define ROW_SIZE     8  // 1列当たりの7セグメントLEDの数
#define GROUP_SIZE   64 // 1セットあたりの7セグメントLEDの数
#define GROUP_COUNT  2  // セット数
#define LOOP_COUNT   8


uint8_t rowData[DATA_SIZE];
uint8_t sendData[DATA_SIZE];

SDClass SD;

const int DATA_LATCH_PIN = 9;
const int TRAN_LATCH_PIN = 3;
const int OE_PIN = 1;

int tran_pos = 0;

uint8_t cathode_data = 0x80;

「




void sendToShiftRegister(int loop) {

  // 最後のレジスタ分から送る
  for (int group = GROUP_COUNT; group > 0; group--) {

    // 列方向の遷移 下から上に上がっていく
    for (int offset = 0; offset < ROW_SIZE; offset++) {

      int index = group*GROUP_SIZE - offset - (loop * ROW_SIZE) - 1;
      SPI.transfer(sendData[index]);
    }
  }
}



void packBitsToBytes() {

  for (int byteIndex = 0; byteIndex < (DATA_SIZE/8); byteIndex++) {

    uint8_t value = 0;

    // 1バイトにする
    for (int bit = 0; bit < 8; bit++) {
      value <<= 1;  // MSBから詰める
      value |= (rowData[byteIndex * 8 + bit] & 0x01);
    }
    sendData[byteIndex] = value;
  }
}



void setup() {
  Serial.begin(115200);
  while (!Serial);

  // SD初期化
  if (!SD.begin()) {
    Serial.println("SD init failed");
    return;
  }

  File file = SD.open("hi.txt");
  if (!file) {
    Serial.println("File open failed");
    return;
  }

  int idx = 0;
  while (file.available() && idx < DATA_SIZE) {
    char c = file.read();
    if (c == '0' || c == '1') {
      rowData[idx++] = c - '0';
    }
  }
  file.close();

  Serial.print("Loaded: ");
  Serial.println(idx);

  packBitsToBytes();

  // SPI初期化
  SPI.begin();
  SPI.beginTransaction(SPISettings(8000000, LSBFIRST, SPI_MODE0));

  // ピン設定
  pinMode(DATA_LATCH_PIN, OUTPUT);
  pinMode(TRAN_LATCH_PIN, OUTPUT);
  pinMode(OE_PIN, OUTPUT);

  digitalWrite(DATA_LATCH_PIN, HIGH);
  digitalWrite(TRAN_LATCH_PIN, HIGH);
  digitalWrite(OE_PIN, HIGH);
}

void loop() {
  digitalWrite(OE_PIN, HIGH);

  for (int loopCount = 0; loopCount < LOOP_COUNT; loopCount++) {

    digitalWrite(DATA_LATCH_PIN, LOW);
    digitalWrite(TRAN_LATCH_PIN, HIGH);
    sendToShiftRegister(loopCount);

    digitalWrite(DATA_LATCH_PIN, HIGH);
    digitalWrite(TRAN_LATCH_PIN, LOW);
    //uint8_t data = (0x80 >> tran_pos);
    SPI.transfer(cathode_data);

    digitalWrite(DATA_LATCH_PIN, HIGH);
    digitalWrite(TRAN_LATCH_PIN, HIGH);
    digitalWrite(OE_PIN, LOW);

    tran_pos += 1;
    cathode_data = cathode_data >> 1;

    if (tran_pos >= 8){
      tran_pos = 0;
      cathode_data = 0x80;
    }

    delay(2);  // 出力更新周期
  }
}