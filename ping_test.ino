//Got this code from Arduino Cookbook by Michael Margolis
const int pingPin = 5;

void setup()
{
  Serial.begin(9600);
 
  
}

void loop()
{
  int cm = ping(pingPin);
  Serial.println(cm);
  delay(10);
}


int ping(int pingPin)
{
  int duration, cm;
  
  //Sound ping triggered by HIGH pulse of 2 us or more
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  
  //times how long it takes sound to come back
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);
  
  cm = microsecondsToCentimeters(duration);
  return cm;
}

long microsecondsToCentimeters(float microseconds)
{
  //speed of sound is 29 microseconds for 1 cm and ping 
  //travels there and back so divide by 2
  return (microseconds / 29) / 2;
}

