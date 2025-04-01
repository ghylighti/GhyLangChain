from langchain.document_loaders import Docx2txtLoader


def getFile():
    loader = Docx2txtLoader('D:\\360MoveData\\Users\\Administrator\\Desktop')
    text = loader.load()
    return text


class ChatDoc:
    pass


getFile()
