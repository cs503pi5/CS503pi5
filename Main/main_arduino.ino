#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;

void setup()
{
  Serial.begin(115200);
  Serial.println("Dual MC33926 Motor Shield");
  md.init();
}
