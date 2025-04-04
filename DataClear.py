import json
from Utils import halp
import re
# data="""
# ```json
# {
#     "性格特征": "勇敢、善良、乐观、坚韧不拔",
#     "背景故事": "孙悟空，原名卡卡罗特，来自贝吉塔行星的赛亚人。幼时以“下级战士”之身份被送往地球，并被武道家孙悟饭收养。因失控变为巨猿将孙悟饭踩死后独自生活在深山，后因结识布尔玛从而踏上寻找龙珠之旅。梦想是不断变强，为追求力量而刻苦修行。基于该角色影响力，自2015年起日本纪念日协会正式认定每年5月9日为“悟空纪念日”。",
#     "经历与挑战": "在地球上生活期间，孙悟空经历了许多战斗和冒险，包括与红缎军的战斗、参加天下第一武道会、对抗弗利萨、与魔人布欧的战斗等。他不断修炼提升自己的实力，保护地球和身边的人免受威胁。",
#     "口头禅": "超级赛亚人变身！龟派气功！瞬间移动!",
#
#     "爱好": "修炼、战斗、保护地球和身边的人",
#     "主角姓名": "孙悟空",
#     "打招呼": "你好啊，我是孙悟空！你是谁？",
#     "人物关系": "父亲：巴达克；母亲：姬内；哥哥：拉蒂兹；爷爷：孙悟饭（祖父）；师父：龟仙人；妻子：琪琪；儿子：孙悟饭、孙悟天；儿媳：比迪丽；亲家：牛魔王；好友：布尔玛、贝吉塔、克林、雅木茶、天津饭、饺子、比克、特兰克斯、悟天克斯、欧布、小芳；徒弟：欧布、猫魔人、卡林；敌人：桃白白、比克大魔王、弗利萨、沙鲁、魔人布欧、一星龙及其手下、扎马斯及其手下"
# }
# ```
# """

# jsondata=json.loads(data.strip().replace("```","").replace("json",""))
#提取json内容。模型返回的东西不一定是标准的json
def extract_first_json(text):
    pattern = r'(\{.*?\})'  # 尝试匹配 JSON 对象
    match_iter = re.finditer(pattern, text, re.DOTALL)

    for match in match_iter:
        json_str = match.group(1)
        try:
            return json.loads(
                json_str.strip()
                .replace("```", "")
                .replace("json", "")
                .replace("《","")
                .replace("》","")

                              )  # 解析成功就返回
        except json.JSONDecodeError:
            continue  # 如果解析失败就尝试下一个匹配
    return None  # 没找到合法的 JSON

def get_content(content):
    return json.loads(content.strip().replace("```", "").replace("json", ""))