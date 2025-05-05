import requests
import json

def get_completion(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": prompt}
    response = requests.post(url='http://127.0.0.1:5001', headers=headers, data=json.dumps(data), stream=True)
    for line in response.iter_lines():
        if line:
            print(f"Received: {line.decode('utf-8')}")  # 调试打印
            yield json.loads(line.decode('utf-8'))['response']

if __name__ == '__main__':
    for chunk in get_completion('请简要说明，把大象放进冰箱分为几步？'):
        print(chunk, end="", flush=True)