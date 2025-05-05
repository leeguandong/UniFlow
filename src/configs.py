import logging
import torch
import os

# OpenAI 配置
OPENAI_API_KEY = "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"
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_PROXY_URL = "http://10.231.139.4:7610"

# Volcengine 配置
VOLCENGINE_API_KEY = "417becbe-4f26-4bd9-bfe7-af32b9eac9f6"

# Transformer 配置
TRANSFORMER_MODEL_PATH = "/path/to/transformer/model"
TRANSFORMER_API_URL = "http://localhost:7001"
TRANSFORMER_PORT = 7001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID and DEVICE == "cuda" else DEVICE

# vLLM 配置
VLLM_MODEL_PATH = "/path/to/vllm/model"
VLLM_PORT = 8003
VLLM_API_BASE = f"http://localhost:{VLLM_PORT}/v1"

# 项目通用配置
DEFAULT_PLATFORM = "openai"
ENABLE_TIMING = True

# 默认配置
DEFAULT_CONFIG = {
    "openai": {
        "model": "gpt-4o-mini",
        "max_tokens": 250,
        "temperature": 0.02,
        "system_prompt": "You are a helpful assistant."},
    "volcengine": {
        "max_tokens": 512, # 为了统一接口，实际没用
        "temperature": 0.7, # 为了统一接口
        "model": "deepseek-v3-241226",
        "system_prompt": "You are a helpful AI."},
    "transformer": {
        "max_tokens": 512,
        "temperature": 0.7,
        "system_prompt": "You are a helpful assistant."},
    "vllm": {
        "max_tokens": 512,
        "temperature": 0.7,
        "system_prompt": "You are a helpful assistant."},
}

# 日志配置
LOG_FILE = "logs/uniflow.log"
import os
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)