int counter = 0;
int wrong_counter = 0;
volatile long enc_count = 0;

#define leftOutputA 2
#define leftOutputB 3

void setup() {
  // put your setup code here, to run once:
  attachInterrupt(0,encoder_isr, CHANGE);
  attachInterrupt(1,encoder_isr, CHANGE);
  pinMode(leftOutputA, INPUT);
  pinMode(leftOutputB, INPUT);
//  digitalWrite(leftOutputA, HIGH);
  Serial.begin(9600);
  Serial.println("Starting..");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(1);
}

void encoder_isr() {
  
  static int8_t lookup_table[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};
    static uint8_t enc_val = 0;
    
    enc_val = enc_val << 2;
    enc_val = enc_val | ((PIND & 0b1100) >> 2);
 
    enc_count = enc_count + lookup_table[enc_val & 0b1111];

    if(lookup_table[enc_val & 0b1111]==1) {
      counter++;
      Serial.print("Left Counter: ");
      Serial.println(counter/2);
    }
        if(lookup_table[enc_val & 0b1111]==0) {
      wrong_counter++;
     // Serial.print("Wrong Counter: ");
     // Serial.println(wrong_counter);
    }
    
//    Serial.print("Left Counter: ");
//    Serial.println(counter);
//    Serial.print("enc_count: ");
//    Serial.println(enc_count);
}
