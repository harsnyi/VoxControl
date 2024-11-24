from audio import Audio
from utils import generate_short_id
import time
from controller import Controller

def main():
    controller = Controller()
    print("Record for 5 seconds")
    uuid = generate_short_id()
    audio = Audio(uuid=uuid)
    audio.record()
    time.sleep(1)
    print("Recognizing your voice ...")
    recognized_text = audio.recognize_audio()
    controller.run_command(recognized_text)


if __name__ == "__main__":
    main()
