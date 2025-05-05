import requests

# 代理API基本配置
API_BASE = "http://172.31.114.167"
API_KEY = "sk-test"  # 任意字符串均可

# 支持的模型列表
models = [
    "gpt-4o-mini-2024-07-18",
    "o1-preview-ca",
    "grok-3-deepsearch",
    "gpt-4o-mini"
]

# 测试提示词
prompt = "请简要介绍一下量子计算的基本原理。"

# 请求 headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求 payload 模板
def build_payload(model, prompt):
    return {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

# 遍历所有模型进行测试
for model in models:
    print(f"\n=== 正在测试模型: {model} ===")
    payload = build_payload(model, prompt)
    try:
        response = requests.post(f"{API_BASE}/v1/chat/completions", headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
        print(reply)
    except Exception as e:
        print(f"请求失败: {e}")