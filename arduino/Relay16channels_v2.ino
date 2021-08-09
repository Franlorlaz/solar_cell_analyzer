int incomingByte =0;
boolean out=HIGH;
boolean calib=LOW;

//const int outputPIN[] = {4,13,16,12,18,14,17,27,19,26,21,25,22,33,23,32}; //Pins for esp32
const int outputPIN[] = {A0,A1,A2,A3,A4,A5, 6, 5, 4, 3,12,11,10,9, 8, 7}; //Pins for arduino uno
// Associated Relay Nr  ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16)

const int outputPIN2 = 13;
 
// the setup routine runs once when you press reset:
void setup()  {
  // declare pins to be an output:
  for (byte i = 0; i < 16; i++) {
    pinMode(outputPIN[i], OUTPUT);
  }
  pinMode(outputPIN2, OUTPUT);
  for (byte i = 0; i < 16; i++) {
    digitalWrite(outputPIN[i], HIGH);
  }
  digitalWrite(outputPIN2, HIGH);
  Serial.begin(9600);
  
  Serial.println("Starting comunication");

  //test();
  
  Serial.println("Ready to work!");
}
 
// the loop routine runs over and over again forever:
void loop()  {
  if(Serial.available()>0){
    incomingByte = Serial.read();
//    incomingByte -= 65; // To start 0 as A ascii character

    if(incomingByte==255){
      calib = HIGH;
      calibration();
      Serial.println("enabled");
      return;
      }
    if(incomingByte==254){
      calib = LOW;
      calibration();
      Serial.println("disabled");
      return;
      }

    if(incomingByte>16){
      out=HIGH;
      incomingByte=incomingByte-17;
    }else{
      out=LOW;
    }
    
    out = out ^ calib; // Changing to calibration mode if necessary
    
    if(incomingByte>=0&&incomingByte<34){
    if(incomingByte==0){
      for(byte i = 0; i < 16; i++){
          digitalWrite(outputPIN[i],!out);// NOi and COMi (Dis)connected
        }
      Serial.print("All Relays' NO and COM ");
      if(out){
        Serial.println("Connected");
      }else{
        Serial.println("Disconnected");
      }
    }else{
      digitalWrite(outputPIN[incomingByte-1],out);// NOk and COMk (Dis)connected
      Serial.print("Relay  ");
      Serial.print(incomingByte);
      if(out){
        Serial.println(" NO and COM Disconnected");
      }else{
        Serial.println(" NO and COM Connected");
      }
    }
    delay(1000); // wait 1000 milliseconds (1 second)
    }
  }
  
}

void calibration() {
  digitalWrite(outputPIN2,!calib);// Relay module 2 (Dis)connected
  for(byte i = 0; i < 16; i++){
          digitalWrite(outputPIN[i],!calib);// NOi and COMi (Dis)connected
        }
      Serial.print("Calibration mode");
}

void test() {
  for (byte i = 0; i < 16; i++) {

      Serial.print("Testing relay  ");
      Serial.println(i+1);
      
    digitalWrite(outputPIN[i], HIGH);
    delay(500);
    digitalWrite(outputPIN[i], LOW);
    delay(500);
    digitalWrite(outputPIN[i], HIGH);
    delay(500);
    digitalWrite(outputPIN[i], LOW);
    delay(500);
  }

  Serial.println("Testing module 2");
      
    digitalWrite(outputPIN2, HIGH);
    delay(500);
    digitalWrite(outputPIN2, LOW);
    delay(500);
    digitalWrite(outputPIN2, HIGH);
    delay(500);
    digitalWrite(outputPIN2, LOW);
    delay(500);
  
    for (byte i = 0; i < 16; i++) {
    digitalWrite(outputPIN[i], HIGH);
  }

  digitalWrite(outputPIN2, HIGH);
  
}
