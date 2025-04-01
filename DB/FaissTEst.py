from transformers import AutoModel, AutoTokenizer
import torch

model_name = "THUDM/chatglm2-6b-int4"

# 加载 Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# 加载模型到 CPU
model = AutoModel.from_pretrained(model_name, trust_remote_code=True).to(device="cpu", dtype=torch.float32)

# 如果模型支持量化，可以直接在模型加载时选择量化
# 因为chatglm2-6b-int4模型本身是量化的，所以不需要再调用quantize
# 使用量化版本的模型加载
# (注意，这通常是通过模型文件本身来进行量化配置的，具体取决于如何提供)

# 进行推理
input_text = "你好，你是谁？"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs["input_ids"])

# 解码输出
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
