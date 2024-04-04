#include <Keyboard.h>

const int ledPin = 13; // Define the LED pin
const int pcPowerPin = A0;
void setup() {
    pinMode(pcPowerPin, OUTPUT);
  digitalWrite(pcPowerPin, HIGH);
  // Initialize the USB keyboard emulation
  Keyboard.begin();
  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);

}

void loop() {
    delay(5000);

  // Press the "A" key
  Keyboard.press('a');
  // Blink the LEDaa
  digitalWrite(ledPin, HIGH); // Turn on the LED
  digitalWrite(pcPowerPin, LOW); // Turn on the LEDaaaaa

  delay(500); // Wait for a short duration
  digitalWrite(ledPin, LOW); // Turn off the LED
  digitalWrite(pcPowerPin, HIGH); // Turn off the LED
  Keyboard.release('a');
  // Wait for 10 seconds
  delay(10000);
}