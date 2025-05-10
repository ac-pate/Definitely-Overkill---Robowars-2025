
#include <Arduino.h>
#include <Servo.h>

const int esc1Pin = 9;   // motor 1
const int esc2Pin = 10;  // motor 2

Servo esc1;
Servo esc2;

// esc min/max pulse widths in microseconds
const int pulseMin = 1100;  // 1.0 ms
const int pulseMax = 1900;  // 2.0 ms

// ramp settings
const float rampStep = 0.02;    // increase throttle by 2% per step
const int rampDelay = 50;       // ms delay between each step

// current throttle values
float currentThrottle1 = 0.0;
float currentThrottle2 = 0.0;

void setup() {
  esc1.attach(esc1Pin, pulseMin, pulseMax);
  esc2.attach(esc2Pin, pulseMin, pulseMax);

  // arm escs with min throttle
  writeThrottle(esc1, 0.0);
  writeThrottle(esc2, 0.0);

  delay(2000);  // wait for escs to initialize
}

void loop() {
  // ramp both motors up to 80% throttle
  rampThrottle(esc1, &currentThrottle1, 0.8);
  rampThrottle(esc2, &currentThrottle2, 0.8);

  delay(2000);

  // ramp both motors down to 0% throttle
  rampThrottle(esc1, &currentThrottle1, 0.0);
  rampThrottle(esc2, &currentThrottle2, 0.0);

  delay(2000);
}

// maps a 0.0–1.0 throttle to pulse width and writes to esc
void writeThrottle(Servo &esc, float throttle) {
  throttle = constrain(throttle, 0.0, 1.0);
  int pulseWidth = pulseMin + throttle * (pulseMax - pulseMin);
  esc.writeMicroseconds(pulseWidth);
}

// gradually ramps throttle to target value
void rampThrottle(Servo &esc, float* currentThrottle, float targetThrottle) {
  while (abs(targetThrottle - *currentThrottle) > 0.01) {
    if (targetThrottle > *currentThrottle) {
      *currentThrottle += rampStep;
    } else {
      *currentThrottle -= rampStep;
    }

    *currentThrottle = constrain(*currentThrottle, 0.0, 1.0);

    writeThrottle(esc, *currentThrottle);
    delay(rampDelay);
  }

  // final adjustment to target
  writeThrottle(esc, targetThrottle);
  *currentThrottle = targetThrottle;
}
