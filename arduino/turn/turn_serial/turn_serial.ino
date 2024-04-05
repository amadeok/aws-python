#include <Keyboard.h>
#include <AbsMouse.h>
#include "utils.h"

void (*resetFunc)(void) = 0;  // declare reset fuction at address 0


enum serialStatusEnum { settingX,
                        settingY,
                        ready };
int serialStatus = settingX;


unsigned int intervalMins = 5 * 60;
unsigned long long waitMs = 0;   //intervalMins * 60 * 1000;
unsigned long long debugMs = 0;  //*1000 MULTIPLIED ON SETUP()
unsigned long blinkRemTimeIntervalMs = 5 * 1000;
bool bPrintInfo = 0;
bool bBeepRemainerTime = 0;
bool bPressEnter = false;

unsigned long long start = millis();
unsigned long long start2 = start;
unsigned long long startPress = start;

const int PIN_BEEP_REM = 3;

void setup() {
  pinMode(PC_POWER_PIN, OUTPUT);
  digitalWrite(PC_POWER_PIN, HIGH);
  waitMs = intervalMins * 60;
  waitMs *= 1000;
  debugMs *= 1000;
  pinMode(PIN_BEEP_REM, INPUT_PULLUP);

  if (using_pro_micro) {
    pinMode(proMicroLED_pin, OUTPUT);  // Set RX LED as an output
    LED_PIN = proMicroLED_pin;
  }
  for (int n = 0; n < 2; n++) {
    blink(1, 300, 100, 700);
    blink(1, 300, 100, 1000);
  }
  digitalWrite(resetPin, HIGH);
  delay(200);
  pinMode(resetPin, OUTPUT);

  Serial.begin(115200);
  Serial.setTimeout(1);

  for (int n_counter = 0; n_counter < 3; n_counter++) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }

  AbsMouse.init(1920, 1080);  //4320, 1650);
  Keyboard.begin();
  delay(500);
}

bool beepOrNot() {
  return bBeepRemainerTime || !digitalRead(PIN_BEEP_REM);
}
void triggerBeep() {
  for (int n = 0; n < 2; n++) {
    blink(1, 300, 200, 500);
    blink(1, 300, 200, 700);
    blink(1, 300, 200, 1000);
    blink(1, 300, 200, 1000);
    blink(1, 300, 200, 700);
    blink(1, 300, 200, 500);
  }
}

void printInfo(unsigned long targetMs, unsigned long remMs, unsigned long hours, unsigned long minutes, unsigned long tensOfMinutes) {
  Serial.print(targetMs);
  Serial.print("tms ");

  Serial.print(remMs / 1000 / 60);
  Serial.print("m ");
  Serial.print((remMs % 60000) / 1000);

  Serial.print("s | ");
  Serial.print(hours);
  Serial.print("h ");

  Serial.print(minutes);
  Serial.print("m | ");
  Serial.print(tensOfMinutes);
  Serial.print(" tens mins ");
  Serial.println("");
}

void loop() {
  // blink(3, 300, 100, 1000);
  delay(100);
  unsigned long targetMs = (debugMs ? debugMs : waitMs);
  unsigned long long ct = millis();
  unsigned long elapsedMs = ct - start;
  unsigned long remMs = targetMs - elapsedMs;
  unsigned long hours = remMs / 3600000;              // 1 hour = 3600000 milliseconds
  unsigned long minutes = (remMs % 3600000) / 60000;  // 1 minute = 60000 milliseconds
  unsigned long tensOfMinutes = minutes / 10;

  if (bPrintInfo) {
    printInfo(targetMs, remMs, hours, minutes, tensOfMinutes);
  }

  if (elapsedMs > targetMs) {
    // Serial.println("trigger");
    //blink(6, 100, 300, 1200);
    triggerBeep();
    digitalWrite(PC_POWER_PIN, LOW);   // Turn on the LED
    delay(500);                        // Wait for a short duration
    digitalWrite(PC_POWER_PIN, HIGH);  // Turn off the LED
    start = millis();
    bPressEnter = true;
  }

  unsigned long elapsedMs2 = ct - start2;
  unsigned long remMs2 = blinkRemTimeIntervalMs - elapsedMs2;

  if (elapsedMs2 > blinkRemTimeIntervalMs) {
    // Serial.println("trigger");
    bool beep = beepOrNot();

    if (hours || tensOfMinutes) {
      blink(hours, 500, 300, beep ? 500 : 0);
      delay(1000);
      blink(tensOfMinutes, 150, 150, beep ? 700 : 0);
    } else if (minutes >= 2)
      blink(4, 75, 75, beep ? 900 : 0);
    else
      blink(20, 75, 75, beep ? 1000 : 0);

    start2 = millis();
  }

  if (bPressEnter) {
    unsigned long elapsedMsPress = ct - startPress;
    unsigned long remMsPress = (10 * 1000) - elapsedMsPress;
    if (elapsedMsPress > (10 * 1000)) {
      //Serial.println("trigger");
      Keyboard.press(KEY_KP_ENTER);
      delay(300);
      Keyboard.release(KEY_KP_ENTER);
      startPress = millis();
    }
  }

  String s;

  if (Serial.available()) {
    switch (serialStatus) {

      case settingX:
        x = serial_read_2bytes();
        serialStatus = settingY;
        break;
      case settingY:
        y = serial_read_2bytes();
        serialStatus = ready;
        break;
      case ready:
        {
          key = y;
          switch (x) {
            case 30000:
              press_key(y);
              break;
            case 30001:
              s = serial_read_string(y);
              Keyboard.print(s);
              break;
            case 30002:
              write_pass();
              break;
            case 30003:
              write_string2();
              break;
            case 30004:
              x = serial_read_2bytes();
              y = serial_read_2bytes();
              AbsMouse.move(x, y);
              break;
            case 30005:
              for (int n_counter = 0; n_counter < 10; n_counter++) {
                digitalWrite(LED_PIN, HIGH);
                if (n_counter % 2 == 0)
                  delay(50);
                else
                  delay(10);
                digitalWrite(LED_PIN, LOW);
                delay(50);
              }
              x = serial_read_2bytes();
              y = serial_read_2bytes();
              AbsMouse.init(x, y);
              bPressEnter = false;

              break;
            case 30006:
              delay(10);
              digitalWrite(resetPin, LOW);
              delay(10);
              break;
            case 30007:  // right click
              x = serial_read_2bytes();
              y = serial_read_2bytes();
              move_click_right(x, y);
              break;

            case 30008:  //change delay
              delay_between = y;
              break;
            case 40010:
              intervalMins = serial_read_2bytes();
              waitMs = intervalMins * 60;
              waitMs *= 1000;
              start = millis();
              break;
            case 40011:
              bBeepRemainerTime = serial_read_2bytes();
              break;
            default:
              move_click(x, y);
          }
          serialStatus = settingX;
          break;
        }
    }
  }
}