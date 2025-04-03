from openai import OpenAI
import dashscope

# 通义千问配置
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_API_KEY = "sk-5fb4c90206e84a7b9d88fc91e72fbe44"

# 初始化OpenAI客户端
qwen_client = OpenAI(
    base_url=QWEN_BASE_URL,
    api_key=QWEN_API_KEY
)

# 语音合成配置（来自CustomWinScript）
TTS_CONFIG = {
    "speech_key": "CmwzTb35WSvnOYEPoY9wC12ExtiNJkI37VJlc9itceLmM6osBYstJQQJ99BAACYeBjFXJ3w3AAAYACOG1fhO",
    "service_region": "eastus",
    "voice_name": "zh-cn-XiaochenNeural"
}

# 大模型配置
MODEL_CONFIG = {
    "knowledge_extract": {
        "primary_model": "qwen-plus",
        "fallback_model": "ep-20250107152728-vkl7w"
    },
    "question_generate": "qwen-plus",
    "evaluation_model": "qwen-turbo"
}

# 初始化Dashscope（用于评估）
dashscope.api_key = QWEN_API_KEY