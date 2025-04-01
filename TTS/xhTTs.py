import base64
import json
import hashlib
import hmac
import time
import asyncio
import websockets
import pygame
import io
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
async def tts_websocket(ans):
    ws_url = get_ws_auth_url()

    pygame.mixer.init()  # 初始化 Pygame 音频

    async with websockets.connect(ws_url,close_timeout=30) as websocket:
        message = {
            "common": {"app_id": "1690d84f"},
            "business": {
                "aue": "lame", "sfl": 1, "auf": "audio/L16;rate=16000",
                "vcn": "qianhui", "speed": 50, "volume": 50,
                "pitch": 50, "bgs": 0, "tte": "UTF8",
                "reg": "2", "rdn": "0"
            },
            "data": {
                "status": 2,
                "text": base64.b64encode(str(ans).encode()).decode()
            }
        }

        await websocket.send(json.dumps(message))

        mp3_data = io.BytesIO()

        while True:
            response = await websocket.recv()
            response_data = json.loads(response)

            if response_data.get("code") != 0:
                print(f"错误: {response_data.get('message')}")
                break

            if "data" in response_data and response_data["data"] is not None:
                audio = response_data["data"].get("audio")
                if audio:
                    mp3_data.write(base64.b64decode(audio))

                status = response_data["data"].get("status")
                if status == 2:  # 语音合成完成
                    break

        # 播放音频
        mp3_data.seek(0)
        pygame.mixer.music.load(mp3_data, "mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)  # 让事件循环继续执行


# asyncio.run(tts_websocket())