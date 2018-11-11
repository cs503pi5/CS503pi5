#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

#define outputL1 6
#define outputL2 5


#define outputR1 3
#define outputR2 2

int lState;
int lLastState;  

int rState;
int rLastState;  

void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
    while(1);
  }
}


void setup() { 
  pinMode (outputL1,INPUT);
  pinMode (outputL2,INPUT);

  pinMode (outputR1,INPUT);
  pinMode (outputR2,INPUT);
 
  Serial.begin (9600);
  Serial.println("starting..");
  Serial.println("PWN, left wheel, right wheel");

  lLastState = digitalRead(outputL1);   
  rLastState = digitalRead(outputR1);  
  md.init();

} 
void loop() { 
  for (int pwm_count = 150; pwm_count < 300; pwm_count = pwm_count + 5){
    //inital sets
    long start_millis = millis();
    md.setM1Speed(pwm_count);
    md.setM2Speed(pwm_count);
    int left_counter = 0; 
    int right_counter = 0; 

    stopIfFault();
    while(left_counter + right_counter < 100){
      lState = digitalRead(outputL1);
       
      if (lState != lLastState){     
        if (digitalRead(outputL2) != lState) { 
          left_counter ++;
        } else {
          left_counter --;
        }
        // Serial.print("Position: " + String(((float)left_counter/20L)));
      } 
      lLastState = lState;
    
      rState = digitalRead(outputR1);
       
      if (rState != rLastState){     
        if (digitalRead(outputR2) != rState) { 
          right_counter ++;
          } else {
          right_counter --;
          }
        // Serial.println("Position: " +  String(((float)right_counter/20L)));
        } 
      rLastState = rState;
    } 
    
    long end_millis = millis();
    double duration = (double)(end_millis - start_millis)/1000;
    // Serial.println(duration);
    double circumference = 22.32914; //cm
    double spoke_length = circumference / 20.0;

    double r_cps = (spoke_length * right_counter) / duration;
    double l_cps = (spoke_length * left_counter) / duration;
 
    // Serial.println("For pwm = " + String(pwm_count));
    // Serial.println("Right wheel centimeters per second: " + String(r_cps));
    // Serial.println("Light wheel centimeters per second: " + String(l_cps));
    Serial.print(String(pwm_count)+",");
    Serial.print(String(l_cps)+",");
    Serial.println(String(r_cps));
  }
}
