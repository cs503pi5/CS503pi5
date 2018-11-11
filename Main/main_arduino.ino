#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

// IR sensor
#define LeftoutputA 6
#define LeftoutputB 5
#define RightoutputA 3
#define RightoutputB 2
int leftCurrentState;
int leftLastState;  
int rightCurrentState;
int rightLastState;
double last_error;
double curr_left_wheel_cps;
double curr_right_wheel_cps;
double delta_left;
double delta_right;

// return delta velocities
double Get_PD_velocity_approximation(double actual_error, double desired_error, double k_constant = 0.5, double b_constant = 0.001){
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

// lwheel is m2
void set_lwheel(int speed){
  md.setM2Speed(speed);
  stopIfFault();
}

// rwheel m1
void set_rwheel(int speed){
  md.setM1Speed(speed);
  stopIfFault();
}
void update_wheels(){
  long start_millis = millis();

  int left_spoke_counter = 0; 
  int right_spoke_counter = 0;
  for (int ir_counter = 0; ir_counter< 1000; ir_counter++){
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
  long end_millis = millis();
  double duration = (double)(end_millis - start_millis)/1000;

  double circumference = 22.32914; //cm
  double spoke_length = circumference / 20.0;

  curr_right_wheel_cps = (spoke_length * right_spoke_counter) / duration;
  curr_left_wheel_cps = (spoke_length * left_spoke_counter) / duration;

  delta_right = spoke_length * right_spoke_counter;
  delta_left =  spoke_length * left_spoke_counter;


  leftLastState = leftCurrentState; 
  rightLastState = rightCurrentState;
}
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

  Serial.println('start');
  set_lwheel(10);
  set_rwheel(30);
  // set_lwheel(toint(Serial.readStringUntil('\n')));
  // set_rwheel(toint(Serial.readStringunitl('\n')));

}

//updates current velocities of each wheel and updates distance of each wheel


void loop(){
  // update_wheels()

  // loop to get a number of counts and then send counter over to pi counter
  
}
