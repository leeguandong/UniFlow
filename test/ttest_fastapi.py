import requests
import json


def get_completion(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": prompt}
    response = requests.post(url='http://127.0.0.1:5001', headers=headers, data=json.dumps(data))
    return response.json()['response']


if __name__ == '__main__':
    print(get_completion('请简要说明，把大象放进冰箱分为几步？'))

#
# curl -X POST "http://127.0.0.1:5001"  -H 'Content-Type: application/json'  -d '{"prompt": "请简要说明，把大象放进冰箱分为几步？"}'
