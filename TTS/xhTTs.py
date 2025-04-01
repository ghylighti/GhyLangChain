import base64
import json
import hashlib
import hmac
import time
import asyncio
import websockets
from urllib.parse import urlparse, urlencode

# 生成请求签名
def get_ws_auth_url():
    app_id = "1690d84f"  # 替换为您的 APPID
    api_key = "dc7ea49d5abe67227218ce8a44c04063"  # 替换为您的 APIKey
    api_secret = "NDE1MjQzZWMzYTk2ODExMjRlODQ5N2Yw"  # 替换为您的 APISecret

    # 计算时间戳和GMT时间
    now = int(time.time())
    date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(now))

    # 创建签名原始字符串
    host = "tts-api.xfyun.cn"
    request_line = "GET /v2/tts HTTP/1.1"
    signature_origin = f"host: {host}\ndate: {date}\n{request_line}"

    # 使用 HMAC-SHA256 生成签名
    signature_sha = hmac.new(api_secret.encode(), signature_origin.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode()

    # 构建 authorization 参数
    authorization_origin = f'api_key="{api_key}",algorithm="hmac-sha256",headers="host date request-line",signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode()).decode()

    # 构建查询参数
    query_params = {
        "authorization": authorization,
        "date": date,
        "host": host
    }

    # 构建 WebSocket 请求 URL
    ws_url = f"wss://{host}/v2/tts?{urlencode(query_params)}"
    return ws_url

## WebSocket 连接函数
async def tts_websocket(text):
    ws_url = get_ws_auth_url()
    audio_data = b""  # 用于存储音频数据

    async with websockets.connect(ws_url) as websocket:
        message = {
            "common": {
                "app_id": "1690d84f"  # 替换为您的 APPID
            },
            "business": {
                "aue": "lame",  # 音频编码为 MP3
                "sfl": 1,       # 开启流式返回
                "auf": "audio/L16;rate=16000",  # 音频采样率为 16k
                "vcn": "xiaoyan",  # 发音人
                "speed": 50,       # 语速
                "volume": 50,      # 音量
                "pitch": 50,       # 音高
                "bgs": 0,          # 无背景音
                "tte": "UTF8",      # 文本编码格式
                "reg": "2",        # 英文发音方式
                "rdn": "0"         # 数字发音方式
            },
            "data": {
                "status": 2,
                "text": base64.b64encode(str(text).encode()).decode()  # 进行Base64编码
            }
        }

        await websocket.send(json.dumps(message))

        while True:
            # 接收响应
            response = await websocket.recv()
            response_data = json.loads(response)

            # 检查返回数据
            if response_data.get("code") != 0:
                print(f"错误: {response_data.get('message')}")
                break

            # 处理音频数据
            if "data" in response_data and response_data["data"] is not None:
                audio = response_data["data"].get("audio")
                if audio:
                    audio_data += base64.b64decode(audio)

                # 合成状态检查
                status = response_data["data"].get("status")
                if status == 2:  # 合成完成
                    print("音频合成完成，保存音频文件...")
                    with open("tts_output.mp3", "wb") as audio_file:
                        audio_file.write(audio_data)
                    print("音频文件已保存为 tts_output.mp3")
                    break
                elif status == 1:  # 合成中
                    ced = response_data["data"].get("ced", "0")
                    print(f"合成进度: {ced} 字节")
                else:
                    print("未知状态")
                    break
            else:
                print("接收到空数据或无音频数据")
                break

# 运行 WebSocket 连接
# asyncio.run(tts_websocket("大家好，我是孙悟空"))