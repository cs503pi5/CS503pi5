#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

double last_error;

double Get_PD_velocity_approximation(actual_error, desired_error, k_constant = 0.5, b_constant = 0.001){
  double delta_v = (-1*k_constant*actual_error) - (b_constant*(actual_error - last_error));
  last_error = actual_error;
  return delta_v;
}

// motors
void stopIfFault(){
  if (md.getFault())
  {
    while(1){
        Serial.println("fault");
    }
  }
}

void set_both_wheel_speeds(int speed){
  md.setM1Speed(speed);
  md.setM2Speed(speed);
  stopIfFault();
}

// IR sensor
#define LeftoutputA 6
#define LeftoutputB 5
#define RightoutputA 3
#define RightoutputB 2
int leftCurrentState;
int leftLastState;  
int rightCurrentState;
int rightLastState;

void setup(){
  Serial.begin(9600);

  //motors
  md.init();

  //IR sensors
  pinMode (LeftoutputA,INPUT);
  pinMode (LeftoutputB,INPUT);
  pinMode (RightoutputA, INPUT);
  pinMode (RightoutputB, INPUT);
  leftLastState = digitalRead(LeftoutputA);
  rightLastState = digitalRead(RightoutputA);
}

void loop(){

  // IR sensor

  // loop to get a number of counts and then send counter over to pi counter
  int left_spoke_counter = 0; 
  int right_spoke_counter = 0;
  for (int ir_counter = 0; ir_counter< 100; ir_counter++){
    leftCurrentState = digitalRead(LeftoutputA); // Reads the "current" state of the outputA
    rightCurrentState = digitalRead(RightoutputA);
    // If the previous and the current state of the outputA are different, that means a Pulse has occured
    if (leftCurrentState != leftLastState){     
      // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
      if (digitalRead(LeftoutputB) != leftCurrentState) { 
        left_spoke_counter ++;
      } else {
        left_spoke_counter --;
      }
    }
    if (rightCurrentState != rightLastState){
      if (digitalRead(RightoutputB) != rightCurrentState) { 
        right_spoke_counter ++;
      } else {
        right_spoke_counter --;
      
    }

  }
  Serial.println("Left Position: " + String(left_spoke_counter)); 
  Serial.println("Right Position: " + String(right_spoke_counter)); 

  leftLastState = leftCurrentState; // Updates the previous state of the outputA with the current state
  rightLastState = rightCurrentState;
}
