from openai import OpenAI
from configs import VLLM_API_BASE, logger, ENABLE_TIMING, DEFAULT_CONFIG
import time

class VLLMAdapter:
    def __init__(self):
        self.client = OpenAI(base_url=VLLM_API_BASE, api_key="dummy")
        self.default_model = DEFAULT_CONFIG["vllm"]["model"]
        logger.info(f"vLLM adapter initialized with default model: {self.default_model}")

    def chat(self, messages, stream=False, tools=None, max_tokens=512, temperature=0.7):
        start_time = time.time() if ENABLE_TIMING else None
        kwargs = {
            "model": self.default_model,  # 从 DEFAULT_CONFIG 获取
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        try:
            if stream:
                response = self.client.chat.completions.create(**kwargs, stream=True)
                result = (chunk.choices[0].delta.content or "" for chunk in response)
                if ENABLE_TIMING:
                    logger.info(f"vLLM stream chat started in {time.time() - start_time:.3f} seconds")
                return result, None
            else:
                response = self.client.chat.completions.create(**kwargs)
                result = response.choices[0].message.content
                if ENABLE_TIMING:
                    logger.info(f"vLLM chat completed in {time.time() - start_time:.3f} seconds")
                return result, None
        except Exception as e:
            logger.error(f"vLLM chat failed: {str(e)}", exc_info=True)
            raise