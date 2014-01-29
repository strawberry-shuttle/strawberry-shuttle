//Got this code from Arduino Cookbook by Michael Margolis
const unsigned int pingPin = 5;
const unsigned int pingPin2 = 6;
const unsigned int MAX_DIST = 200; //Max distance in cm

//Don't edit
const unsigned int TIMEOUT_DIST = MAX_DIST*29*2; //Will change based on speed of sound, DO NOT USE IN PRODUCTION

void setup()
{
  Serial.begin(9600);
 
  
}

void loop()
{
  float  cm = ping(pingPin);
  //float  cm2 = ping(pingPin2);
 
  
  Serial.print(cm);
  Serial.print(", ");
  //Serial.print(" ");
  //Serial.print(cm2);
  //Serial.println("");

  delay(10);
}

/*
float ping2(unsigned int pingPin, unsigned int pingPin2)
{
  unsigned int duration;
  float cm;
  
  //Sound ping triggered by HIGH pulse of 2 us or more
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  
  //times how long it takes sound to come back
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH, TIMEOUT_DIST); //This will check up to 1.1m
  
  cm = microsecondsToCentimeters(duration);
  return cm;
}
*/
float ping(unsigned int pingPin)
{
  unsigned int duration;
  float cm;
  
  //Sound ping triggered by HIGH pulse of 2 us or more
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  
  //times how long it takes sound to come back
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH, TIMEOUT_DIST); //This will check up to 1.1m
  
  cm = microsecondsToCentimeters(duration);
  return cm;
}

float microsecondsToCentimeters(unsigned int microseconds)
{
  //speed of sound is 29 microseconds for 1 cm and ping 
  //travels there and back so divide by 2
  //Serial.println(microseconds);
  return (microseconds / 29.0) / 2;
}

