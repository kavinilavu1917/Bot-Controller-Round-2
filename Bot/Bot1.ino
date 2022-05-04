

// Node mcu version 3.0


#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Servo.h>
Servo MG995_Servo;

//Motor PINs
#define IN_1 D5
#define IN_2 D6
#define IN_3 D7
#define IN_4 D8


bool forward = 0;
bool backward = 0;
bool left = 0;
bool right = 0;
int Speed;

const char* auth="dcsdcsd52z5dedz5xad8";
const char* ssid = ""; // Write here your router's username
const char* password = ""; // Write here your router's passward
WiFiClient client_obj;
int count=0;
void setup(){
	Serial.begin(9600);
	//MG995_Servo.attach(3);
	WiFi.begin(ssid,password);
	while(WiFi.status()!=WL_CONNECTED){
		delay(500);
	}

	MG995_Servo.attach(3);

	pinMode(IN_1, OUTPUT);
	pinMode(IN_2, OUTPUT);
	pinMode(IN_3, OUTPUT);
	pinMode(IN_4, OUTPUT);
	pinMode(2, OUTPUT);

	/*
	socket communication with given host and port number 9488
	*/

	while (!client_obj.connect("192.168.43.9",9488)){
		Serial.println("connectionFailed");
	}

}

/*
Fliping Function
*/

void flip(){
	MG995_Servo.write(180); 
	//Turn clockwise at high speed
	delay(3000);
	//Turn left high speed
	MG995_Servo.write(0);
	delay(3000);
	client_obj.print("A");
}


//Forward Function
void carforward(){
	char delaycommand = client_obj.read();

	digitalWrite(IN_1, HIGH);
	digitalWrite(IN_2, LOW);
	digitalWrite(IN_3, HIGH);
	digitalWrite(IN_4, LOW);
	if (delaycommand=='X')
		delay(84);
	else if(delaycommand=='Y')
		delay(168);
	else if(delaycommand=='Z')
		delay(252);
	digitalWrite(IN_1, LOW);
	digitalWrite(IN_2, LOW);
	digitalWrite(IN_3, LOW);
	digitalWrite(IN_4, LOW);
	client_obj.print("A");
}

//Left Function
void carturnleft(){
	char delaycommand = client_obj.read();

	digitalWrite(IN_1, HIGH);
	digitalWrite(IN_2, LOW);
	digitalWrite(IN_3, LOW);
	digitalWrite(IN_4, HIGH);
	if (delaycommand=='X')
		delay(125);
	else if (delaycommand=='Y')
		delay(250);
	else if (delaycommand=='Z')
		delay(375);
	digitalWrite(IN_1, LOW);
	digitalWrite(IN_2, LOW);
	digitalWrite(IN_3, LOW);
	digitalWrite(IN_4, LOW);
	client_obj.print("A");
}

//Right Function
void carturnright(){
	char delaycommand = client_obj.read();

	digitalWrite(IN_1, LOW);
	digitalWrite(IN_2, HIGH);
	digitalWrite(IN_3, HIGH);
	digitalWrite(IN_4, LOW);
	if (delaycommand=='X')
		delay(125);
	else if (delaycommand=='Y')
		delay(250);
	else if (delaycommand=='Z')
		delay(375);
	digitalWrite(IN_1, LOW);
	digitalWrite(IN_2, LOW);
	digitalWrite(IN_3, LOW);
	digitalWrite(IN_4, LOW);
	client_obj.print("A");
}


void loop() {
	digitalWrite(2, HIGH);
	delay(1000);
	digitalWrite(2, LOW);
	delay(1000);

	if (count==0){
		client_obj.print("bot1");
		count++;
	}

	char command = client_obj.read();
	Serial.println(command);
	if (command=='F')
		carforward();
	else if(command=='L')
		carturnleft();
	else if(command=='R')
		carturnright();
	else if(command=='D'){
		client_obj.stop();
	else if(command=='E')
		flip();
}
