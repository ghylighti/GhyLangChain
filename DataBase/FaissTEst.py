import faiss
import numpy as np

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True).float()

while True:
    query = input("User: ")
    response, _ = model.chat(tokenizer, query)
    print("ChatGLM:", response)


# from transformers import AutoTokenizer, AutoModel
#
#
# # 加载 ChatGLM 模型
# tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
# model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

# # 进行对话
# history = []
# while True:
#     query = input("User: ")
#     response, history = model.chat(tokenizer, query, history=history)
#     print("ChatGLM:", response)
#
# # 设定向量维度
# d = 128  # 128维向量
# index = faiss.IndexFlatL2(d)  # L2 距离索引
#
# # 生成随机向量数据（假设有 10 个向量）
# np.random.seed(42)
# data = np.random.random((10, d)).astype('float32')
#
# # 添加向量到索引
# index.add(data)
# print(f"当前索引中的向量数量: {index.ntotal}")  # 10
#
#
# # 生成一个查询向量
# query_vector = np.random.random((1, d)).astype('float32')
#
# # 搜索索引中最接近的 3 个向量
# D, I = index.search(query_vector, k=3)
# print(f"查询结果的索引: {I}")
# print(f"对应的距离: {D}")
