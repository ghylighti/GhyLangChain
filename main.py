# This is a sample Python script.
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from selfllm.xinghuoLLm import XinghuoLLm
from test.xinghuotest import xinghuoApi
# 配置星火模型的API URL和API密钥
api_url = "https://spark-api-open.xf-yun.com/v1/chat/completions"  # 替换成你的星火模型API URL
api_token = "nsVFfBjLOCzfmmgjVWFa:mRZLpSpSeiQhJWlFEzTG"  # 替换成你的API密钥

# 定义一个使用 PromptTemplate 和 LLM 结合的新的 `Runnable` 类
class XinghuoRunnable(Runnable):
    def __init__(self, prompt_template: PromptTemplate, llm: XinghuoLLm):
        self.prompt_template = prompt_template
        self.llm = llm

    def invoke(self, inputs: dict):
        # 根据输入生成提示文本
        prompt = self.prompt_template.format(**inputs)
        # 使用 LLM 生成响应
        response = self.llm._generate(prompt)
        return response

if __name__ == '__main__':
    # 创建自定义的 XinghuoLLM 实例
    xinhuo_llm= XinghuoLLm(api_url=api_url,api_token=api_token)
    # 创建一个提示模板
    prompt_template = "给定以下文本信息: {text}，你能提供进一步的解释吗?"
    prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
    # 创建 Langchain 链
    # 创建新的 Runnable 实例
    chain = XinghuoRunnable(prompt_template=prompt_template, llm=xinhuo_llm)

    # 假设用户输入的查询
    user_input = "我想了解一下 Langchain 的使用方法"

    # 使用 Xinghuo API 获取响应
    xinghuo_response = chain.invoke({"text": user_input})
    
    print("xinghuo API 的响应:", xinghuo_response)

