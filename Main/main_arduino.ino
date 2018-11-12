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
double x_cord = 0.0; 
double y_cord = 0.0;
double theta = 0.0;
double delta_left;
double delta_right;
double v_left_ref;
double v_right_ref;
double duration_pad;

// updates read world cord
void update_cord(){
  double SLeft = delta_left;
  double SRight = delta_right;
  double WBase = 3.55379 ; //cm 
  double Dx=(SLeft+SRight)/2;
  double DTheta=atan2((SRight-SLeft)/2,WBase/2);
  theta+=DTheta;
  x_cord += Dx*cos(theta);
  y_cord +=Dx*sin(theta);
}


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
  Serial.println(speed);
  Serial.print("start set speed");
  md.setM1Speed(speed);
  stopIfFault();
  Serial.println("end set");

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

  // if no spokes move add on to this pad. In case wheels are too slow for sampling rate
  if (right_spoke_counter== 0 && left_spoke_counter ==0){
    duration_pad += millis() - start_millis;
  }
  else{
    
  }
  long end_millis = millis();
  double duration = (double)(end_millis - start_millis + duration_pad)/1000;
  duration_pad = 0.0;
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
  while(!Serial);
  Serial.setTimeout(10000000000000000000); 
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

//updates current velocities of each wheel and updates distance of each wheel

void loop(){
  //if stuff in the serial port
  if (Serial.available()){
    int variable = Serial.readStringUntil(' ').toInt();
    Serial.println(variable);
    if (variable == 1){
      int PWM_value_L = Serial.readStringUntil('\n').toInt();
      set_lwheel(PWM_value_L);
    }
    else if(variable ==2){
      int PWM_value_R = Serial.readStringUntil('\n').toInt();
        Serial.println(PWM_value_R);
        set_rwheel(PWM_value_R);
        
    }
      //send over value for velocity of left wheel reference
      // example "3 VREF_VAL\n"
    else if (variable == 3){
      double val_l = Serial.readStringUntil('\n').toDouble();
      v_left_ref = val_l;
    }
    else if (variable == 4){
      double val_r = Serial.readStringUntil('\n').toDouble();
      v_right_ref = val_r;
    }
  }
  update_wheels();
  update_cord();

  String cord_vals = String(x_cord) + "," + String(y_cord) + "," + String(theta);
  Serial.println((cord_vals);

  // loop to get a number of counts and then send counter over to pi counter
  
}