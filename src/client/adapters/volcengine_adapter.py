import os
from volcenginesdkarkruntime import Ark
from configs import VOLCENGINE_API_KEY, logger, ENABLE_TIMING, DEFAULT_CONFIG
import time

class VolcengineAdapter:
    def __init__(self):
        self.client = Ark(api_key=VOLCENGINE_API_KEY)
        self.default_model = DEFAULT_CONFIG["volcengine"]["model"]
        logger.info(f"Volcengine adapter initialized with default model: {self.default_model}")

    def chat(self, messages, stream=False, tools=None, max_tokens=512, temperature=0.7):
        start_time = time.time() if ENABLE_TIMING else None
        try:
            kwargs = {
                "model": self.default_model,  # 从 DEFAULT_CONFIG 获取
                "messages": messages,
                # "max_tokens": max_tokens,
                # "temperature": temperature
            }
            if stream:
                response = self.client.chat.completions.create(**kwargs, stream=True)
                def stream_generator():
                    for chunk in response:
                        if not chunk.choices:
                            continue
                        content = chunk.choices[0].delta.content or ""
                        yield content
                if ENABLE_TIMING:
                    logger.info(f"Volcengine stream chat started in {time.time() - start_time:.3f} seconds")
                return stream_generator(), None
            else:
                response = self.client.chat.completions.create(**kwargs)
                result = response.choices[0].message.content
                if ENABLE_TIMING:
                    logger.info(f"Volcengine chat completed in {time.time() - start_time:.3f} seconds")
                return result, None
        except AttributeError as e:
            logger.error(f"Volcengine chat failed: {str(e)}", exc_info=True)
            raise