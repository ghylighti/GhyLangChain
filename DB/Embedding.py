from torch import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

# 载入模型（可以换成 'BAAI/bge-large-zh' 适应更大数据）
model_name = "BAAI/bge-base-zh"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 生成嵌入向量
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# 计算余弦相似度
def cosine_similarity(v1, v2):
    v1 = torch.from_numpy(v1)  # 转换 NumPy 数组为 Tensor
    v2 = torch.from_numpy(v2)
    return torch.nn.functional.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item()

if __name__ == '__main__':
    var = 0