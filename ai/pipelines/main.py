from ai.utils.speech_to_text import WhisperSTT

def main():
    stt = WhisperSTT()
    stt.convert_audio_to_wav("uploads/audio_file.mp3", "temp.wav")
    text = stt.transcribe("temp.wav")
    print("STT 결과:", text)

if __name__ == "__main__":
    main()
