#include <Keyboard.h>

const int ledPin = 17;  // Define the LED pin
const int pcPowerPin = A0;
void setup() {
  pinMode(pcPowerPin, OUTPUT);
  digitalWrite(pcPowerPin, HIGH);
  // Initialize the USB keyboard emulation
  Keyboard.begin();
  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);  // open the serial port at 9600 bps:
}
unsigned long long intervalMins = 5;
unsigned long long start = millis();
unsigned long long waitMs = intervalMins * 60 * 1000;

void blink(int times, int delay_ = 250) {
  for (int n = 0; n < times; n++) {

    digitalWrite(ledPin, HIGH);
    delay(delay_);
    digitalWrite(ledPin, LOW);
    delay(delay_);
  }
}
void printLongLong(long long value) {
  if (value < 0) {
    Serial.print('-');
    value = -value;
  }
  
  unsigned long longPart = (unsigned long)(value >> 32); // Get the upper 32 bits
  unsigned long remainder = (unsigned long)value;   // Get the lower 32 bits

  Serial.print(longPart);
  Serial.print(remainder);
}

void loop() {
  // blink(5);
  unsigned long long ct = millis();
  if (ct - start > waitMs) {
    Serial.println("trigger");
    blink(5, 150);
    digitalWrite(pcPowerPin, LOW);  // Turn on the LED
    delay(500);                      // Wait for a short duration
    digitalWrite(pcPowerPin, HIGH);  // Turn off the LED
    start = ct;
  }
  delay(5000);
  // Keyboard.press(KEY_KP_ENTER);
  blink(1);
  // Keyboard.release(KEY_KP_ENTER);
  long long rem = ct - start;
  printLongLong(rem);
  
  Serial.print(" ");
  printLongLong(waitMs);
  Serial.println();

  // Press the "A" keya
  // 
  // Blink the LEDaa

  // 
  // Wait for 10 seconds
}
