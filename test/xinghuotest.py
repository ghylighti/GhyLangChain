import json

import requests

url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
data = {
    "max_tokens": 4096,
    "top_k": 4,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": "你好。请问今天几号"
        }
    ],
    "model": "4.0Ultra"
}
data["stream"] = False
header = {
    "Authorization": "Bearer nsVFfBjLOCzfmmgjVWFa:mRZLpSpSeiQhJWlFEzTG",
    "Content-Type": "application/json"
}


def xinghuoApi():
    response = requests.post(url, headers=header, json=data, stream=False)
    response.encoding = "utf-8"
    # 打印整个响应对象
    return response.json()["choices"][0]["message"]["content"]

    # 如果响应内容是JSON格式，并且需要解析为字典

