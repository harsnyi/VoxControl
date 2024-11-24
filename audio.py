import sounddevice as sd
import numpy as np
import wave
import speech_recognition as sr
import os

class Audio:
    def __init__(self, uuid):
        self.uuid = uuid
        self.recognizer = sr.Recognizer()
        self.SAMPLE_RATE = 44100
        self.DURATION = 5
        self.CHANNELS = 1
        self.OUTPUT_DIR = os.path.join("/Users/harsnyi/Documents/VoxControl/recordings", self.uuid)
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        self.OUTPUT_FILENAME = os.path.join(self.OUTPUT_DIR, "output.wav")

    def record(self):
        print("Recording...")

        # Record audio
        recording = sd.rec(int(self.SAMPLE_RATE * self.DURATION),
                            samplerate=self.SAMPLE_RATE, channels=self.CHANNELS, dtype='int16')
        sd.wait()

        print("Recording finished.")

        # Save audio to file
        with wave.open(self.OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(recording.tobytes())
    
    def recognize_audio(self) -> str:
        audio_file = self.OUTPUT_FILENAME
        with sr.AudioFile(audio_file) as source:
            # Record the audio data
            audio_data = self.recognizer.record(source)

            try:
                # Recognize the speech
                text = self.recognizer.recognize_whisper(audio_data)
                return text
            except sr.UnknownValueError:
                print("Speech recognition could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from service; {e}")
        return ""