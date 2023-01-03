#include <ESP8266WiFi.h>

int rmp = 5; //D1
int rmg = 0; //D3
int lmp = 4; //D2
int lmg = 2; //D4
#define enc1a 14 //D5
#define enc1b 12 //D6
int ea_reading;
int eb_reading;
int total_a_readings;
int a_previous_state = 0;
int na = 0;
float rotations_a = 0.0;
int changes_per_rev = 1000;
int va; 

void setup() {
  Serial.begin(9600);
  pinMode(rmp, OUTPUT);
  pinMode(lmp, OUTPUT);
  pinMode(enc1a, INPUT);
  pinMode(enc1b, INPUT);
}

void read_encoder(int pin){
  int pin_state = digitalRead(pin);
  if (pin_state!=a_previous_state){
    na = na+1;
    if(na>changes_per_rev){
      na = 0;
      rotations_a = rotations_a+1;
      Serial.println(rotations_a);
    }
  }
  a_previous_state = pin_state;
}

void loop() {
  // put your main code here, to run repeatedly:
  read_encoder(enc1a);
  digitalWrite(rmp, 100);
  digitalWrite(lmp, 100);  
}
