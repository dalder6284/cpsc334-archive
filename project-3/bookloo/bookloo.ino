// Basic demo for accelerometer readings from Adafruit MPU6050

// ESP32 Guide: https://RandomNerdTutorials.com/esp32-mpu-6050-accelerometer-gyroscope-arduino/
// ESP8266 Guide: https://RandomNerdTutorials.com/esp8266-nodemcu-mpu-6050-accelerometer-gyroscope-arduino/
// Arduino Guide: https://RandomNerdTutorials.com/arduino-mpu-6050-accelerometer-gyroscope/

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>

#define SPONGE 34
#define LED 17

// MPU-6050
Adafruit_MPU6050 mpu;

struct __attribute__((packed)) DataPacket {
  float ax;
  float ay;
  float az;

  float gx;
  float gy;
  float gz;

  uint16_t sponge;
};

DataPacket packet;

// WiFI
WiFiClient client;

const char* ssid = "yale wireless";
const uint16_t port = 8090;
const char* host = "10.74.138.181";

void blinkLed(int times) {

  int tdelay = int(1000 / times);

  for (int i = 0; i < times; i++) { 
    digitalWrite(LED, HIGH);
    delay(tdelay);
    digitalWrite(LED, LOW);
    delay(tdelay);
  }
}

void setup(void) {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  // SERIAL
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  // MPU 6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  Serial.println("");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  // WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, "");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("...");
    blinkLed(3);
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("");

  while (1) {
    if (client.connect(host, port)) {
      Serial.println("Connected to server!");
      break;
    }

    Serial.println("Connection to host failed.");
    blinkLed(3);
  }

  Serial.println("");
}

void loop() {
  uint16_t x = analogRead(SPONGE);
  Serial.println(x);
  if (client.connected()) {
    digitalWrite(LED, HIGH);
    packet.sponge = x;

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    packet.ax = a.acceleration.x;
    packet.ay = a.acceleration.y;
    packet.az = a.acceleration.z;
    
    packet.gx = g.gyro.x;
    packet.gy = g.gyro.y;
    packet.gz = g.gyro.z;
    

    client.write((uint8_t*)&packet, sizeof(packet));
    // Serial.println("Packet sent.");
    delay(200);
    return;
  }

  Serial.println("Client not connected. Attempting to reconnect.");
  while (1) {
    if (client.connect(host, port)) {
      Serial.println("Connected to server!");
      break;
    }

    Serial.println("Connection to host failed. Retrying.");
    blinkLed(3);
  }

}