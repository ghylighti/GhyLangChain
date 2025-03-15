import uuid

from transformers import AutoModel, AutoTokenizer
import torch
import chromadb


# 初始化 Chroma 客户端和模型
def init():
    global client, collection, model, tokenizer
    # 初始化 Chroma 客户端
    client = chromadb.Client()

    # 创建一个集合来存储数据（角色信息集合）
    collection = client.create_collection("character_data")

    # 加载模型和 tokenizer（可以选择Sentence-BERT模型或其他合适的模型）
    model_name = "sentence-transformers/paraphrase-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)


# 获取文本的向量
def chroma_get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.pooler_output[0].numpy()  # 返回句子级的向量


# 向 Chroma 数据库中保存向量
def chroma_save_embedding(data):
    character=data["主角姓名"]
    # 向量化每个属性
    embeddings = {key: value for key, value in data.items()}

    # 插入角色的属性和它们的向量
    for key, value in embeddings.items():
        id = str(uuid.uuid4())
        collection.add(
            embeddings=chroma_get_embedding(embeddings.get(key)),
            documents=[value],  # 向量数据
            metadatas=[{"attribute": key,"character":character}],  # 每个向量的元数据，标明属性名称
            ids=[id] # 使用属性名称作为ID
        )


# 查询 Chroma 数据库中的向量
def chroma_query_embedding(query_text, top=3,usr_name=''):

    # 使用 Chroma 进行相似度查询
    results = collection.query(
        query_texts=query_text,
        n_results=top,  # 返回最相似的结果
    )
    return results


# 示例：如何使用
# if __name__ == "__main__":
#     init()  # 初始化 Chroma 客户端和模型
#
#     # 示例数据
#     data = {
#         "性格特征": "单纯、善良、好战、勤奋",
#         "背景故事": "悟空是来自第七宇宙的赛亚人，自幼被送往地球，后因战斗天赋和善良的性格成为保护地球的英雄。他经历了多次生死考验，包括与弗利萨、沙鲁、魔人布欧等强敌的战斗，并在战斗中不断成长。",
#         "经历与挑战": "悟空在多次战斗中遭遇了强大的对手，如弗利萨、沙鲁、魔人布欧等。他在每次战斗中都面临着巨大的挑战，但凭借着自己的努力和坚持，最终战胜了这些强敌。此外，他还在阴间勤学苦练，不断提升自己的实力。",
#         "口头禅": "没有特定的口头禅，但在战斗中会喊出“龟派气功”等招式名称。",
#         "爱好": "修行、战斗、保护地球",
#         "主角姓名": "孙悟空"
#     }
#
#     # 保存数据
#     chroma_save_embedding(data)
#
#     # 查询文本并返回相似度最高的结果
#     query_text = "悟空的背景故事是什么？"
#     results = chroma_query_embedding(query_text, top=3)
#     print(results)
