#include<Arduino.h>

const int esc1Pin = 9;   // motor 1
const int esc2Pin = 10;  // motor 2

const int pwmFreq = 50;  // esc expects 50hz
const int pwmRes = 16;   // teensy uses 16-bit pwm
const int pwmMax = 65535;

// esc min/max pulse widths in microseconds
const float pulseMin = 1000.0;  // 1.0 ms
const float pulseMax = 2000.0;  // 2.0 ms

// ramp settings
const float rampStep = 0.02;    // increase throttle by 2% per step
const int rampDelay = 50;       // ms delay between each step

void setup() {
  analogWriteFrequency(esc1Pin, pwmFreq);
  analogWriteFrequency(esc2Pin, pwmFreq);

  analogWriteResolution(pwmRes);

  // arm escs with min throttle
  writeThrottle(esc1Pin, 0.0);
  writeThrottle(esc2Pin, 0.0);

  delay(2000);  // wait for escs to initialize
}

void loop() {
  // ramp both motors up to 80% throttle
  rampThrottle(esc1Pin, 0.8);
  rampThrottle(esc2Pin, 0.8);

  delay(2000);

  // ramp back down to 0%
  rampThrottle(esc1Pin, 0.0);
  rampThrottle(esc2Pin, 0.0);

  delay(2000);
}

// maps a 0.0–1.0 throttle to pwm duty cycle
void writeThrottle(int pin, float throttle) {
  throttle = constrain(throttle, 0.0, 1.0);

  // linear interpolation between min and max pulse
  float pulseWidth = pulseMin + throttle * (pulseMax - pulseMin);  // in microseconds

  // convert pulse width to duty cycle
  float dutyCycle = pulseWidth / 20000.0;  // 20 ms = 50hz period
  int dutyValue = (int)(pwmMax * dutyCycle);

  analogWrite(pin, dutyValue);
}

// gradually ramp throttle to target value
void rampThrottle(int pin, float targetThrottle) {
  // get current pwm value
  int currentValue = analogRead(pin);  // teensy doesn't support analogRead on pwm outputs, workaround below

  // estimate current throttle (optional fallback to global state)
  static float currentThrottle1 = 0.0;
  static float currentThrottle2 = 0.0;

  float* currentThrottle = (pin == esc1Pin) ? &currentThrottle1 : &currentThrottle2;

  while (abs(targetThrottle - *currentThrottle) > 0.01) {
    if (targetThrottle > *currentThrottle) {
      *currentThrottle += rampStep;
    } else {
      *currentThrottle -= rampStep;
    }

    *currentThrottle = constrain(*currentThrottle, 0.0, 1.0);

    writeThrottle(pin, *currentThrottle);
    delay(rampDelay);
  }

  writeThrottle(pin, targetThrottle);  // final write to lock exact value
  *currentThrottle = targetThrottle;
}
