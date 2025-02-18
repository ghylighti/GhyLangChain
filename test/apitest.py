
import requests
import json

# 星火 API 请求地址（以示例地址为准，实际地址请查看星火官方文档）
url = "https://api.xinghuo.com/v1/chat/completions"

headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# 请求体，包含模型输入和相关配置
data = {
    "model": "xinghuo-chatbot-v1",
    "messages": [
        {"role": "system", "content": "你是一个八卦对话机器人。"},
        {"role": "user", "content": "最近有什么八卦新闻吗？"}
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print("机器人回答:", result['choices'][0]['message']['content'])
else:
    print("API 请求失败:", response.status_code)
