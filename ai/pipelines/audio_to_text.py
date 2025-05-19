import os
import uuid
from ai.utils.speech_to_text import WhisperSTT

def audio_file_to_text(audio_path: str) -> str:
    """
    다양한 형식의 오디오 파일을 Whisper 모델을 이용해 텍스트로 변환
    :param audio_path: 업로드된 오디오 파일 경로 (mp3, webm 등)
    :return: 변환된 텍스트
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"입력 파일이 존재하지 않습니다: {audio_path}")

    stt = WhisperSTT(model_size="base")
    temp_wav_path = audio_path.replace(os.path.splitext(audio_path)[-1], f"_{uuid.uuid4().hex[:8]}.wav")

    try:
        stt.convert_audio_to_wav(audio_path, temp_wav_path)
        text = stt.transcribe(temp_wav_path)
        return text

    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)