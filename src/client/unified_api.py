import time
import base64
from client.adapters.openai_adapter import OpenAIAdapter
from client.adapters.volcengine_adapter import VolcengineAdapter
from client.adapters.vllm_adapter import VLLMAdapter
from client.adapters.transformer_adapter import TransformerAdapter
from configs import DEFAULT_PLATFORM, ENABLE_TIMING, DEFAULT_CONFIG, logger

class UnifiedAPI:
    ADAPTER_CLASSES = {
        "openai": OpenAIAdapter,
        "volcengine": VolcengineAdapter,
        "vllm": VLLMAdapter,
        "transformer": TransformerAdapter,
    }

    def __init__(self):
        self._adapters = {}
        logger.info("UnifiedAPI initialized")

    def _get_adapter(self, platform):
        if platform not in self.ADAPTER_CLASSES:
            logger.error(f"Unsupported platform: {platform}")
            raise ValueError(f"Unsupported platform: {platform}")
        if platform not in self._adapters:
            self._adapters[platform] = self.ADAPTER_CLASSES[platform]()
        return self._adapters[platform]

    def chat(self, prompt, platform=DEFAULT_PLATFORM, system_prompt=None, max_tokens=None, temperature=None, stream=False, image_path=None):
        start_time = time.time() if ENABLE_TIMING else None
        config = DEFAULT_CONFIG.get(platform, DEFAULT_CONFIG[DEFAULT_PLATFORM]).copy()
        if system_prompt is not None:
            config["system_prompt"] = system_prompt
        if max_tokens is not None:
            config["max_tokens"] = max_tokens
        if temperature is not None:
            config["temperature"] = temperature

        messages = [{"role": "system", "content": config["system_prompt"]}]
        if image_path:
            if platform not in ["openai"]:
                logger.warning(f"Platform {platform} does not support multimodal input. Ignoring image.")
                messages.append({"role": "user", "content": prompt})
            else:
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                })
        else:
            messages.append({"role": "user", "content": prompt})

        adapter = self._get_adapter(platform)
        try:
            result, _ = adapter.chat(messages, stream=stream, max_tokens=config["max_tokens"], temperature=config["temperature"])
            if ENABLE_TIMING:
                logger.info(f"UnifiedAPI chat completed for {platform} in {time.time() - start_time:.3f} seconds")
            logger.info(f"Prompt: {prompt}, Response: {result}")
            return result
        except Exception as e:
            logger.error(f"UnifiedAPI chat failed for platform {platform}: {str(e)}", exc_info=True)
            raise