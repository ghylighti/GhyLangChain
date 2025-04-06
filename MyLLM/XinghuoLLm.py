import requests
from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel




# 1. 创建一个 Pydantic 模型来管理 API 参数
class XinghuoLLmParams(BaseModel):
    api_url: str
    api_token: str

# 2. 创建一个 XinghuoLLm 类继承自 BaseLLM，并通过 Pydantic 参数传递 API URL 和 API Token
class XinghuoLLm(BaseLLM, XinghuoLLmParams):
    def __init__(self, **kwargs):
        # 使用 Pydantic 的参数验证
        super().__init__(**kwargs)

    def _generate(self, prompt: str, stop=None):
        # 调用 xinghuoApi，发送请求并返回生成的回答
        response = requests.post(
            self.api_url,
            json={
                "max_tokens": 4096,
                "top_k": 4,
                "temperature": 0.5,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "4.0Ultra"
            },
            headers={'Authorization': f'Bearer {self.api_token}'}
        )
        response.encoding = "utf-8"

        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]  # 假设返回是 JSON 格式
            return result
        else:
            return "请求失败"
    def _llm_type(self):
        return "xinghuo"


