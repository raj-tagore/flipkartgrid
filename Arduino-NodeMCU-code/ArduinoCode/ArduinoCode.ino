#include <AFMotor.h>
#include <Servo.h>
#include<SoftwareSerial.h>

AF_DCMotor rightmotor(3); 
AF_DCMotor leftmotor(4); //defining right and left motors
Servo myservo;
SoftwareSerial ArduinoComms(17, 18); //define arduino communicator A0 is pin 14

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
char messageFromPC[numChars] = {0};
int integer1 = 0;
int integer2 = 0;
int sp = 0;

int pos = 0;    // variable to store the servo position

boolean newData = false;

void setup() {
  Serial.begin(9600); // set up Serial library at 9600 bps
  ArduinoComms.begin(9600);
  Serial.println("both arduino comms and serial comms activated");
  rightmotor.setSpeed(200);
  rightmotor.run(RELEASE);
  leftmotor.setSpeed(200);
  leftmotor.run(RELEASE);
  myservo.attach(10);
  myservo.write(0);
}

void loop() {
  recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            // because strtok() used in parseData() replaces the commas with \0
        parseData();
        showParsedData();
        newData = false;
    }
  if (messageFromPC[1] == 'x'){
    rightmotor.setSpeed(0);
    leftmotor.setSpeed(0);
    myservo.write(0); 
    Serial.println("stopping");
  }
  else if (messageFromPC[1] == 'e'){
    myservo.write(90);              // tell servo to go to position in variable 'pos'
    delay(600);                       // waits 15 ms for the servo to reach the position
    Serial.println("ejecting");      // goes from 180 degrees to 0 degrees
    myservo.write(0);              // tell servo to go to position in variable 'pos'
    delay(600);                       // waits 15 ms for the servo to reach the position
  }
  else{
    moveDCMotors();
  }
}

void runrightmotor(int s){
      if(s>=0){
          rightmotor.run(FORWARD);
          rightmotor.setSpeed(s); 
      }
      else {
          rightmotor.run(BACKWARD);
          rightmotor.setSpeed(-s); 
      }
}

void runleftmotor(int s){
      if(s>=0){
          leftmotor.run(BACKWARD);
          leftmotor.setSpeed(s); 
      }
      else {
          leftmotor.run(FORWARD);
          leftmotor.setSpeed(-s); 
      }
}

void moveDCMotors(){
  runrightmotor(integer1);
  runleftmotor(integer2);
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '[';
    char endMarker = ']';
    char rc;

    while (ArduinoComms.available() > 0 && newData == false) {
        rc = ArduinoComms.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    integer1 = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    integer2 = atoi(strtokIndx); 

}

//============

void showParsedData() {
    Serial.print("Message ");
    Serial.println(messageFromPC);
    Serial.print("Integer1 ");
    Serial.println(integer1);
    Serial.print("Integer2 ");
    Serial.println(integer2);
}
