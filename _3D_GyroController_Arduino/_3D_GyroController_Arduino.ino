/*
 * Created by:  Noureddine Ait Said
 * Website:     github.com/noureddine-as
 * E-mail:      noureddine.asni@gmail.com
 * 
 */

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"


#define MAX_16BIT       (32768.0)
#define LED_PIN         13
#define SIZE            5


int16_t gx, gy, gz, deg_x, deg_y, deg_z;
int32_t t, t1, t2, omegaX, omegaY, omegaZ;
int gyro_config;
bool blinkState = false;
MPU6050 accelgyro;


void setup() {
  Wire.begin();
  Serial.begin(9600);
  accelgyro.initialize();

//accelgyro.setFullScaleGyroRange(0);
  gyro_config = accelgyro.getFullScaleGyroRange();

  switch (gyro_config) {
    case 0:
        gyro_config = 250; break;
    case 1: 
        gyro_config = 500;  break;
    case 2: 
        gyro_config = 1000; break;
    case 3: 
        gyro_config = 2000; break;
    default:  
        gyro_config = 250; break ;
  }

  pinMode(LED_PIN, OUTPUT);
  t = millis();

}


void loop() {
  
  t1 = millis();

  for(int i=0; i<SIZE; i++){
     accelgyro.getRotation(&gx, &gy, &gz);
     omegaX += gx;
     omegaY += gy;
     omegaZ += gz;
     delay(5);
  }
  // Calculate the mean
  omegaX /= SIZE;     omegaY /= SIZE;    omegaZ /= SIZE;

  t2 = millis();

  omegaX = (omegaX * gyro_config)/(MAX_16BIT);
  omegaY = (omegaY * gyro_config)/(MAX_16BIT);
  omegaZ = (omegaZ * gyro_config)/(MAX_16BIT); 

  // Angular displacements in degrees
  deg_x = omegaX * (t2 - t1) * PI/(180.0);
  deg_y = omegaY * (t2 - t1) * PI/(180.0);
  deg_z = omegaZ * (t2 - t1) * PI/(180.0);


  Serial.print(deg_x); Serial.print(":");
  Serial.print(deg_y); Serial.print(":");
  Serial.println(deg_y); 


  // blink LED to indicate activity
  if(millis() - t > 1000)
  {
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
    t = millis();
  }
}

