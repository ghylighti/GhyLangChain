import hanlp
import re
hanlp = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)

def split_word(text):
    word_list=hanlp(text)
    filtered_words = list(filter(lambda x: x not in '，、。！？；：', word_list))
    return filtered_words
# #去除标点符号
# def re_word(text):
#    return re.sub(r'[^\w\s]', '', text)

if __name__ == '__main__':
    split_word(text = "我爱北京天安门")