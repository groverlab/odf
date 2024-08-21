void setup() {
  analogReadResolution(14);
  Serial.begin(115200);
}

void loop() {
  Serial.println(analogRead(A1));
}
