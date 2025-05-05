import requests
import json


def get_completion(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": prompt}
    try:
        response = requests.post(url='http://127.0.0.1:5001', headers=headers, data=json.dumps(data))
        return response.json()['response']
    except Exception as e:
        return f"错误: {str(e)}"


def main():
    print("欢迎使用交互式问答CLI (输入 '退出' 或 'quit' 结束)")
    while True:
        # 获取用户输入
        prompt = input("\n请输入您的问题: ")

        # 检查退出条件
        if prompt.lower() in ['退出', 'quit']:
            print("感谢使用，再见！")
            break

        # 获取并显示回答
        response = get_completion(prompt)
        print("回答:", response)


if __name__ == '__main__':
    main()