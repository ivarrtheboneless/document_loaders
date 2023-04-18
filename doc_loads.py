from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import YoutubeLoader


def word_doc(document_name):
    loader = UnstructuredWordDocumentLoader(document_name + ".docx")
    data = loader.load()
    return data

def web_site(website):
    loader = WebBaseLoader("website")
    data = loader.load()
    return data

#Enable the Youtube Api Authorize credentials
def youtube(link):
    loader = YoutubeLoader.from_youtube_url(link, add_video_info=True)
    data = loader.load()
    return data


