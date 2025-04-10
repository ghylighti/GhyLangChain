## 项目介绍

LangChain开发的一个角色聊天智能体。
使用document_loaders学习外部知识，基于chroma向量库检索召回。
大模型底座和TTS服务用的讯飞星火的。如果有自己的模型可以自行修改

# 项目命令行操作文档

该文档介绍了如何使用命令行界面（CLI）与系统进行交互，以及各个命令的功能和用法。
启动类：CMDMain
## 命令列表

### 1. `hello`
**功能：**  
打印问候信息。如果提供了名字作为参数，将显示包含名字的问候；否则，显示通用的问候信息。

**用法：**  
`hello [name]`

---

### 2. `clean`
**功能：**  
清除数据库。

**用法：**  
`clean`

---

### 3. `exit`
**功能：**  
退出命令行界面。

**用法：**  
`exit`

---

### 4. `EOF`
**功能：**  
处理 Ctrl+D（EOF）输入以退出 CLI。

**用法：**  
`[按下 Ctrl+D]`

---

### 5. `spk`
**功能：**  
使用问答系统进行交互。根据输入的问题（`arg`）查询相关信息，并通过 TTS 播放结果。

**用法：**  
`spk [question]`

---

### 6. `load`
**功能：**  
加载指定的 HTML 知识库。

**用法：**  
`load [html_file]`

---

### 7. `role`
**功能：**  
设置系统的角色。

**用法：**  
`role [role_name]`

---

### 8. `book`
**功能：**  
设置当前的书籍或知识库。

**用法：**  
`book [book_name]`

## 后续开发
1. 记忆化
2. 情感采集
3. fastApi
