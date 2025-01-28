/*
TX (from RS485 module) → RX (GPIO 17) on the ESP32.
RX (from RS485 module) → TX (GPIO 16) on the ESP32.
VCC (from RS485 module) → 5V or 3.3V (depending on the module) on the ESP32.
GND (from RS485 module) → GND on the ESP32.

LOOP A(NO) - p4
LOOP A(COM)       - gnd ()
LOOP B(NO) - p5
LOOP B(COM)       - gnd ()


*/


#define LOOP_A_PIN 4
#define LOOP_B_PIN 5

unsigned long detectionTimestamp = 0;
unsigned long timeout = 180000;

bool loopADetected = false;
bool loopBDetected = false;
bool sequenceComplete = false;

HardwareSerial mySerial(1);

void setup() {
  pinMode(LOOP_A_PIN, INPUT_PULLUP);
  pinMode(LOOP_B_PIN, INPUT_PULLUP);
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
}

void loop() {
  if (sequenceComplete) {
    delay(1000);
    resetSequence();
    sequenceComplete = false;
    return;
  }

  if (digitalRead(LOOP_A_PIN) == LOW && !loopADetected && !loopBDetected) {
    loopADetected = true;
    detectionTimestamp = millis();
    Serial.println("Loop A detected, waiting for Loop B...");
  }

  if (digitalRead(LOOP_B_PIN) == LOW && !loopBDetected && !loopADetected) {
    loopBDetected = true;
    detectionTimestamp = millis();
    Serial.println("Loop B detected, waiting for Loop A...");
  }

  if (loopADetected && !loopBDetected) {
    if (digitalRead(LOOP_B_PIN) == LOW) {
      Serial.println("Sequence: Loop A -> Loop B (Car Entry)");
      sendProtocol(true);
      resetSequence();
      sequenceComplete = true;
    } 
    else if (millis() - detectionTimestamp > timeout) {
      Serial.println("Timeout: Restarting sequence...");
      resetSequence();
      sequenceComplete = true;
    }
  }

  // If Loop B -> Loop A detected (Car Exit)
  if (loopBDetected && !loopADetected) {
    if (digitalRead(LOOP_A_PIN) == LOW) {
      Serial.println("Sequence: Loop B -> Loop A (Car Exit)");
      sendProtocol(false);
      resetSequence();
      sequenceComplete = true;
    } else if (millis() - detectionTimestamp > timeout) {
      Serial.println("Timeout: Restarting sequence...");
      resetSequence();
      sequenceComplete = true;
    }
  }
}

void sendProtocol(bool isEntry) {
  byte entryMessage[] = {0xAA, 0x01, 0x00, 0x55};
  byte exitMessage[] = {0xAA, 0x00, 0x01, 0x55};

  byte* messageToSend;
  
  // Determine which message to send based on the isEntry flag
  if (isEntry) {
    messageToSend = entryMessage;
  } else {
    messageToSend = exitMessage;
  }

  // Print the data to Serial Monitor for debugging
  Serial.print("Sending data: ");
  for (int i = 0; i < 4; i++) {
    Serial.print("0x");
    if (messageToSend[i] < 0x10) {
      Serial.print("0");
    }
    Serial.print(messageToSend[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  // Send the selected message over RS485
  mySerial.write(messageToSend, sizeof(entryMessage));
}

// Function to reset the sequence variables
void resetSequence() {
  loopADetected = false;
  loopBDetected = false;
  detectionTimestamp = 0;
}

