#define LeftoutputA 6
#define LeftoutputB 5
#define RightoutputA 3
#define RightoutputB 2

int leftCurrentState;
int leftLastState;  
int rightCurrentState;
int rightLastState;

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

void update_cord(){
  double SLeft = delta_left;
  double SRight = delta_right;
  //double WBase = 3.55379 ; //cm 
  double WBase = 18;
  double Dx=(SLeft+SRight)/2;
  double DTheta=atan2((SRight-SLeft)/2,WBase/2);
  theta+=DTheta;
  x_cord += Dx*cos(theta);
  y_cord +=Dx*sin(theta);
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
}

void setup(){
  
  Serial.begin(115200);
  while(!Serial);
  Serial.setTimeout(1000000); 
  //motors

  //IR sensors
  pinMode (LeftoutputA,INPUT);
  pinMode (LeftoutputB,INPUT);
  pinMode (RightoutputA, INPUT);
  pinMode (RightoutputB, INPUT);
  leftLastState = digitalRead(LeftoutputA);
  rightLastState = digitalRead(RightoutputA);

}

void loop(){
   update_wheels();
   update_cord();

   String cord_vals = String(x_cord) + "," + String(y_cord) + "," + String(theta);
   Serial.println(cord_vals);
}
