#include <Stepper.h>

int StepsPerRevolution = 2048;
int MotSpeed = 10;
int dt = 50;
Stepper MyStepper(StepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  MyStepper.setSpeed(MotSpeed);

}

void loop() {
  // put your main code here, to run repeatedly:
  MyStepper.step(StepsPerRevolution);
  delay(dt);
  MyStepper.step(-StepsPerRevolution);
  delay(dt);

}
