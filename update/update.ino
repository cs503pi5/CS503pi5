
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  
   
}


 void update(double x, double y, double Theta){
  double SLeft;
  double SRight;
  double WBase;#Wheel_base
  double Dx=(SLeft+Sright)/2
  double DTheta=atan2((SRight-SLeft)/2,WBase/2);
  Theta+=DTheta;
  x += Dx*cos(Theta);
  y +=Dx*sin(Theta);
  return;
 }
