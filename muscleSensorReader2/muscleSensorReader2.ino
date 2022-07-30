void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float currTime = millis();
  Serial.println(analogRead(1));
  while(millis() - currTime < 1) {}
}
