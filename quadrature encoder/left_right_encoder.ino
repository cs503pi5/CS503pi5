
 #define outputL1 3
 #define outputL2 4


 #define outputR1 2
 #define outputR2 5
 
 int left_counter = 0; 
 int right_counter = 0; 

 
 int lState;
 int lLastState;  

 int rState;
 int rLastState;  
 
 void setup() { 
   pinMode (outputL1,INPUT);
   pinMode (outputL2,INPUT);

   pinMode (outputR1,INPUT);
   pinMode (outputR2,INPUT);
   
   Serial.begin (9600);
   Serial.println("starting..");

   lLastState = digitalRead(outputL1);   
   rLastState = digitalRead(outputR1);  
 } 
 void loop() { 
  
   lState = digitalRead(outputL1);
   
   if (lState != lLastState){     
     if (digitalRead(outputL2) != lState) { 
       left_counter ++;
     } else {
       left_counter --;
     }
     Serial.print("Position: ");
     Serial.println((float)left_counter/20L);
   } 
   lLastState = lState;

  rState = digitalRead(outputR1);
   
   if (rState != rLastState){     
     if (digitalRead(outputR2) != rState) { 
       right_counter ++;
     } else {
       right_counter --;
     }
     Serial.print("Position: ");
     Serial.println((float)right_counter/20L);
   } 
   rLastState = rState;
   
 }
