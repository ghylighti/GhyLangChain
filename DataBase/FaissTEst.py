
from huggingface_hub import snapshot_download

from transformers import AutoTokenizer, AutoModel
import os
import torch

# 限制 PyTorch 线程数，避免多线程冲突
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
torch.set_num_threads(1)

# 指定本地模型路径
model_path = "./models/chatglm2-6b"
snapshot_download(
    repo_id="THUDM/chatglm2-6b",
    local_dir="./models/chatglm2-6b",
    endpoint="https://hf-mirror.com"
)
import sys
sys.path.append("./models/chatglm2-6b")  # 指定本地模型路径
# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 强制使用 float32 以避免不兼容的数据类型
model = AutoModel.from_pretrained(
    model_path,
    trust_remote_code=True,
    torch_dtype=torch.float16,  # 使用更低的精度
    low_cpu_mem_usage=True  # 启用低内存模式
)


# 将模型移动到 CPU
model = model.to("cpu").eval()


while True:
    query = input("User: ")
    response, _ = model.chat(tokenizer, query)
    print("ChatGLM:", response)

# 进行对话
history = []
while True:
    query = input("User: ")
    response, history = model.chat(tokenizer, query, history=history)
    print("ChatGLM:", response)

# 设定向量维度
d = 128  # 128维向量
index = faiss.IndexFlatL2(d)  # L2 距离索引

# 生成随机向量数据（假设有 10 个向量）
np.random.seed(42)
data = np.random.random((10, d)).astype('float32')

# 添加向量到索引
index.add(data)
print(f"当前索引中的向量数量: {index.ntotal}")  # 10


# 生成一个查询向量
query_vector = np.random.random((1, d)).astype('float32')

# 搜索索引中最接近的 3 个向量
D, I = index.search(query_vector, k=3)
print(f"查询结果的索引: {I}")
print(f"对应的距离: {D}")
