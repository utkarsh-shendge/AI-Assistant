import speech_recognition as sr
import pyttsx3
import time
import pickle
import datetime
import webbrowser
import os
import pywhatkit
import re
import time
import pyautogui
import pygetwindow as gw
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import requests

ESP_IP = "10.106.31.163"   # <-- replace with your IP

def control_device(device, state):
    try:
        requests.get(f"http://{ESP_IP}/{device}/{state}")
    except:
        print("ESP not reachable")


cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nova-assistant-57be1-default-rtdb.firebaseio.com'
})

def log_to_firebase(command, intent, confidence):
    try:
        ref = db.reference("logs")

        data = {
            "command": command,
            "intent": intent,
            "confidence": float(confidence),
            "timestamp": datetime.now().isoformat()
        }

        ref.push(data)

    except Exception as e:
        print("Firebase logging error:", e)

def get_logs_from_firebase():
    try:
        ref = db.reference("logs")
        data = ref.get()
        return data
    except Exception as e:
        print("Error fetching logs:", e)
        return None

def analyze_usage(logs):
    if not logs:
        return "No data available"

    intent_count = {}

    for key in logs:
        intent = logs[key].get("intent")

        if intent in intent_count:
            intent_count[intent] += 1
        else:
            intent_count[intent] = 1

    # Find most used intent
    most_used = max(intent_count, key=intent_count.get)
    count = intent_count[most_used]

    return most_used, count

def format_intent(intent):
    return intent.replace("_", " ").lower()

def speak_summary():
    logs = get_logs_from_firebase()

    result = analyze_usage(logs)

    if result == "No data available":
        speak("No usage data found")
        return

    intent, count = result

    readable = format_intent(intent)

    speak(f"Your most used command is {readable}, used {count} times")

def send_whatsapp_desktop(contact_name, message):

    # Open WhatsApp Desktop
    os.system("start whatsapp:")
    time.sleep(7)

    # Bring WhatsApp window to front
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        windows[0].activate()
        time.sleep(2)

    # Open search (Ctrl + F)
    pyautogui.hotkey("ctrl", "f")
    time.sleep(2)

    # Type contact name
    pyautogui.write(contact_name)
    time.sleep(2)

    pyautogui.press("enter")
    time.sleep(2)

    # Type message
    pyautogui.write(message)
    time.sleep(2)

    pyautogui.press("enter")

    print("Message sent successfully")
    print(gw.getAllTitles())

# ---------- TTS ----------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.2)

def play_song_spotify_app(query):
    try:
        speak(f"Playing {query} on Spotify")

        # Open Spotify
        os.system("start spotify")
        time.sleep(5)

        # Bring Spotify to front
        windows = gw.getWindowsWithTitle("Spotify")
        if windows:
            windows[0].activate()
            time.sleep(3)

        # Open search
        pyautogui.hotkey("ctrl", "l")
        time.sleep(5)

        # Type song name
        pyautogui.write(query)
        time.sleep(5)

        # Press Enter twice (search + play)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.press("enter")

    except Exception as e:
        print("Spotify error:", e)

