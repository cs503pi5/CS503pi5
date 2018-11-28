
volatile long right_enc_count = 0;
volatile long left_enc_count = 0;

// goes digital pins go 0 1 2 3 4 5 6 7
// 2 and 3 are interrupt pins
// left wheel takes 1 for leftOutputB and 2 for leftOutputA
// right wheel takes 3 for RightoutpuA and 4 for rightoutputB??? i think
// the right side IR closest to the front goes to 3, the IR closest to the back goes to 4
#define rightOutputA 3
#define rightOutputB 4

//the left side closest to the front is in pin 2, the ir further in the back is in pin 1
#define leftOutputA 2
#define leftOutputB 1


void setup() {
  // put your setup code here, to run once:

  //pin 2 is interrupt int 0
  //pin 3 is interrupt int 1
  attachInterrupt(0,left_encoder_isr, CHANGE);
  attachInterrupt(1,right_encoder_isr, CHANGE);
  pinMode(rightOutputA, INPUT);
  pinMode(rightOutputB, INPUT);
  pinMode(leftOutputA, INPUT);
  pinMode(leftOutputB, INPUT);
  
//  digitalWrite(leftOutputA, HIGH);
  Serial.begin(115200);
  Serial.println("Starting..");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(1);
}

void left_encoder_isr() {
    static int8_t left_lookup_table[] = {0,0,0,-1,0,0,1,0,0,1,0,0,-1,0,0,0};
    static uint8_t left_enc_val = 0;
    
    left_enc_val = left_enc_val << 2;
    //PIND reads all pin inputs from pins 0 to 7, our pins of interest are pins 3 and 4 for the left wheel
    left_enc_val = left_enc_val | ((PIND & 0b110) >> 1);
    Serial.print(left_enc_val);
    left_enc_count = left_enc_count + left_lookup_table[left_enc_val & 0b1111];
    Serial.println("Left Counter: " + String(left_enc_count));
}


void right_encoder_isr() {
  
  static int8_t lookup_table[] = {0,0,0,-1,0,0,1,0,0,1,0,0,-1,0,0,0};
    static uint8_t right_enc_val = 0;
    
    right_enc_val = right_enc_val << 2;
    //PIND reads all pin inputs from pins 0 to 7, our pins of interest are pins 3 and 4 for the right wheel
    right_enc_val = right_enc_val | ((PIND & 0b11000) >> 3);
    right_enc_count = right_enc_count + lookup_table[right_enc_val & 0b1111];
    Serial.println("Right Counter: " + String(right_enc_count));
}
