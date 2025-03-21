"""
语音处理服务模块
实现语音识别和合成功能
"""

import azure.cognitiveservices.speech as speechsdk
from config import Config

class SpeechService:
    """语音服务封装类"""
    
    def __init__(self, config):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=config['AZURE_SPEECH_KEY'],
            region=config['AZURE_REGION']
        )
    
    def speech_to_text(self, audio_path):
        """语音转文字"""
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        result = recognizer.recognize_once()
        return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else None
    
    def text_to_speech(self, text):
        """文字转语音"""
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        result = synthesizer.speak_text(text)
        return result.audio_data