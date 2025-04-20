int enA = 9, in1 = 7, in2 = 6;
int enB = 10, in3 = 12, in4 = 11;

void setup() {
  Serial.begin(9600);
  pinMode(in1, OUTPUT); pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT); pinMode(in4, OUTPUT);
  pinMode(enA, OUTPUT); pinMode(enB, OUTPUT);
  stopMotors();
}

void moveForward() {
  digitalWrite(in1, HIGH); digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH); digitalWrite(in4, LOW);
  analogWrite(enA, 40); analogWrite(enB, 40);
}

void moveForwardSlow() {
  digitalWrite(in1, HIGH); digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH); digitalWrite(in4, LOW);
  analogWrite(enA, 25); analogWrite(enB, 25);  // Slow speed
}

void turnLeft() {
  digitalWrite(in1, LOW); digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH); digitalWrite(in4, LOW);
  analogWrite(enA, 40); analogWrite(enB, 40);
}

void turnRight() {
  digitalWrite(in1, HIGH); digitalWrite(in2, LOW);
  digitalWrite(in3, LOW); digitalWrite(in4, HIGH);
  analogWrite(enA, 40); analogWrite(enB, 40);
}

void stopMotors() {
  digitalWrite(in1, LOW); digitalWrite(in2, LOW);
  digitalWrite(in3, LOW); digitalWrite(in4, LOW);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'F') moveForward();
    else if (cmd == 'f') moveForwardSlow();
    else if (cmd == 'L') turnLeft();
    else if (cmd == 'R') turnRight();
    else if (cmd == 'S') stopMotors();
  }
}