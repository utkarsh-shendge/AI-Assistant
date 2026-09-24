# NOVA – Smart Voice Assistant with IoT, Machine Learning & Cloud Integration

NOVA is an intelligent voice-controlled personal assistant that combines **Speech Recognition, Machine Learning, IoT, Cloud Computing, and Desktop Automation** into a single system.

The assistant understands natural voice commands, identifies the user's intent using a machine learning model, performs computer-based tasks, controls IoT devices through an ESP8266, and stores activity logs in Firebase for usage analysis.

---

## 🚀 Features

### 🎙️ Voice Assistant
- Voice-based interaction using a microphone
- Speech-to-text conversion using Google Speech Recognition
- Text-to-speech responses using `pyttsx3`
- Wake-word based activation using **"Nova"**

### 🤖 Machine Learning
- Intent classification using a trained ML model
- Confidence-based intent prediction
- Supports multiple user commands
- Hybrid approach using keyword-based rules for critical IoT commands

### 💡 IoT Home Automation
- ESP8266-based device control
- Voice-controlled LED
- Voice-controlled fan
- HTTP-based communication between Python and ESP8266

### 👁️ Automatic Motion-Based Lighting
- HC-SR501 PIR motion sensor
- Separate LED for automatic motion-based lighting
- Detects human motion and automatically turns the LED ON/OFF

### ☁️ Firebase Cloud Logging
- Stores assistant activity in Firebase Realtime Database
- Records:
  - User command
  - Detected intent
  - Confidence score
  - Timestamp
- Provides usage analysis to identify frequently used commands

### 🌐 Desktop Automation
- Open Google
- Search Google
- Open YouTube
- Search YouTube
- Open Microsoft Word
- Open WhatsApp
- Send WhatsApp messages through desktop automation
- Open and interact with Spotify

---

# 🏗️ System Architecture

```text
                  ┌───────────────────┐
                  │       User        │
                  │   Voice Command   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Speech Recognition│
                  │  Google Speech API│
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   NOVA Assistant  │
                  │   Python Program  │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Intent Prediction │
                  │   ML Classifier   │
                  └─────────┬─────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       Desktop Tasks    IoT Control    Cloud Logging
             │              │              │
             ▼              ▼              ▼
      Google/YouTube    ESP8266       Firebase
      Word/WhatsApp       │
      Spotify             │
                          ▼
                 ┌─────────────────┐
                 │   IoT Devices   │
                 ├─────────────────┤
                 │ Voice LED       │
                 │ PIR LED         │
                 │ DC Fan Motor    │
                 └─────────────────┘

🔧 Hardware Components
Component	Quantity	Purpose
NodeMCU ESP8266	1	Main IoT controller
HC-SR501 PIR Sensor	1	Human motion detection
LED	2	Voice-controlled and PIR-controlled lighting
220Ω/330Ω Resistor	2	LED current limiting
L298N Motor Driver	1	DC motor control
Small DC Motor	1	Fan
Fan Blade	1	Fan assembly
Breadboard	1	Circuit prototyping
Jumper Wires	Set	Circuit connections
USB Cable	1	NodeMCU programming/power
🔌 Hardware Connections
Voice-Controlled LED
NodeMCU D2
    │
    ▼
Resistor
    │
    ▼
LED 1
    │
    ▼
GND
PIR-Controlled LED
NodeMCU D6
    │
    ▼
Resistor
    │
    ▼
LED 2
    │
    ▼
GND
PIR Sensor
HC-SR501        NodeMCU
-----------------------
VCC      --->   3V3
GND      --->   GND
OUT      --->   D5
L298N + DC Motor
NodeMCU D1  ---> L298N IN1
NodeMCU D3  ---> L298N IN2
NodeMCU GND ---> L298N GND

L298N OUT1  ---> Motor
L298N OUT2  ---> Motor

The motor is powered through the motor driver rather than directly from an ESP8266 GPIO pin.

💻 Software Technologies
Python
Arduino IDE
C/C++ for ESP8266
Machine Learning
Speech Recognition
Text-to-Speech
HTTP
Firebase Realtime Database
Selenium / PyAutoGUI-based automation
Google Speech Recognition
📦 Python Libraries

Install the required Python packages:

pip install SpeechRecognition
pip install pyttsx3
pip install PyAudio
pip install requests
pip install pywhatkit
pip install pyautogui
pip install pygetwindow
pip install firebase-admin

Depending on your implementation, additional packages may be required for your trained ML model.

📁 Project Structure
smart_assistant/
│
├── assistant_ml.py
│
├── train_model.py
│
├── model/
│   ├── intent_model.pkl
│   └── vectorizer.pkl
│
├── firebase_key.json
│
├── dataset/
│   └── intents.csv
│
├── hardware/
│   └── esp8266_code.ino
│
├── venv/
│
└── README.md

Important: Do NOT upload firebase_key.json to GitHub. It contains private Firebase credentials.

⚙️ Setup
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

Move into the project:

cd smart_assistant
2. Create a Virtual Environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Firebase

Create a Firebase project and enable Firebase Realtime Database.

Download your Firebase service-account credentials and place them locally as:

firebase_key.json

Do not commit this file to GitHub.

5. Configure ESP8266

Open the ESP8266 Arduino code and enter your Wi-Fi credentials:

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

Upload the code using Arduino IDE.

Open Serial Monitor and note the ESP8266 IP address:

WiFi Connected
ESP8266 IP Address: 192.168.X.X
6. Configure Python Assistant

Update the ESP8266 IP in assistant_ml.py:

ESP_IP = "192.168.X.X"

The laptop and ESP8266 must be connected to the same local network.

▶️ Running the Assistant

Activate the virtual environment:

venv\Scripts\activate

Run:

python assistant_ml.py

NOVA will start and respond to the wake word:

Nova
🗣️ Example Commands
Computer Automation
Nova open YouTube
Nova open Google
Nova search Google
Nova search YouTube
Nova open Word
IoT Control
Nova turn on light
Nova turn off light
Nova turn on fan
Nova turn off fan
WhatsApp
Nova send WhatsApp message to Papa

NOVA then asks for the message.

Music
Nova play a song
Nova play [song name]
Nova open Spotify
💡 Smart Lighting

The project uses two independent LEDs.

LED 1 – Voice Controlled

Controlled through:

Voice Command
      ↓
Python Assistant
      ↓
HTTP Request
      ↓
ESP8266
      ↓
LED 1
LED 2 – PIR Controlled
Human Motion
      ↓
HC-SR501 PIR
      ↓
ESP8266
      ↓
LED 2

This allows the project to demonstrate both manual voice-based control and automatic sensor-based control.

☁️ Firebase Activity Logging

NOVA stores command activity in Firebase.

Example record:

{
  "command": "turn on fan",
  "intent": "FAN_ON",
  "confidence": 0.97,
  "timestamp": "2026-09-24T09:30:00"
}

The stored information can be used to analyze:

Frequently used commands
Intent frequency
User interaction patterns
Assistant usage
🧠 Machine Learning Workflow
Voice Command
      ↓
Speech-to-Text
      ↓
Text Preprocessing
      ↓
TF-IDF / Vectorization
      ↓
ML Intent Classifier
      ↓
Intent + Confidence
      ↓
Action

For important device commands, the project can also use keyword-based validation before ML classification to reduce incorrect device selection.
