# 原始文本
import re
import string

text = "你好，世界！这是一个测试。"


def delete_marks(txt):
    # 使用 string.punctuation 获取所有标点符号
    translator = str.maketrans('', '', string.punctuation)
    # 去掉标点符号
    cleaned_text = txt.translate(translator)
    return cleaned_text

def extract_book_name(title):
    match = re.search(r'《(.*?)》', title)
    if match:
        return match.group(1)
    return title  # 没有书名号就返回原内容