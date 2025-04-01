import tempfile
from models import db, AudioRecord
from utils.speech import speech_to_text, text_to_speech

def process_audio_input(session_id: str, audio_file) -> str:
    """处理语音输入"""
    # 保存临时音频文件
    with tempfile.NamedTemporaryFile(suffix='.wav') as tmp_file:
        audio_file.save(tmp_file.name)
        
        # 语音转文字
        text = speech_to_text(tmp_file.name)
        
        # 保存原始音频记录
        audio_record = AudioRecord(
            session_id=session_id,
            audio_path=tmp_file.name,
            transcript=text
        )
        db.session.add(audio_record)
        db.session.commit()
    
    return text

def generate_audio_response(text: str) -> str:
    """生成语音响应"""
    output_path = text_to_speech(text)
    return output_path