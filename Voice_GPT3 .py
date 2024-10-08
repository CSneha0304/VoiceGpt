import openai
import pyttsx3
import speech_recognition as sr
import pyaudio

#Set your OpenAI API key
openai.api_key = "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"

#Initialize the text_to_speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer() 
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print("Say anything : ")
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"] 

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #wait for user to say "hello"
        print("Say 'Hello' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    #Record Audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause.threshold = 1   
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    #Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print("You said : {text}")

                        #Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        #Read response using text-to-speech
                        speak_text(response)
            except Exception as e :
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()


    
