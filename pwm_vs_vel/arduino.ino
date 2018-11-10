
 #define outputL1 6
 #define outputL2 5


 #define outputR1 3
 #define outputR2 2
 
 int left_counter = 0; 
 int right_counter = 0; 

 
 int lState;
 int lLastState;  

 int rState;
 int rLastState;  
 long start_millis;

 void setup() { 
   pinMode (outputL1,INPUT);
   pinMode (outputL2,INPUT);

   pinMode (outputR1,INPUT);
   pinMode (outputR2,INPUT);
   
   Serial.begin (9600);
   Serial.println("starting..");

  start_millis = millis();
   lLastState = digitalRead(outputL1);   
   rLastState = digitalRead(outputR1);  
 } 
 void loop() { 
  
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
  Serial.println(duration);
  right_counter = 0;
  left_counter = 0;
 }
