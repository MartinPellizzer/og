uint32_t timer = 0;

void setup() {
  Serial.begin(9600);
    digitalWrite(2, HIGH);
  pinMode(2, OUTPUT);
}

void loop() {
  if (millis() - timer > 300000) {
    timer = millis();
    digitalWrite(2, !digitalRead(2));
    Serial.println("okl");
  }
}
