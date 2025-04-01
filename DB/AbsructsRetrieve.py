from abc import ABC, abstractmethod
from langchain.llms import OpenAI
from langchain.chains import ConversationChain


# 抽象类，定义检索接口
class VectorRetrieval(ABC):
    @abstractmethod
    def retrieve(self, query: str):
        """
        这个方法将用于检索相关文档或信息。
        如果不进行检索，可以空实现，或者返回空。
        """
        pass


# 空实现：不做检索
class NoRetrieval(VectorRetrieval):
    def retrieve(self, query: str):
        # 空实现，表示不进行检索
        print(f"跳过检索，直接处理查询：{query}")
        return None


# 对话链类，利用 LLM 生成回答
class ConversationWithRetrieval:
    def __init__(self, llm: OpenAI, retrieval: VectorRetrieval):
        self.llm = llm
        self.retrieval = retrieval
        self.conversation = ConversationChain(llm=self.llm)

    def predict(self, user_input: str):
        # 如果有检索需求，可以调用检索
        retrieval_result = self.retrieval.retrieve(user_input)

        # 可以根据检索的结果进行处理，或者跳过
        if retrieval_result:
            # 你可以将检索结果传递给模型，或者做一些预处理
            print(f"检索到结果：{retrieval_result}")
        else:
            print(f"没有进行检索，直接生成回答。")

        # 使用模型生成回答
        response = self.conversation.predict(input=user_input)
        return response