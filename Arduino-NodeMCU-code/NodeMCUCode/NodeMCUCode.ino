#include <ESP8266WiFi.h>
#include<SoftwareSerial.h>
#include<WiFiUDP.h>

//define the client and server
WiFiClient client;
WiFiServer server(80); 
SoftwareSerial ESP8266Comms(D2, D3); //define the communicator to arduino

WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[256];
char replyPacket[256];

void setup() 
  {Serial.begin(9600); //begin serial monitor
  ESP8266Comms.begin(9600); //begin communicator
  pinMode(D2, INPUT); 
  pinMode(D3, OUTPUT);
  WiFi.begin("7star", "00000000"); //connect to wifi
  while (WiFi.status() != WL_CONNECTED) //if connected to wifi move further
    {delay(500);
     Serial.print("*");} 
  Serial.println();
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());
  Udp.begin(localUdpPort);} //start server

void loop() 
  {
  int packetSize = Udp.parsePacket();
  if (packetSize){
    Serial.printf("received %d bytes from %s port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if(len>0){
      incomingPacket[len] = '\0';
    }
    Serial.printf("UDP Packet contains %s\n", incomingPacket);
    ESP8266Comms.print(incomingPacket);
  }
  } //send data to arduino
