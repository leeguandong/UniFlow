import httpx
from configs import TRANSFORMER_API_URL, logger, ENABLE_TIMING
import time

class TransformerAdapter:
    def __init__(self):
        self.client = httpx.Client()
        logger.info("Transformer adapter initialized")

    def chat(self, messages, stream=False, tools=None, max_tokens=512, temperature=0.7):
        start_time = time.time() if ENABLE_TIMING else None
        payload = {
            "prompt": messages[-1]["content"],
            "system_prompt": messages[0]["content"] if messages[0]["role"] == "system" else "You are a helpful assistant.",
            "max_tokens": max_tokens,
            "temperature": temperature,
            # "stream": stream
        }
        try:
            response = self.client.post(f"{TRANSFORMER_API_URL}/chat", json=payload)
            response.raise_for_status()
            result = response.json()["response"]
            if ENABLE_TIMING:
                logger.info(f"Transformer chat completed in {time.time() - start_time:.3f} seconds")
            return result, None
        except Exception as e:
            logger.error(f"Transformer chat failed: {str(e)}", exc_info=True)
            raise

    def __del__(self):
        self.client.close()