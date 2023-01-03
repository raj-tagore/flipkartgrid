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
  myservo.attach(13);
  myservo.write(0);
}

void loop() {
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
    //--------------- we now have 4 integers from the udp comms
    //--------------- 1 is eject command. 2 and 3 are motor speeds. 4 is angle turn
    if (integer0!=0){
      eject();
    }
    else if (integer3!=0){
      turn();
    }
    else {
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
      delay(600);                       // waits 600 ms for the servo to reach the position
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

void turn(){
  if (integer3>0){
    //turn left
      analogWrite(lmp, integer3);
      digitalWrite(lmg, LOW);
      analogWrite(rmp, integer3);
      digitalWrite(rmg, HIGH);
  }
  else if (integer3<0){
    //turn right
      analogWrite(lmp, -integer3);
      digitalWrite(lmg, HIGH);
      analogWrite(rmp, -integer3);
      digitalWrite(rmg, LOW);
  }
}
