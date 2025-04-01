from langchain_community.document_loaders import WebBaseLoader
# 指定要加载的网页 URL
url = "https://baike.baidu.com/item/%E5%AD%99%E6%82%9F%E7%A9%BA/5653843"


def html_loader(hurl):
    # 创建网页加载器
    loader = WebBaseLoader(hurl)
    # 加载网页内容
    docs = loader.load()
    # 打印网页文本内容
    print(docs[0].page_content)
    return docs[0]
