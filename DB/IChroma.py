import uuid

import chromadb
import torch
import re

from chromadb.errors import UniqueConstraintError
from langsmith import expect

from Utils import halp
from transformers import AutoModel, AutoTokenizer

from DB import Embedding

dbname="character_data"

def create_client():
    global client
    # client = chromadb.Client()
    #持久化
    client = chromadb.PersistentClient(path="./chroma_db")  # 持久化到本地
def clean_db():
    try:
        client.delete_collection(dbname)
        print(f"清除集合{dbname}")
        init()
        print(f"重新创建该集合{dbname}")
    except Exception as e:
        print(f"不存在集合{dbname}")



# 初始化 Chroma 客户端和模型
def init():
    global  collection, model, tokenizer
    # 创建一个集合来存储数据（角色信息集合）
    try:
        collection = client.create_collection(name=dbname,
                                              metadata={"hnsw:space": "cosine"})
    except UniqueConstraintError as e:
        print("该集合已经存在，直接使用")
        collection= client.get_collection(name=dbname)

    # 加载模型和 tokenizer（可以选择Sentence-BERT模型或其他合适的模型）
    # model_name = "sentence-transformers/paraphrase-MiniLM-L6-v2"
    #完全的模型，据说更准确
    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)


def chroma_get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    token_embeddings = outputs.last_hidden_state  # (batch_size, seq_len, hidden_dim)
    attention_mask = inputs['attention_mask'].unsqueeze(-1)  # (batch_size, seq_len, 1)

    # Mean pooling
    embeddings = (token_embeddings * attention_mask).sum(dim=1) / attention_mask.sum(dim=1)

    return embeddings[0].numpy()


def chroma_save_embedding(data):
    print(data)
    book, character = get_role_book(data)
    print(f"{character}=>>>{book}")
    # 向量化每个属性
    for key, value in data.items():
        for key_word in halp.split_word(value):
            id = str(uuid.uuid4())
            collection.add(
                embeddings=[Embedding.get_embedding(key_word)],  # 每个属性的单独向量
                documents=[value],  # 存储该属性的文本
                metadatas=[{"attribute": key, "character":f"{book}_{character}"}],  # 元数据
                ids=[id]  # 使用ID
            )


def get_role_book(data):
    character = data["主角姓名"]
    book = data["作品名称"]
    return extract_book_name(book), character
def extract_book_name(title):
    match = re.search(r'《(.*?)》', title)
    if match:
        return match.group(1)
    return title  # 没有书名号就返回原内容

def chroma_query_embedding(query_text, top=3,character=None,book=None):
    query_embedding = Embedding.get_embedding(query_text)  # 这里修正：转换为 list
    results = collection.query(
        query_embeddings=[query_embedding],  # 这里修正：必须是 list 的 list
        n_results=top,  # 这里修正：不需要 query_texts
        include = ["metadatas","documents"],  # 让结果包含存储的向量
        where={"character": f"{book}_{character}"}
    )
    # results = collection.get(include=["documents", "metadatas"])
    # for doc, meta in zip(results["documents"], results["metadatas"]):
    #     print(f"存储内容: {doc}，元数据: {meta}")
    return results



