#include <ESP8266WiFi.h>
#include<SoftwareSerial.h>

//define the client and server
WiFiClient client;
WiFiServer server(80);
//define the communicator to arduino
SoftwareSerial ESP8266Comms(D2, D3);

void setup() 
  {Serial.begin(9600); //begin serial monitor
  ESP8266Comms.begin(9600); //begin communicator
  pinMode(D1, INPUT); 
  pinMode(D2, OUTPUT);
  WiFi.begin("7star", "00000000"); //connect to wifi
  while (WiFi.status() != WL_CONNECTED) //if connected to wifi move further
    {delay(500);
     Serial.print("*");} 
  Serial.println();
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());
  server.begin();} //start server

void loop() 
  {client = server.available(); //if a request is made, this turns true
  if (client == 1)
    Serial.println("server avail");
    {String request = client.readStringUntil('\n');
    request.trim(); 
    Serial.println(request);
    ESP8266Comms.println(request);}} //send data to arduino
