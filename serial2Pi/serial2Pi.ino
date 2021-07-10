#include <Servo.h>
// Declare the Servo pin 
int servoPin = 3; 
// Create a servo object 
Servo Servo1; 
void setup(){
 Serial.begin(9600);
 Servo1.attach(servoPin);
}

void loop(){
  if(Serial.available()>0){
   String data = Serial.readString();
   //String datas = &data[0];
   int str_len = data.length()+1;
   char char_array[str_len];
   String dam = "ad";
   int str_len1 = dam.length()+1;
   char char_array1[str_len1];
   dam.toCharArray(char_array1, str_len1);
   data.toCharArray(char_array, str_len);
   Serial.println(data[0]);
       if(data[0]==dam[0]){
     Servo1.write(45);
      }
      if(data[0]==dam[1]){
     Servo1.write(135);
      }
   }
}
