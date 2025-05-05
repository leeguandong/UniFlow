import subprocess
from configs import VLLM_MODEL_PATH, VLLM_PORT, logger

def start_vllm_service():
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", VLLM_MODEL_PATH,
        "--port", str(VLLM_PORT)
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info(f"Started vLLM service on port {VLLM_PORT}")
    process.wait()  # 等待进程完成，手动停止需外部终止

if __name__ == "__main__":
    start_vllm_service()