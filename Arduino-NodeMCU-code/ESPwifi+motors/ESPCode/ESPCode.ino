#include <ESP8266WiFi.h>
#include <AFMotor.h>
//included all files

//now initialize the motors
int rmp = 1; //right motor pin
int lmp = 2; //left motor pin
AF_DCMotor right_motor(rmp);
AF_DCMotor left_motor(lmp);
Servo servo_motor;

//initialize the wifi client and server
WiFiClient client;
WiFiServer server(80); //80 is the port number


//initialize variables to store the input from wifi
char message_from_pc[32] = {0};
int i1 = 0; //integer1
int i2 = 0; //integer2
int sp = 0; //servo position

void setup() {
  // begin the serial monitor and setup the motors
  Serial.begin(9600);
  right_motor.setSpeed(200);
  right_motor.run(RELEASE);
  left_motor.setSpeed(200);
  left_motor.run(RELEASE);
  servo_motor.attach(10);
  servo_motor.write(0);

  //begin the wifi connection
  WiFi.begin("7star", "00000000"); //connect to wifi
  while (WiFi.status() != WL_CONNECTED) //if connected to wifi move further
    {delay(500);
     Serial.print("*");} 
  Serial.println();
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: ");
  Serial.println(WiFi.localIP());
  server.begin();} //start server

void loop() {
  //first receive message from wifi connection
  client = server.available(); //if a request is made, this turns true
  if (client == 1)
    Serial.println("server avail");
    {String request = client.readStringUntil('\n');
    request.trim(); 
    Serial.println(request);}

}
