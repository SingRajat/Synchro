import os
from dotenv import load_dotenv
from config.settings import Chroma_Persist_dir
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

class RAG_Logic:

    def __init__(self):
        self.embeddings=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
        )
    
    def Load_Doc(self,file_path):
        if file_path.endswith("pdf"):
            self.Loader=PyPDFLoader(file_path)
        else:
            self.Loader=WebBaseLoader(file_path) 
        self.doc=self.Loader.load()
        return self.doc
    
    def Split_Chunks(self):
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", ""]
        )
        self.chunks=self.splitter.split_documents(self.doc)
        return self.chunks
    
    def Vector_store(self):
        self.db=Chroma.from_documents(
            documents=self.chunks,
            embedding=self.embeddings,
            persist_directory=Chroma_Persist_Dir
        )
        return self.db

    def builder(self):
        self.Load_Doc()
        self.Split_Chunks()
        return self.Vector_store()
    



