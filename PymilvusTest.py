# 向量存储
from sentence_transformers import SentenceTransformer

import DataClear
from DataBase import Milvus

xinghuo_response=DataClear.jsondata
print("xinghuo API 的响应1:", xinghuo_response)



性格特征=xinghuo_response["性格特征"]
背景故事=xinghuo_response["背景故事"]
经历与挑战=xinghuo_response["经历与挑战"]
爱好=xinghuo_response["爱好"]
口头禅=xinghuo_response["口头禅"]


print("xinghuo API 的响应1:", 性格特征)

print("xinghuo API 的响应1:", 背景故事)

print("xinghuo API 的响应:", 经历与挑战)
print("xinghuo API 的响应:", 爱好)
print("xinghuo API 的响应:", 口头禅)





# 使用 Sentence Transformers 模型
model = SentenceTransformer('all-MiniLM-L6-v2')


# 将文本向量化
background_vector = model.encode(背景故事).tolist()
personality_vector = model.encode(性格特征).tolist()
experience_vector = model.encode(口头禅).tolist()
print(f"背景故事:{background_vector}")
print(personality_vector)
print(experience_vector)

Milvus.init()