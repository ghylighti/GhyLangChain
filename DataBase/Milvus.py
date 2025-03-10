from pymilvus import connections, FieldSchema, DataType, CollectionSchema, Collection
from pymilvus.orm import utility
import numpy as np  # 假设您用 NumPy 来创建 embeddings

name_db = "default"
port = "19531"
host = "localhost"

table_name = "test_table"

def init():
    # 假设 embeddings 是一个已定义的 NumPy 数组
    # 请根据实际情况定义您的 embeddings
    embeddings = np.random.random((10, 128))  # 假设有10个样本，每个样本128维

    # 连接到 Milvus 数据库
    if not connections.has_connection(name_db):
        connections.connect(name_db, host=host, port=port)
        print(f"Milvus启动成功")
    # 检查集合是否存在
    if not utility.has_collection(table_name):
        # 定义字段
        fields = [
            FieldSchema(name="text", dtype=DataType.STRING, is_primary=False),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=embeddings.shape[1])
        ]

        # 定义集合的 Schema
        schema = CollectionSchema(fields, description="Character traits embeddings")

        # 创建集合
        collection = Collection(name=table_name, schema=schema)
        print(f"Collection '{table_name}' created successfully.")
    else:
        print(f"Collection '{table_name}' already exists.")

if __name__ == '__main__':
    init()
