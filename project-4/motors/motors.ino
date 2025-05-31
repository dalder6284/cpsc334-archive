// #include <Stepper.h>
#include <ESP32Servo.h>

// const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution

// // ULN2003 Motor Driver Pins
// #define IN1 19
// #define IN2 18
// #define IN3 5
// #define IN4 17

#define SERVO 2

// // initialize the stepper library
// Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);


// void setup() {
//   // set the speed at 5 rpm
//   myStepper.setSpeed(39);
//   // initialize the serial port
//   Serial.begin(115200);
//   Serial.println("Beginning...");
//   delay(3000);
// }

// void loop() {
//   // step one revolution in one direction:
//   Serial.println("clockwise");
//   myStepper.step(stepsPerRevolution);
//   delay(1000);

//   // step one revolution in the other direction:
//   Serial.println("counterclockwise");
//   myStepper.step(-stepsPerRevolution);
//   delay(1000);

  
// }

#include <Stepper.h>

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution

// ULN2003 Motor Driver Pins
#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 17

// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);
Servo servo1;

int pos = 90;

void setup() {
  // set the speed at 5 rpm
  myStepper.setSpeed(5);
  // initialize the serial port
  Serial.begin(115200);
  servo1.attach(SERVO);
  servo1.write(pos);
}

void moveStepper(int steps, int time, int speed) {
  myStepper.setSpeed(speed);
  myStepper.step(steps);
  delay(time);
}

void moveServo(int start, int end, int ms) {
  if (start < end) {
    for(int posDegrees = start; posDegrees <= end; posDegrees++) {
      servo1.write(posDegrees);
      Serial.println(posDegrees);
      delay(ms);
    }
  } else {
    for(int posDegrees = start; posDegrees >= end; posDegrees--) {
      servo1.write(posDegrees);
      Serial.println(posDegrees);
      delay(ms);
    }
  }

  pos = end;
}

void gentleSweep() {
  moveServo(pos, 105, 20);
  moveStepper(-1024, 500, 10);
  servo1.write(20);
  moveStepper(1024, 500, 10);
}

void gentleBackAndForth() {

  moveServo(pos, 105, 20);
  moveStepper(-1024, 500, 10);
  moveStepper(1024, 500, 10);
}

void littleDance() {
  servo1.write(20);
  for (int i = 0; i < 4; i++) {
    moveServo(20, 30, 10);
    moveServo(30, 20, 10);
  }
  moveStepper(-1024, 500, 15);
  for (int i = 0; i < 4; i++) {
    moveServo(20, 30, 10);
    moveServo(30, 20, 10);
  }
  moveStepper(1024, 500, 15);
}

void littleTappyTap() {
  moveStepper(-256, 500, 15);
  for (int i = 0; i < 4; i++) {
    servo1.write(150);
    moveServo(150, 100, 10);
  }
  servo1.write(20);
  moveStepper(-256, 500, 15);
  for (int i = 0; i < 4; i++) {
    servo1.write(68);
    moveServo(65, 20, 10);
  }
  moveStepper(512, 500, 15);

}

void littleFlourishTap() {
  moveStepper(-256, 500, 15);
  for (int i = 0; i < 4; i++) {
    servo1.write(150);
    moveServo(150, 100, 10);
  }
  moveServo(pos, 105, 10);
  moveStepper(-640, 500, 15);
  servo1.write(20);
  moveStepper(384, 500, 15);
  for (int i = 0; i < 4; i++) {
    servo1.write(68);
    moveServo(65, 20, 10);
  }
  moveStepper(512, 500, 15);

}

void loop() {

  randomSeed(millis());
  int choice = random(0,5);

  switch (choice) {
    case 0:
      littleTappyTap();
      break;
    case 1:
      gentleSweep();
      break;
    case 2:
      gentleBackAndForth();
      break;
    case 3:
      littleDance();
      break;
    case 4:
      littleFlourishTap();
      break;
    default:
      // This should never happen, but just in case
      break;
  }
}