import chromadb

# 创建一个 Chroma 客户端
client = chromadb.Client()

# 创建或获取一个集合（Collection），类似于一个数据库表
collection = client.create_collection(name="example_collection")

from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModel
import torch

# 使用 HuggingFace 模型生成文本嵌入（Embeddings）
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def embed(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

# 假设我们有以下文本
texts = ["你好", "Chroma 是一个向量数据库","chroma 不好用"]

# 获取文本的向量嵌入
vectors = embed(texts)

# 插入数据到 Chroma 集合
collection.add(
    documents=texts,
    embeddings=vectors.tolist(),
    metadatas=[{"source": "example"}] * len(texts),
    ids=["doc1", "doc2","doc3"]
)


# 查询文本并转换为向量
query_text = "chroma 好用吗?"
query_vector = embed([query_text])[0]

# 使用 Chroma 进行相似度查询
results = collection.query(
    query_embeddings=[query_vector.tolist()],
    n_results=1  # 返回最相似的2个结果
)

# 打印查询结果
print(results)
