import httpx
from openai import OpenAI
from configs import OPENAI_API_KEY, OPENAI_BASE_URL, logger, ENABLE_TIMING, DEFAULT_CONFIG, OPENAI_PROXY_URL
import time


class OpenAIAdapter:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=httpx.Client(proxies={"http://": OPENAI_PROXY_URL, "https://": OPENAI_PROXY_URL})
        )
        self.default_model = DEFAULT_CONFIG["openai"]["model"]
        logger.info(f"OpenAI adapter initialized with default model: {self.default_model}")

    def chat(self, messages, stream=False, tools=None, max_tokens=512, temperature=0.7):
        start_time = time.time() if ENABLE_TIMING else None
        kwargs = {
            "model": self.default_model,  # 从 DEFAULT_CONFIG 获取
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        # if tools:
        #     kwargs["tools"] = tools
        try:
            if stream:
                response = self.client.chat.completions.create(**kwargs, stream=True)
                result = (chunk.choices[0].delta.content or "" for chunk in response)
                if ENABLE_TIMING:
                    logger.info(f"OpenAI stream chat started in {time.time() - start_time:.3f} seconds")
                return result, None
            else:
                response = self.client.chat.completions.create(**kwargs)
                result = response.choices[0].message.content
                if ENABLE_TIMING:
                    logger.info(f"OpenAI chat completed in {time.time() - start_time:.3f} seconds")
                return result, None
        except Exception as e:
            logger.error(f"OpenAI chat failed: {str(e)}", exc_info=True)
            raise
