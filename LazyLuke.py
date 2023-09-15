import speech_recognition as sr
import threading
import subprocess
import time
import os
import pygame.mixer
import webbrowser
import pyautogui
import ctypes
import pyttsx3


# Initialize the recognizer
recognizer = sr.Recognizer()
pygame.mixer.init()
engine = pyttsx3.init()
engine.setProperty("rate", 160)

# Hide the console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

sound = pygame.mixer.Sound('sound.wav')

# Flag to track if the computer is currently sleeping
is_sleeping = False

listening_thread_active = True


def perform_action(command):
    global is_sleeping
    if command == "sleep" and not is_sleeping:
        print("Putting PC to sleep...")
        sound.play()
        subprocess.run(["nircmd.exe", "standby"])
        is_sleeping = True
        # Wait for a moment before re-enabling listening
        time.sleep(3)
    elif command == "shutdown":
        sound.play()
        time.sleep(3)
        os.system("shutdown /s /t 1")
    elif command == "restart":
        sound.play()
        time.sleep(3)
        os.system("shutdown /r /t 1")

    elif command == "increase volume":
        print("Increasing volume...")
        sound.play()
        subprocess.run(["nircmd.exe", "changesysvolume", "5000"])  # Increase volume by 2000 units
    elif command == "decrease volume":
        print("Decreasing volume...")
        sound.play()
        subprocess.run(["nircmd.exe", "changesysvolume", "-5000"])  # Decrease volume by 2000 units

    elif command == "increase brightness":
        print("Increasing brightness...")
        sound.play()
        subprocess.run(["nircmd.exe", "changebrightness", "10"])  # Increase brightness by 10%
    elif command == "decrease brightness":
        print("Decreasing brightness...")
        sound.play()
        subprocess.run(["nircmd.exe", "changebrightness", "-10"])  # Decrease brightness by 10%
    elif command == "scroll up":
        print("Scrolling up...")
        sound.play()
        pyautogui.scroll(250)  # Simulate scrolling up
    elif command == "scroll down":
        print("Scrolling down...")
        sound.play()
        pyautogui.scroll(-250)  # Simulate scrolling down
    elif command == "open youtube":
        print("Opening YouTube...")
        sound.play()
        webbrowser.open("https://www.youtube.com")
    elif command == "open whatsapp":
        print("Opening WhatsApp...")
        sound.play()
        webbrowser.open("https://web.whatsapp.com")
    elif command == "open wikipedia":
        print("Opening Wikipedia...")
        sound.play()
        webbrowser.open("https://en.wikipedia.org")
    elif command == "open gmail":
        print("Opening Gmail...")
        sound.play()
        webbrowser.open("https://mail.google.com")
    elif command == "open google":
        print("Opening Google...")
        sound.play()
        webbrowser.open("https://www.google.com")
    elif command == "exit" or command == "close":
        engine.say("Goodbye !")
        engine.runAndWait()
        print("Exiting the script...")
        listening_thread_active = False
        os._exit(0)  # Terminate the script

def ask_for_name():
    global engine
    engine.say("Hello! I'm Lazyluke. What's your name?")
    engine.runAndWait()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            name = recognizer.recognize_google(audio).capitalize()
            engine.say(f"Nice to meet you, {name}!")
            engine.runAndWait()
        except sr.UnknownValueError:
            engine.say("I couldn't hear your name clearly. Let's try again next time.")
            engine.runAndWait()

# Define a function to listen for voice commands
def listen_for_commands():
    global is_sleeping
    with sr.Microphone() as source:
        print("Listening for commands...")
        sound.play()

        try:
            while True:
                if not is_sleeping:
                    audio = recognizer.listen(source,phrase_time_limit = 5)
                    try:
                        text = recognizer.recognize_google(audio).lower()
                        print(text)
                        if "sleep" in text:
                            perform_action("sleep")
                        elif "shutdown" in text:
                            perform_action("shutdown")
                        elif "restart" in text:
                            perform_action("restart")
                        elif "increase volume" in text:
                            perform_action("increase volume")
                        elif "decrease volume" in text:
                            perform_action("decrease volume")

                        elif "increase brightness" in text:
                            perform_action("increase brightness")
                        elif "decrease brightness" in text:
                            perform_action("decrease brightness")
                        elif "scroll up" in text:
                            perform_action("scroll up")
                        elif "scroll down" in text:
                            perform_action("scroll down")
                        elif "open youtube" in text:
                            perform_action("open youtube")
                        elif "open whatsapp" in text:
                            perform_action("open whatsapp")
                        elif "open wikipedia" in text:
                            perform_action("open wikipedia")
                        elif "open gmail" in text:
                            perform_action("open gmail")
                        elif "open google" in text:
                            perform_action("open google")
                        elif "exit" in text:
                            perform_action(("exit"))
                    except sr.UnknownValueError:
                        pass
                else:
                    # Sleep for a moment to reduce CPU usage during sleep
                    time.sleep(1)
        except KeyboardInterrupt:
            pass

# Define a function to check if the computer woke up from sleep and restart listening
def check_wakeup():
    global is_sleeping
    while True:
        if is_sleeping:
            is_sleeping = False
            print("PC woke up. Listening for commands...")
            # Restart the listening thread
            listening_thread_active = False
            time.sleep(2)  # Wait for 2 seconds to allow the old thread to terminate
            listening_thread_active = True
            new_listening_thread = threading.Thread(target=listen_for_commands)
            new_listening_thread.daemon = True
            new_listening_thread.start()
        time.sleep(1)

if __name__ == "__main__":

    first_run = not os.path.exists("user_name.txt")

    if first_run:
        # Ask for the user's name on the first run and save it to a file
        ask_for_name()
        with open("user_name.txt", "w") as name_file:
            name_file.write("1")  # Create a flag file

    # Greet the user
    with open("user_name.txt", "r") as name_file:
        user_name = name_file.read()
        engine.say(f"Hi, {user_name}!")
        engine.runAndWait()

    # Create a thread for listening to voice commands
    listening_thread = threading.Thread(target=listen_for_commands)
    listening_thread.daemon = True
    listening_thread.start()

    # Create a thread to check if the computer wakes up
    wakeup_thread = threading.Thread(target=check_wakeup)
    wakeup_thread.daemon = True
    wakeup_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
