#define RE_DE_PIN 16

HardwareSerial Sender(1);
uint8_t buff[9] = {0};
uint8_t i = 0;
uint8_t new_data = 0;
uint32_t timer = 0;

void setup()
{
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 27, 14);
  Sender.begin(9600, SERIAL_8N1, 17, 4);
  pinMode(RE_DE_PIN, OUTPUT);
}

void loop()
{
  if (new_data)
  {
    if (millis() - timer > 40)
    {
      i = 0;
      new_data = 0;

      digitalWrite(RE_DE_PIN, HIGH);
      for(int k = 0; k < 9; k++)
      {
        Sender.write(buff[k]);
      }
      delay(10);
      digitalWrite(RE_DE_PIN, LOW);
    }
  }  
  
  if (Serial2.available() > 0)  
  {
    uint8_t c = Serial2.read();
    buff[i] = c;
    i++;
    new_data = 1;
    timer = millis();
  }
}
