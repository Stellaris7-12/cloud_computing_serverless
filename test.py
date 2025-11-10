'''import requests
import json

# Local and remote URLs
url_local = 'http://localhost:8080/2015-03-31/functions/function/invocations'
url_lambda = "https://<your_api_id>.execute-api.us-east-1.amazonaws.com/default/<your_lambda_function>"

# Input data wrapped in a "body" field for Lambda
data1 = {"values": [[0.1, 2, 0.1, 3]]}
data2 = {"values": [[5.9, 3.0, 5.1, 2.3]]}

# Prepare the payload to match the Lambda's expectation (event body)
payload1 = {"body": json.dumps(data1)}
payload2 = {"body": json.dumps(data2)}

# Send the requests
result1 = requests.post(url_local, json=payload1).json()
result2 = requests.post(url_local, json=payload2).json()

# Print the results
print(result1, result2)
'''

# 修改 test.py，先只测试本地
import requests
import json
import sys

# 配置
LOCAL_MODE = True  # 设置为 False 当你想测试远程时
url_local = 'http://localhost:8080/2015-03-31/functions/function/invocations'
url_lambda = "https://YOUR_ACTUAL_API_ID.execute-api.us-east-1.amazonaws.com/default/iris-model-lambda"

# 测试数据
test_data = [
    {"values": [[5.1, 3.5, 1.4, 0.2]]},  # 预期: Setosa (0)
    {"values": [[6.7, 3.1, 4.4, 1.4]]},  # 预期: Versicolor (1)
    {"values": [[5.9, 3.0, 5.1, 2.3]]}   # 预期: Virginica (2)
]

def test_local():
    """测试本地Docker容器"""
    print("🔧 测试本地Docker容器...")
    for i, data in enumerate(test_data, 1):
        try:
            # 本地测试需要包装在 "body" 中
            payload = {"body": json.dumps(data)}
            response = requests.post(url_local, json=payload, timeout=10)
            print(f"测试 {i}: {data['values'][0]}")
            print(f"响应: {response.json()}")
            print("-" * 40)
        except Exception as e:
            print(f"❌ 测试 {i} 失败: {e}")

def test_remote():
    """测试远程API Gateway"""
    print("🌐 测试远程API Gateway...")
    for i, data in enumerate(test_data, 1):
        try:
            # 远程测试直接发送数据，不需要 "body" 包装
            response = requests.post(url_lambda, json=data, timeout=10)
            print(f"测试 {i}: {data['values'][0]}")
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            print("-" * 40)
        except Exception as e:
            print(f"❌ 测试 {i} 失败: {e}")

if __name__ == "__main__":
    if LOCAL_MODE:
        test_local()
    else:
        # 只有在完成API Gateway配置后，才设置 LOCAL_MODE = False
        if "YOUR_ACTUAL_API_ID" in url_lambda:
            print("❌ 请先更新 url_lambda 中的 API ID 和函数名称！")
            print("当前URL:", url_lambda)
            sys.exit(1)
        test_remote()