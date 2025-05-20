from pydub import AudioSegment
import whisper
import os

class WhisperSTT:
    def __init__(self, model_size: str = "base"):
        """
        Whisper 모델 초기화
        :param model_size: base, small, medium, large 등 중 선택
        """
        self.model = whisper.load_model(model_size)

    def convert_audio_to_wav(self, input_path: str, output_path: str) -> None:
        """
        다양한 포맷의 오디오 파일을 wav 형식으로 변환
        :param input_path: 입력 오디오 파일 경로
        :param output_path: 출력 wav 경로
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"입력 오디오 파일이 존재하지 않습니다: {input_path}")

        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")

    def transcribe(self, wav_path: str) -> str:
        """
        wav 파일을 Whisper로 텍스트로 변환
        :param wav_path: wav 파일 경로
        :return: 변환된 텍스트
        """
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"wav 파일이 존재하지 않습니다: {wav_path}")

        result = self.model.transcribe(wav_path)
        return result["text"]
