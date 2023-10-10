/*
   1. 측정 시작 버튼을 누른다 -> 측정을 하고 데이터를 저장해둔다
   2. 시리얼이 연결되고 난 후 전송 버튼을 누른다 -> 저장해둔 데이터를 모두 출력한다.
*/
#define INPUT_SIZE 10

// 입출력용 버퍼
char inputBuf[10];
char outputBuf[35];

// 실험 정보와 측정 데이터 개수
float freq, R, L, C;
float R2 = 0; // RLC회로 이후 GND와의 전압차를 만들어내기 위해 달아주는 저항의 값
const int dataNum = 500;  // 측정할 데이터 개수
char gotDataFlag = 0;  // 출력할 데이터가 존재하는지 여부
unsigned long start_time; // 측정 시작 시각
unsigned long end_time; // 측정 종료 시각

// 신호 저장 배열
// 배열의 길이를 최대화하고자 배열의 자료형을 unsigned char로 설정하여 0~255 사이 값으로 전압값을 1/4배해 저장해둠.
unsigned char original_waves[dataNum] = {0, };
unsigned char rlc_waves[dataNum] = {0, };

// 표시등 핀과 버튼 핀
int sendButton_pin = 5;
int gled_pin = 4;
int rled_pin = 3;
int measureButton_pin = 2;

void setup() {
  // 핀 초기설정
  pinMode(gled_pin, OUTPUT);
  pinMode(rled_pin, OUTPUT);
  pinMode(sendButton_pin, INPUT_PULLUP);  // 버튼 입력 핀은 INPUT_PULLUP 모드로 설정해서 플로팅 현상을 막음
  pinMode(measureButton_pin, INPUT_PULLUP);
  digitalWrite(gled_pin, LOW);
  digitalWrite(rled_pin, LOW);

  Serial.begin(2000000);  // ** Baudrate 시리얼 모니터에서 꼭 맞춰주기!
  
}



void loop() {
  // 측정 시작 버튼을 누르면 측정해서 데이터를 저장해둠
  // (버튼 핀은 INPUT_PULLUP 모드로 설정하고 GND에 연결했기 때문에 누르면 LOW 신호가 들어옴)
  if (digitalRead(measureButton_pin) == LOW) measureWave();

  // 측정 데이터가 존재하는 경우 전송 버튼이 눌리면 결과를 시리얼 모니터에 출력함
  if (digitalRead(sendButton_pin) == LOW && gotDataFlag == 1) {
    outputResult();
  }
}

void measureWave() {
  //측정 진행중임을 빨간 LED로 표시
  digitalWrite(rled_pin, HIGH);

  start_time = micros();  // 측정 시작 시각 저장
  for (int i = 0; i < dataNum; i++) {
    original_waves[i] = (unsigned char)analogRead(A0) / 4;
    rlc_waves[i] = (unsigned char)analogRead(A1) / 4;
  }
  end_time = micros();  // 측정 종료 시각 저장

  // 측정 종료시 표시등 상태 바꿈
  digitalWrite(rled_pin, LOW);
  digitalWrite(gled_pin, HIGH);
  gotDataFlag = 1;
}

void outputResult() {
  Serial.println("측정한 주파수를 입력해주세요 : ");
  while (Serial.available() == 0 ) {} // 주파수 입력이 있을때까지 기다림
  Serial.readBytesUntil('\n', inputBuf, INPUT_SIZE);
  freq = atof(inputBuf);
  Serial.println(freq);
  Serial.flush();
  
  Serial.println("사용한 저항값을 Ohm 단위로 입력해주세요 : ");
  while (Serial.available() == 0 ) {}
  Serial.readBytesUntil('\n', inputBuf, INPUT_SIZE);
  R = atof(inputBuf);
  Serial.println(R);
  Serial.flush();
  
  Serial.println("사용한 L값을 mH 단위로 입력해주세요 : ");
  while (Serial.available() == 0 ) {}
  Serial.readBytesUntil('\n', inputBuf, INPUT_SIZE);
  L = atof(inputBuf);
  Serial.println(L);
  Serial.flush();

  Serial.println("사용한 C값을 uF 단위로 입력해주세요 : ");
  while (Serial.available() == 0 ) {}
  Serial.readBytesUntil('\n', inputBuf, INPUT_SIZE);
  C = atof(inputBuf);
  Serial.println(C);
  Serial.flush();

  Serial.println("사용한 R2값을 Ohm 단위로 입력해주세요(없으면 0입력) : ");
  while (Serial.available() == 0 ) {}
  Serial.readBytesUntil('\n', inputBuf, INPUT_SIZE);
  R2 = atof(inputBuf);
  Serial.println(R2);
  Serial.flush();
    
  for (int i = 0; i < dataNum; i++) {
    sprintf(outputBuf, "%d;%d", (unsigned int)(original_waves[i]) * 4, (unsigned int)(rlc_waves[i]) * 4);
    Serial.println(outputBuf);
  }
  Serial.println("한 채널에서의 샘플당 측정 시간 : ");
  sprintf(outputBuf, "%lu", (end_time - start_time) / dataNum);
  Serial.print(outputBuf);
}
