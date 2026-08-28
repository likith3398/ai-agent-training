import os

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

docs = DirectoryLoader(
    "day04/kb",
    glob="*.txt",
    loader_cls=TextLoader
).load()

print(f"Loaded {len(docs)} documents.")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

print(f"Created {len(chunks)} chunks.")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")