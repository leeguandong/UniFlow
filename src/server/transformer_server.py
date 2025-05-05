from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import uvicorn
import json
import datetime
import torch
import time
from configs import TRANSFORMER_MODEL_PATH, CUDA_DEVICE, logger, ENABLE_TIMING

# 清理 GPU 内存函数
def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

# 创建 FastAPI 应用
app = FastAPI(title="Transformer Server")

# 全局模型和分词器
model = None
tokenizer = None

@app.on_event("startup")
def startup_event():
    global model, tokenizer
    logger.info(f"Loading model from {TRANSFORMER_MODEL_PATH} on {CUDA_DEVICE}")
    tokenizer = AutoTokenizer.from_pretrained(TRANSFORMER_MODEL_PATH, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(
        TRANSFORMER_MODEL_PATH,
        device_map=CUDA_DEVICE,
        torch_dtype=torch.bfloat16
    )
    logger.info("Transformer model and tokenizer loaded successfully")

@app.post("/chat")
async def chat(request: Request):
    start_time = time.time() if ENABLE_TIMING else None
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get("prompt", "")
    system_prompt = json_post_list.get("system_prompt", "You are a helpful assistant.")
    max_tokens = json_post_list.get("max_tokens", 512)
    temperature = json_post_list.get("temperature", 0.7)
    stream = json_post_list.get("stream", False)  # 暂不支持流式

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        # 调用模型生成
        input_ids = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([input_ids], return_tensors="pt").to(model.device)
        generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=max_tokens)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        answer = {
            "response": response,
            "status": 200,
            "time": time_str
        }

        if ENABLE_TIMING:
            logger.info(f"Transformer chat completed in {time.time() - start_time:.3f} seconds")
        logger.info(f"Prompt: {prompt}, Response: {response}")
        torch_gc()
        return answer["response"]  # 与其他服务保持一致，仅返回 response
    except Exception as e:
        logger.error(f"Transformer chat failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, workers=1)