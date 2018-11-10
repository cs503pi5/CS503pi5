/*5ection of the PING))) attached to digital pin 7

  created 3 Nov 2008
  by David A. Mellis
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Ping
*/

// this constant won't change. It's the pin number of the sensor's output:
const int pingPin = 7;

float count = 0;
float total_distance = 0;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
}

void loop() {
  // establish variables for duration of the ping, and the distance result
  // in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH pulse
  // whose duration is the time (in microseconds) from the sending of the ping
  // to the reception of its echo off of an object.
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);

  // convert the time into a distance
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);
  
  // float length_inches = 12;
  // float length_cm = length_inches * 2.54;
  // float length_meter = length_cm / 100;
  // // Serial.println("Duraton for " + String(length_cm) + ": " + String(duration));
  // float distance = length_meter * 2.0; // since you travel twice
  // float time_seconds = duration / 1000000.0; // 1mu is 1 millionth of a second
  // float speed = distance/time_seconds;

  // Serial.println("Derived speed m/s: " + String(speed));
  // Serial.println("Ping's calculated distance: " + String(cm/(float)100) + "m");
  // Serial.println();
  
  count += 1.0;
  // float meters = (float)cm/(float)100;
  total_distance += (float)cm;
  
  Serial.print("Average of distance after "+String(count)+" measurements: ");
  Serial.println(String(total_distance/count) + "cm");
  delay(1);
}

long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are 73.746
  // microseconds per inch (i.e. sound travels at 1130 feet per second).
  // This gives the distance travelled by the ping, outbound and return,
  // so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the object we
  // take half of the distance travelled.
  return microseconds / 29 / 2;
}
