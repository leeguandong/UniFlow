import requests
import json
import sys

# API 地址
URL = "http://localhost:8000/v1/completions"

# 请求头
HEADERS = {
    "Content-Type": "application/json"
}


def query_model(prompt):
    """向 vLLM 服务发送请求并返回结果"""
    data = {
        "model": 'DeepSeek-R1-Distill-Qwen-7B',
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["text"].strip()
        else:
            return f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        return f"发生错误: {str(e)}"


def main():
    print("欢迎使用 vLLM CLI 模式！输入 'exit' 或按 Ctrl+C 退出。")
    while True:
        try:
            # 获取用户输入
            prompt = input("请输入你的问题: ")
            if prompt.lower() == "exit":
                print("退出程序...")
                break

            if not prompt.strip():
                print("输入不能为空，请重新输入！")
                continue

            # 发送请求并显示结果
            response = query_model(prompt)
            print("模型回复:", response)
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n通过 Ctrl+C 退出程序...")
            break
        except Exception as e:
            print(f"程序出错: {str(e)}")


if __name__ == "__main__":
    main()