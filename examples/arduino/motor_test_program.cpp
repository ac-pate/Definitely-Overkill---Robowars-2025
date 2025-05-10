#include <Arduino.h>
#include <Servo.h>

// esc pins
const int motorLeftPin = D3;
const int motorRightPin = 11;

// esc signal range
const int PULSE_FULL_REVERSE = 1100;
const int PULSE_STOP = 1500;
const int PULSE_FULL_FORWARD = 1900;

// built-in blue led on nano ble sense
const int LED_PIN = LED_BUILTIN;

// ramping
#define USE_RAMPING true
const float RAMP_STEP = 0.02; // 2% throttle per update
const int RAMP_INTERVAL = 30; // ms between ramp updates

// servo escs
Servo motorLeft;
Servo motorRight;

// current and target throttle [-1.0 to 1.0]
float currentThrottleLeft = 0.0;
float currentThrottleRight = 0.0;
float targetThrottleLeft = 0.0;
float targetThrottleRight = 0.0;

// timestamp for ramp
unsigned long lastRampTime = 0;

// user input
int action = 0;
int speed = 0;

// converts a -1.0 to 1.0 speed to pulse width
int speedToPulse(float s) {
    s = constrain(s, -1.0, 1.0);
    if (s > 0) return PULSE_STOP + s * (PULSE_FULL_FORWARD - PULSE_STOP);
    if (s < 0) return PULSE_STOP + s * (PULSE_STOP - PULSE_FULL_REVERSE);
    return PULSE_STOP;
  }
  
  
// sends pwm pulse to esc
void writeThrottle(Servo &esc, float value) {
  esc.writeMicroseconds(speedToPulse(value));
}

// converts a -1.0 to 1.0 speed to pulse width
  
  // ramps current throttle toward target
  float rampTo(float current, float target, float step) {
    if (abs(target - current) <= step) return target;
    return (target > current) ? current + step : current - step;
  }
  
  // updates throttle values (non-blocking)
  void updateThrottle() {
    if (millis() - lastRampTime < RAMP_INTERVAL) return;
    lastRampTime = millis();
  
    if (USE_RAMPING) {
      currentThrottleLeft = rampTo(currentThrottleLeft, targetThrottleLeft, RAMP_STEP);
      currentThrottleRight = rampTo(currentThrottleRight, targetThrottleRight, RAMP_STEP);
    } else {
      currentThrottleLeft = targetThrottleLeft;
      currentThrottleRight = targetThrottleRight;
    }
  
    writeThrottle(motorLeft, currentThrottleLeft);
    writeThrottle(motorRight, currentThrottleRight);
  
    // turn led on if either motor is moving
    if (abs(currentThrottleLeft) > 0.01 || abs(currentThrottleRight) > 0.01) {
      digitalWrite(LEDB, LOW);
  } else {
      digitalWrite(LEDB, HIGH);
  }
  }
  
  // movement abstractions
  void moveForward(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = s;
    targetThrottleRight = s;
  }

  void stop(int speed) {
    float s = speed * 0.0;
    targetThrottleLeft = s;
    targetThrottleRight = s;
  }
  
  void moveBackward(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = -s;
    targetThrottleRight = -s;
  }
  
  void spinLeft(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = -s;
    targetThrottleRight = s;
  }
  
  void spinRight(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = s;
    targetThrottleRight = -s;
  }
  
  void arcLeft(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = s * 0.5;
    targetThrottleRight = s;
  }
  
  void arcRight(int speed) {
    float s = speed / 100.0;
    targetThrottleLeft = s;
    targetThrottleRight = s * 0.5;
  }
  
  void impulse(int speed) {
    float s = speed / 100.0;
    writeThrottle(motorLeft, s);
    writeThrottle(motorRight, s);
    delay(150);
    targetThrottleLeft = 0.0;
    targetThrottleRight = 0.0;
  }
  
  // handles serial input
  void handleInput() {
    if (Serial.available()) {
      action = Serial.parseInt();
      speed = Serial.parseInt();
      speed = constrain(speed, 0, 100); // always positive
  
      Serial.print("Action: "); Serial.print(action);
      Serial.print(" | Speed: "); Serial.println(speed);
  
      switch (action) {
        case 0: stop(speed); break;
        case 1: moveForward(speed); break;
        case 2: moveBackward(speed); break;
        case 3: spinLeft(speed); break;
        case 4: spinRight(speed); break;
        case 5: arcLeft(speed); break;
        case 6: arcRight(speed); break;
        case 7: impulse(speed); break;
        default: targetThrottleLeft = 0.0; targetThrottleRight = 0.0; break;
      }
    }
  }
  

void setup() {
  Serial.begin(115200);
  while (!Serial);

  motorLeft.attach(motorLeftPin);
  motorRight.attach(motorRightPin);

  // Initialize RGB LED pins
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  // Turn off all colors
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  // set both escs to stop
  writeThrottle(motorLeft, 0.0);
  writeThrottle(motorRight, 0.0);
  digitalWrite(LEDB, LOW);

  delay(5000); // wait for escs to initialize

  Serial.println("Enter: <action> <speed (0–100)>");
  Serial.println("Actions: 1=FWD, 2=BWD, 3=SpinL, 4=SpinR, 5=ArcL, 6=ArcR, 7=Impulse");
}


void loop() {
  handleInput();
  updateThrottle();
}
