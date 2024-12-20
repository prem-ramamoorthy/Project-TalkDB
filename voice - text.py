import speech_recognition as sr

def interactive_voice_to_text():
    r = sr.Recognizer()
    print("Press Ctrl+C to stop the program.")
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio. Please try again."
            
        except sr.RequestError:
            return "Sorry, the service is down. Please check your internet connection."

print(interactive_voice_to_text())
