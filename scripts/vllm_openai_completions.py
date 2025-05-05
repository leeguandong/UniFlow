# vllm_openai_completions.py
from openai import OpenAI
client = OpenAI(
    base_url="http://127.0.0.1:5001/v1",
    api_key="sk-xxx", # 随便填写，只是为了通过接口参数校验
)

completion = client.chat.completions.create(
  model="DeepSeek-R1-Distill-Qwen-7B",
  messages=[
    {"role": "user", "content": "我想问你，5的阶乘是多少？<think>\n"}
  ]
)

print(completion.choices[0].message)
#curl -X POST "http://127.0.0.1:5001"  -H 'Content-Type: application/json'  -d '{"prompt": "请简要说明，把大象放进冰箱分为几步？"}'


