import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key="417becbe-4f26-4bd9-bfe7-af32b9eac9f6")

print("----- standard request -----")
completion = client.chat.completions.create(
    model="deepseek-v3-241226",
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)