# ---------- Load ML Model ----------
model = pickle.load(open("model/intent_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

def predict_intent_with_confidence(text):
    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]
    max_prob = max(probs)
    intent = model.classes_[probs.argmax()]
    return intent, max_prob
# ---------- Speech Recognition ----------
r = sr.Recognizer()

speak("Smart assistant with machine learning started")

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source)

        text = r.recognize_google(audio).lower()
        print("User said:", text)

        WAKE_WORD = "nova"

        if WAKE_WORD not in text:
            print("Wake word not detected. Ignoring...")
            continue

        text = text.replace(WAKE_WORD, "").strip()

        text = text.lower()

        # 🔥 PRIORITY KEYWORD MATCHING (FIX YOUR BUG)

        if "fan" in text:
            if "on" in text:
                speak("Turning on fan")
                control_device("fan", "on")
                continue

            elif "chalu" in text:
                speak("Turning on fan")
                control_device("fan", "on")
                continue

            elif "off" in text:
                speak("Turning off fan")
                control_device("fan", "off")
                continue

            elif "band" in text:
                speak("Turning off fan")
                control_device("fan", "off")
                continue

        if "play" in text or "song" in text or "music" in text:

            query = text.replace("play", "").replace("song", "").replace("music", "").strip()

            if not query:
                speak("Which song should I play?")
                
                try:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        audio = r.listen(source)

                    query = r.recognize_google(audio)
                except:
                    speak("I could not understand")
                    continue

            play_song_spotify_app(query)
            continue

        elif "light" in text:
            if "on" in text:
                speak("Turning on light")
                control_device("light", "on")
                continue

            elif "chalu" in text:
                speak("Turning on light")
                control_device("light", "on")
                continue

            elif "off" in text:
                speak("Turning off light")
                control_device("light", "off")
                continue

            elif "band" in text:
                speak("Turning off light")
                control_device("light", "off")
                continue

        # ----------- Predict Intent + Confidence (fallback) -----------
        intent, confidence = predict_intent_with_confidence(text)
        log_to_firebase(text, intent, confidence)

        print(f"Predicted intent: {intent}")
        print(f"Confidence: {confidence:.2f}")



        CONFIDENCE_THRESHOLD = 0.10  # 10% minimum confidence

        if confidence < CONFIDENCE_THRESHOLD:
            speak("I am not confident about that command. Please repeat.")
            continue

        # ----------- ACTIONS -----------
        if intent == "OPEN_YOUTUBE":
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif intent == "OPEN_WORD":
            speak("Opening Microsoft Word")
            os.system("start winword")

        elif intent == "SHOW_SUMMARY":
            speak_summary()


        elif intent == "SEARCH_YOUTUBE":

            # Try extracting query from same sentence
            if "youtube" in text:
                query = text.replace("youtube", "").replace("search", "").replace("play", "").strip()
            else:
                query = ""

            # If query not found → ask user
            if not query:
                speak("What should I search on YouTube?")
                
                try:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        audio = r.listen(source, timeout=5, phrase_time_limit=10)

                    query = r.recognize_google(audio)
                    print("YouTube query:", query)

                except:
                    speak("I could not understand")
                    continue

            speak(f"Searching YouTube for {query}")

            import urllib.parse
            encoded_query = urllib.parse.quote(query)

            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(url)

        elif intent == "SEARCH_GOOGLE":

            speak("What should I search?")

            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)

                query = r.recognize_google(audio)
                print("Search query:", query)

            except:
                speak("I could not understand the search query")
                continue

            speak(f"Searching for {query}")

            import urllib.parse
            encoded_query = urllib.parse.quote(query)

            url = f"https://www.google.com/search?q={encoded_query}"
            webbrowser.open(url)
        
        elif intent == "OPEN_SPOTIFY":
            speak("Opening Spotify")
            os.system("start spotify")

        elif intent == "SEND_WHATSAPP":

            words = text.split()

            if "to" in words:
                name = words[words.index("to") + 1].capitalize()
            else:
                speak("Please say the contact name")
                continue

            speak(f"What message should I send to {name}?")

            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)

                message = r.recognize_google(audio)

            except:
                speak("I could not understand the message")
                continue

            speak("Sending your message")

            send_whatsapp_desktop(name, message)

        elif intent == "OPEN_GOOGLE":
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif intent == "GET_TIME":
            now = datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif intent == "LIGHT_ON":
            speak("Turning on the light")

        elif intent == "LIGHT_OFF":
            speak("Turning off the light")

        elif intent == "OPEN_WHATSAPP":
            speak("Opening WhatsApp")
            # Fallback to WhatsApp Web
            os.system("start whatsapp:")

        elif intent == "EXIT":
            speak("Goodbye")
            break

        else:
            speak("I did not understand the command")

    except sr.UnknownValueError:
        speak("Please repeat")
    except sr.RequestError:
        speak("Network error")