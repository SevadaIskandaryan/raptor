/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-servo-motor
 */

#include <Servo.h>

Servo servo_x;  // create servo object to control a servo
Servo servo_y;
int pos_x = 0;
int pos_y = 0;
String msg;


void setup() {
  Serial.begin(9600);
  servo_y.attach(9);  // attaches the servo on pin 9 to the servo objectư
  servo_y.write(pos_x);   // rotate slowly servo to 0 degrees immediately
  servo_x.attach(10);  // attaches the servo on pin 9 to the servo objectư
  servo_x.write(pos_y); 
}

void loop() {

    if (Serial.available() > 0){
        msg = Serial.readString();
        int colonIndex = msg.indexOf(':');
        String x_str = msg.substring(0, colonIndex);
        String y_str = msg.substring(colonIndex+1);
        // 
        pos_x = x_str.toInt();
        pos_y = y_str.toInt();

        Serial.println(x_str + "_" + y_str);
        
        servo_y.write(pos_y);
        servo_x.write(pos_x);
        //delay(50); 
    }
    delay(500); 
}
