import speech_recognition as sr
import webbrowser
import pyttsx3
import pywhatkit
import wikipedia
import musicLibrary  

from gtts import gTTS
import pygame
import os
import time 


recognizer = sr.Recognizer()
engine = pyttsx3.init()


pygame.mixer.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def searchGoogle(query):
    results = pywhatkit.search(query)
    if results:
        speak(f"I found the following on Google: {results}")
    else:
        searchWikipedia(query)


def searchYoutube(query):
    speak("This is what I found for your search!")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    time.sleep(5)  
    speak("Done playing top results.")

def playYoutube():
    speak("Please say the name of the song you want to play.")
    with sr.Microphone() as source:
        print("Listening for song name...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        song_name = recognizer.recognize_google(audio)
        print(f"Heard song name: {song_name}")
        if song_name.lower() in musicLibrary.music:
            link = musicLibrary.music[song_name.lower()]
            print(f"Found song in library: {song_name} - {link}")
            webbrowser.open(link)
            speak(f"Playing {song_name}")
        else:
            speak(f"Searching YouTube for {song_name}")
            searchYoutube(song_name)
    except sr.UnknownValueError:
        print("Could not understand the song name")
        speak("Sorry, I didn't catch that. Please repeat.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, there was a problem with the recognition service.")

def searchWikipedia(query):
    speak("Searching from Wikipedia....")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia..")
        print(results)
        speak(results)
    except:
        speak("No speakable output available")

def processCommand(command):
    command = command.lower()
    
    if "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook...")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")
    elif "open chat gpt" in command:
        speak("Opening ChatGPT...")
        webbrowser.open("https://chat.openai.com/")
    elif "play" in command:
        playYoutube()
    elif "wikipedia" in command:
        searchWikipedia(command.replace("wikipedia", "").strip())
    elif "youtube" in command:
        searchYoutube(command.replace("youtube", "").strip())
    else:
        speak("Searching Google...")
        searchGoogle(command)

if __name__ == "__main__":
    speak("Initializing Pluto....")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for activation word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            try:
                word = recognizer.recognize_google(audio)
                print(f"Heard activation word: {word}")
            except sr.UnknownValueError:
                print("Could not understand the activation word")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue
            
            if word.lower() == "pluto":
                speak("Yes?")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    
                    try:
                        command = recognizer.recognize_google(audio)
                        print(f"Heard command: {command}")
                        processCommand(command)
                    except sr.UnknownValueError:
                        print("Could not understand the command")
                        speak("Sorry, I didn't catch that. Please repeat.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                        speak("Sorry, there was a problem with the recognition service.")
                    
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except Exception as e:
            print(f"Error: {e}")


