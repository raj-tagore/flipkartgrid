#include<ESP8266WiFi.h>
#include<WiFiUDP.h>
#include<Servo.h>

//----------------Both motors power and ground
int rmp = 4; //RMP = 4 LMP = 5 
int rmg = 2;
int lmp = 5;
int lmg = 0;

//----------------Servo Motor vars
Servo myservo;
int pos = 0;

//---------------Both encoders
int encL = 14; //D5
int encR = 12; //D6

int l_prev_st = 0;
long int l_no = 0; //No of readings of L
int l_prev_no = 0;
int l_diff = 0;
int l_speed = 0;
int l_error = 0;
int l_prev_error = 0;
int l_tot_error = 0;

int r_prev_st = 0;
long int r_no = 0; //No of readings of R
int r_prev_no = 0;
int r_diff = 0;
int r_speed = 0;
int r_error = 0;
int r_prev_error = 0;
int r_tot_error = 0;

int t1;
int t3;

float kp = 0.3;
float kd = 0.1;
float ki = 0.05;


//----------------define the wifi variables
WiFiClient client;
WiFiServer server(80);
WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[256];
char replyPacket[256];

//----------------vars to receive and parse data
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
int integer0 = 0;
int integer1 = 0;
int integer2 = 0;
int integer3 = 0;
int sp = 200;

void setup() {
  Serial.begin(9600);

  //---------------setup wifi
  WiFi.begin("7star", "00000000"); //connect to wifi
  while (WiFi.status() != WL_CONNECTED) //if connected to wifi move further
    {delay(500);
     Serial.print("*");} 
  Serial.println();
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());
  Udp.begin(localUdpPort);
  
  //---------------setup pins
  pinMode(rmp, OUTPUT);
  pinMode(rmg, OUTPUT);
  pinMode(lmp, OUTPUT);
  pinMode(lmg, OUTPUT);
  pinMode(encL, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encL), l_increment, CHANGE);
  pinMode(encR, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encR), r_increment, CHANGE);
  myservo.attach(13);
  myservo.write(0);

  l_prev_st = digitalRead(encL);
  r_prev_st = digitalRead(encR);

  t1 = millis();
  t3 = millis();
}

void loop() {
    //--------------- we now have 4 integers from the udp comms
    //--------------- 1 is eject command. 2 and 3 are motor speeds. 4 is angle turn
    if (integer0!=0){
      eject();
    }
    else if (integer3!=0){
      turn();
    }
    else {
      int packetSize = Udp.parsePacket();
    if (packetSize){
      Serial.printf("received %d bytes from %s port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if(len>0){
        incomingPacket[len] = '\0';
      }
      //Serial.printf("UDP Packet contains %s\n", incomingPacket);
    
      //--------------enter loop code here
      parseIncomingPacket();
      splitData();
    }
      if(integer1>0&&integer2>0){ 
        pid_control();
      }
      runmotors();
   }
}

void parseIncomingPacket(){
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '[';
    char endMarker = ']';
    char rc;
    int len = strlen(incomingPacket);
    for (int i=0; i<len; i++){
      rc = incomingPacket[i];
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
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
    Serial.println(receivedChars);
}

void splitData() {      // split the data into its parts
    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(receivedChars,",");      // get the first part
    integer0 = atoi(strtokIndx);             
 
    strtokIndx = strtok(NULL, ",");  // this continues where the previous call left off
    integer1 = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    integer2 = atoi(strtokIndx); 

    strtokIndx = strtok(NULL, ",");
    integer3 = atoi(strtokIndx);
}

void showParsedData() {
    Serial.print("Integer0 ");
    Serial.println(integer0);
    Serial.print("Integer1 ");
    Serial.println(integer1);
    Serial.print("Integer2 ");
    Serial.println(integer2);
    Serial.print("Integer3 ");
    Serial.println(integer3);
}

void eject(){
  if (integer0>0){
      myservo.write(90);              // tell servo to go to position in variable 'pos'
      delay(600);                       // waits 15 ms for the servo to reach the position
      Serial.println("ejecting");      // goes from 180 degrees to 0 degrees
      myservo.write(0);              // tell servo to go to position in variable 'pos'
      delay(600); 
    }
}

void runmotors(){
  
  if (integer2>=0){
      analogWrite(rmp, integer2);
      digitalWrite(rmg, HIGH);
    }
    else{
      analogWrite(rmp, -integer2);
      digitalWrite(rmg, LOW);
    }
    if (integer1>=0){
      analogWrite(lmp, integer1);
      digitalWrite(lmg, HIGH);
    }
    else{
      analogWrite(lmp, -integer1);
      digitalWrite(lmg, LOW);
    }
}

ICACHE_RAM_ATTR void l_increment(){
  l_no = l_no+1;
}

ICACHE_RAM_ATTR void r_increment(){
  r_no = r_no+1;
}

void get_speed(){
  int t2 = millis();
  if (t2-t1>100){
    int l_speed = l_no-l_prev_no;
    int r_speed = r_no-r_prev_no;
    Serial.print(l_speed);
    Serial.print("--L (ticks per 100 millis) R--");
    Serial.println(r_speed);
    l_prev_no = l_no;
    r_prev_no = r_no;
    t1 = t2;
  }  
}

void pid_control(){
  int t4 = millis();
  if (t4-t3>100&&integer1!=0){
    int l_speed = l_no-l_prev_no;
    int r_speed = r_no-r_prev_no;
    l_prev_no = l_no;
    r_prev_no = r_no;
    t3 = t4;
    
    r_error = r_speed - l_speed;
    
    integer1 = integer1 - l_error*kp - l_prev_error*kd - l_tot_error*ki;
    integer2 = integer2 - r_error*kp - r_prev_error*kd - r_tot_error*ki;
    l_prev_error = l_error;
    l_tot_error = l_tot_error + l_error;
    r_prev_error = r_error;
    r_tot_error = r_tot_error + r_error;

    if (integer1>255){
      integer1 = 255;
    }
    else if (integer1<90){
      integer1 = 90;
    }
    if (integer2>255){
      integer2 = 255;
      l_error = -r_error;
    }
    else if (integer2<90){
      integer2 = 90;
    }

    Serial.print(l_speed);
    Serial.print("::L (speed) R::");
    Serial.println(r_speed);
    Serial.print(l_error);
    Serial.print("::L (error) R::");
    Serial.println(r_error);
    Serial.print(integer1);
    Serial.print("::L (power) R::");
    Serial.println(integer2);
  }
}

void turn(){
  l_prev_no = l_no;
  r_prev_no = r_no;
  int pulses_per_rotation = 3350;
  if (integer3>0){
    float fraction = (float)integer3/(float)360;
    //turn left
    while(l_no-l_prev_no<(fraction*pulses_per_rotation)){
      Serial.print(l_no);
      Serial.print(", ");
      Serial.print(l_prev_no);
      Serial.print(", ");
      Serial.println(fraction);
      analogWrite(lmp, sp);
      digitalWrite(lmg, LOW);
      analogWrite(rmp, sp);
      digitalWrite(rmg, HIGH);
    }
    runmotors();
  }
  else if (integer3<0){
    float fraction = (float)-integer3/(float)360;
    //turn right
    while(r_no-r_prev_no<(fraction*pulses_per_rotation)){
      analogWrite(lmp, sp);
      digitalWrite(lmg, HIGH);
      analogWrite(rmp, sp);
      digitalWrite(rmg, LOW);
    }
    runmotors();
  }
  integer3 = 0;
}
