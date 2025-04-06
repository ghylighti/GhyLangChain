# This is a sample Python script.
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import DataClear
from DB import IChroma
from MyLLM.XinghuoLLm import XinghuoLLm
from Loader import Loader
from Const import Const, PromptTemp

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


xinhuo_llm = XinghuoLLm(api_url=Const.api_url, api_token=Const.api_token)
def load(url):
    user_input= Loader.html_loader(url)
    # 创建自定义的 XinghuoLLM 实例
    xinhuo_llm = XinghuoLLm(api_url=Const.api_url, api_token=Const.api_token)
    # 创建一个提示模板
    prompt = PromptTemplate(input_variables=["input_text"], template=PromptTemp.prompt_template)
    # 创建新的 Runnable 实例
    chain = XinghuoRunnable(prompt_template=prompt, llm=xinhuo_llm)
    # 使用 Xinghuo API 获取响应
    xinghuo_response = chain.invoke({"input_text": user_input})
    content=DataClear.extract_first_json(xinghuo_response)
    # xinghuo_response = DataClear.jsondata
    IChroma.chroma_save_embedding(content)
def query(ques,charset,book):
    result = IChroma.chroma_query_embedding(ques, 2,charset, book)
    print("向量查询", result)
    return result

def get_prompt(question,result,role,book):
    prompt1 = PromptTemplate(input_variables=["book", "role", "tips", "question"], template=PromptTemp.prompt_question)
    ##确定答案后，调用gpt回答
    # 创建新的 Runnable 实例
    chain1 = XinghuoRunnable(prompt_template=prompt1, llm=xinhuo_llm)
    xinghuo_response = chain1.invoke(
        {
            'book': book,
            'role': role,
            'tips': '。'.join(result.get('documents')[0]),
            'question': question
        }
    )
    return xinghuo_response


if __name__ == '__main__':
    "0"

