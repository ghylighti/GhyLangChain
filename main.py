# This is a sample Python script.
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

import DataClear
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
    prompt_template = """
    请分析以下文本主角，结合网络内容。并返回一个
    result对象，包含以下字段：
    - "性格特征"：""。
    - "背景故事"：""。
    - "经历与挑战"：""。
    - "口头禅"：""。
    - "爱好"：""。
    - "主角姓名"：""。

    文本：
    "{input_text}"
    """
    prompt = PromptTemplate(input_variables=["input_text"], template=prompt_template)
    # 创建新的 Runnable 实例
    chain = XinghuoRunnable(prompt_template=prompt_template, llm=xinhuo_llm)

    # 假设用户输入的查询
    user_input = """
    单纯，在战斗中总是愿意轻信于人，容易被别人的一面之词所迷惑，很难辨别善恶真假，因为这个原因悟空在不少战斗中吃亏（例如第六宇宙和第七宇宙举办武道大会的时候，悟空就因为弗罗斯特向他很友好，并且还向第七宇宙的其他人打招呼，所以就轻信弗罗斯特是好人了，最后因为麻痹大意，中了弗罗斯特的毒针，因此输掉了比赛），有利也有弊。因为单纯，悟空能够免疫恶魔人的恶魔光线，而且悟空还能够乘坐筋斗云。
善良，内心温柔心肠柔软，不会轻易要人的性命（除非像比克大魔王、沙鲁、原始魔人布欧、扎马斯那样一心想毁灭或者征服世界之人），虽是好战的赛亚人，但战斗经常点到即止，不会主动杀害对手，或者是希望他能留下来，将来能有交手的机会（例如当贝吉塔在那美克星被弗利萨杀死时，悟空不管他是不是敌人，都亲手埋葬他，并说出贝吉塔虽很令他讨厌，但承认他是赛亚人的荣耀，自己也引以为荣。当弗利萨被自己招数击中奄奄一息的时候，万般恳求悟空救他的时候，悟空一开始虽说他太可恶，却还是分自己一点气给他让他能活下去。 亲手杀掉小布欧后还向阎王许愿，希望再次遇到布欧并让他转世，这才有欧布的诞生）。
好战，悟空是个武痴，每当有实力强劲的对手出现，都会令他感到兴奋。不管是从拉蒂兹口中得知有两名最强的赛亚人，还是那美克星上有比贝吉塔更强的气，都让他悲喜交加，他追求比赛公平。当武道会被比克废掉四肢，神仙提议围攻比克时，悟空却因这是比赛而反对。当沙鲁游戏时伙伴们都想着悟饭能跟消耗部分体力的沙鲁战斗时，悟空却主动给沙鲁仙豆以求公平。在与希特一战时为让其使出真正实力，请求裁判将“不能杀死参赛者”的规定取消。
勤奋，他是个修行“狂人”。死后也仍在阴间勤学苦练，悟空知道和自己交过手的人，有好多都是天赋要强于他的，悟空也不得不努力。悟空连种田的时候都想着要修炼，时不时就想着去界王神那里去修炼。包括在比鲁斯星的修炼过程中，悟空也是丝毫都没有懈怠。以至在和布欧交锋时贝吉塔都不得不承认对悟空的钦佩。
    """

    # 使用 Xinghuo API 获取响应
    # xinghuo_response = chain.invoke({"input_text": user_input})
    xinghuo_response=DataClear.jsondata

    print("xinghuo API 的响应:", xinghuo_response)

