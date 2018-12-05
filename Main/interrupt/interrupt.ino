#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

volatile long right_enc_count = 0;

volatile long left_enc_count = 0;

// goes digital pins go 0 1 2 3 4 5 6 7
// 2 and 3 are interrupt pins
// left wheel takes 1 for leftOutputB and 2 for leftOutputA
// right wheel takes 3 for RightoutpuA and 4 for rightoutputB??? i think
// the right side IR closest to the front goes to 3, the IR closest to the back goes to 4

#define rightOutputA 3
#define rightOutputB 5

//the left side closest to the front is in pin 2, the ir further in the back is in pin 1
#define leftOutputA 2
#define leftOutputB 6

String inData = "";


void setup() {
  //pin 2 is interrupt int 0
  //pin 3 is interrupt int 1
  
  //md init overwrite pin 4, have to set it first
  md.init();

  attachInterrupt(0,left_encoder_isr, CHANGE);
  attachInterrupt(1,right_encoder_isr, CHANGE);
  pinMode(rightOutputA, INPUT);
  pinMode(rightOutputB, INPUT);
  pinMode(leftOutputA, INPUT);
  pinMode(leftOutputB, INPUT);

  Serial.begin(115200);

  // wait until serial is ready
  while(!Serial);

  //Serial.println("0,0");
  //md.setSpeeds(200,200);
   //md.setM2Speed(200);
  //stopIfFault();    
}

void loop() {
    // get data from serial in
  while (Serial.available() > 0){
        char rec = Serial.read();
        inData += rec; 
        // Process message when new line character is recieved
        if (rec == '\n')
        {     
            //Serial.print(inData);
            // extract lpwm and rpwm from the string
            //Serial.println("goes in if loop");
            int lpwm = inData.substring(0,inData.indexOf(',')).toInt();
            int start = inData.indexOf(',');
            int end_pt = inData.indexOf('\n');
            int rpwm = inData.substring(start+1, end_pt).toInt();

            //Serial.println("setting wheels to" + String(lpwm));
            //Serial.println("setting wheels to" + String(rpwm));
            md.setM2Speed(lpwm);
            stopIfFault();
            md.setM1Speed(rpwm);
            stopIfFault();

            
            
            inData = ""; // Clear recieved buffer

            //break incase new stuff comes and we're just stuck here
            break;
        }
      
    }
    // update_wheels();
    // update_cord();

    // String cord_vals = String(x_cord) + "," + String(y_cord) + "," + String(theta);
 //   Serial.println(String(left_enc_count) + ","+String(right_enc_count));
    }
//}
// motors
void stopIfFault(){
  if (md.getFault())
  {
    while(1){
        Serial.println("fault");
    }
  }
}
void set_lwheel(int speed){
  md.setM2Speed(speed);
  stopIfFault();
}

// rwheel m1
void set_rwheel(int speed){
  md.setM1Speed(speed);
  stopIfFault();

}

// 2 and 6
void left_encoder_isr() {
    static int8_t left_lookup_table[] = {0,0,0,-1,0,0,1,0,0,1,0,0,-1,0,0,0};
    static uint8_t left_enc_val = 0;
    //int countL = 0;
    //countL++;
    left_enc_val = left_enc_val << 2;
    //PIND reads all pin inputs from pins 0 to 7, our pins of interest are pins 3 and 4 for the left wheel
    uint8_t temp = 0;
    temp = (PIND >> 2) & 0b1;
    temp = temp | (PIND >> 5 & 0b10);
    left_enc_val = left_enc_val | temp;
    left_enc_count = left_enc_count + left_lookup_table[left_enc_val & 0b1111];
    //if(countL % 3 == 0){
      Serial.println(String(left_enc_count) + ","+String(right_enc_count));
    //}
}

// 3 and 5
void right_encoder_isr() {
    static int8_t lookup_table[] = {0,0,0,-1,0,0,1,0,0,1,0,0,-1,0,0,0};
    static uint8_t right_enc_val = 0;
    //int countR = 0;
    //countR++;
    right_enc_val = right_enc_val << 2;
    //PIND reads all pin inputs from pins 0 to 7, our pins of interest are pins 3 and 4 for the right wheel
    uint8_t temp = 0;
    temp = (PIND >> 3) & 0b1;
    temp = temp | (PIND >> 4 & 0b10);
    right_enc_val = right_enc_val | temp;
    right_enc_count = right_enc_count + lookup_table[right_enc_val & 0b1111];
    // Serial.println("Right Counter: " + String(right_enc_count));
    //if(countR % 3 == 0){
     // Serial.println(String(left_enc_count) + ","+String(right_enc_count));
   // }
    Serial.println(String(left_enc_count) + ","+String(right_enc_count));
}
