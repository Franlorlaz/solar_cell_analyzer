// the number of the LED pin
const int ledRpin = 32;
const int ledGpin = 33;
const int ledBpin = 25; 
const int inputPIN = 35;
const int outputPIN[] = {23,22,21,19,18,5,17,16,4,0,2,26,27,14,12,13}; //Pins for esp32

// setting PWM properties
int freq = 5000;
int Channel[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
int resolution = 8;
int currentChannel = 0;

boolean working=true;
boolean power;
int val[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

int V[] = {0,0,0,0,0,0,0,0,0,0};
byte count=0;

String sdata="";  // Initialised to nothing.
 
void setup(){
  Serial.begin(9600);
  
  Serial.println("Starting comunication");
  
  Serial.println("Ready to work!");

  pinMode(inputPIN, INPUT);
  pinMode(ledRpin, OUTPUT);
  pinMode(ledGpin, OUTPUT);
  pinMode(ledBpin, OUTPUT);  

  for (byte i = 0; i < 16; i++) {
  // configure LED PWM functionalitites
  ledcSetup(Channel[i], freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(outputPIN[i], Channel[i]);
  }

}
 
void loop(){
  byte ch;
  String valStr;
  int Val;
  Val = analogRead(inputPIN);
  V[count%10]=Val;
  count++;
  Val = (V[0]+V[1]+V[2]+V[3]+V[4]+V[5]+V[6]+V[7]+V[8]+V[9])/10;
  //Serial.println(float(Val)*18/4095);
  if (Val<500){
    power=LOW;
  }else{
    power=HIGH;
  }

  if (working!=power){
    if (power){
      for (byte i = 0; i < 16; i++) {
        ledcWrite(Channel[i], val[i]);
        delay(15);
      }
      Serial.println("Warning: power source restored");
    } else {
      for (byte i = 0; i < 16; i++) {
        ledcWrite(Channel[i], 0);
        delay(15);
      }
      Serial.println("Warning: power source is off");
    }
    working = power;
  }

  if (Val<3000){
    digitalWrite(ledRpin, HIGH); //led rojo encendido
    //Serial.println("led rojo encendido");
    //delay(500);
  }else{
    digitalWrite(ledRpin, LOW);//led rojo apagado
    //delay(500);
  }
  if (working){
    boolean aux = false;
    for (byte i = 0; i < 16; i++) {
      if (val[i]>0){
        aux = true;
        break;
      }
    }
    if (aux){
      digitalWrite(ledGpin, HIGH);//led verde encendido
      //Serial.println("led verde encendido");
      digitalWrite(ledBpin, LOW);//led azul apagado
      //delay(500);
    }else{
      digitalWrite(ledGpin, LOW);//led verde apagado
      digitalWrite(ledBpin, HIGH);//led azul encendido
      //Serial.println("led azul encendido");
      //delay(500);
    }
  }else{
      digitalWrite(ledGpin, LOW);//led verde apagado
      digitalWrite(ledBpin, LOW);//led azul apagado
      //delay(500);
  }

   if (Serial.available()) {
      ch = Serial.read();

      sdata += (char)ch;

      if (ch==10) {  // Command received and ready.
        
         sdata.trim();

         // Process command in sdata.
         switch( sdata.charAt(0) ) {
         case 'd':
            if (sdata.length()>1){
               valStr = sdata.substring(1);
               val[currentChannel] = valStr.toInt();
               if (power){
                  ledcWrite(currentChannel, val[currentChannel]);   
                  delay(15);
               } else {
                  Serial.println("Warning: power source is off");
               }
            }
            Serial.print("DutyCycle ");
            Serial.print(val[currentChannel]);
            Serial.print(" at channel  ");
            Serial.println(currentChannel);
            break;
         case 'c':
            if (sdata.length()>1){
               valStr = sdata.substring(1);
               currentChannel = valStr.toInt();
            }
            Serial.print("Channel  ");
            Serial.println(currentChannel);
            Serial.print(" GPIO  ");
            Serial.println(outputPIN[currentChannel]);
            break;
         case 'f':
            Serial.print("Frequency: ");
            Serial.print(freq);
            Serial.println(" Hz");
            break;
         case 'p':
            Serial.print("Power: ");
            //Serial.print(3.3*Val/4095); // voltage
            Serial.print(float(Val)*18/4095);
            Serial.println(" V");
            break;
         case 'v':
            if (sdata.length()>1){
               valStr = sdata.substring(1);
               Val = valStr.toInt();
            }
            Serial.print("Val ");
            Serial.println(Val);
            break;
         default: Serial.println(sdata);
         } // switch

         sdata = ""; // Clear the string ready for the next command.
      } // if \r
   }  // available
}
