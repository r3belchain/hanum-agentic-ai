# core/memory_service.py
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.prompts import PromptTemplate

PATH_DB = "./data/chroma_db"

# 1. Inisialisasi Model Embedding Pilihan Lu (Qwen3)
fungsi_embedding = OllamaEmbeddings(
    model="qwen3-embedding:0.6b",  # Mempertahankan model pilihan lu
    base_url="http://localhost:11434"
)

# 2. Inisialisasi Koneksi ChromaDB dengan Koleksi Pilihan Lu
db_hanum = Chroma(
    persist_directory=PATH_DB,
    embedding_function=fungsi_embedding,
    collection_name="memori_pakar_hanum"  # Mempertahankan nama koleksi lu
)

def ambil_retriever_per_bidang(bidang, llm):
    """
    Fungsi Upgrade: Mengambil data secara cerdas dengan filter 
    metadata berdasarkan folder bidang yang dikirim oleh Router.
    """
    search_kwargs = {"k": 3}  # Mengambil 3 potongan teks paling relevan
    
    # JIKA bidangnya spesifik (bukan umum), pasang filter otomatis!
    if bidang != "umum":
        search_kwargs["filter"] = {"bidang": bidang}
        
    # Buat retriever dasar dengan filter
    base_retriever = db_hanum.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )
    
    # 3. Tambahkan Fitur Multi-Query (Agar pencarian di DB jauh lebih akurat)
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from
a vector database. Provide these alternative questions separated by newlines.
Original question: {question}""",
    )
    
    # Bungkus retriever dasar dengan kecerdasan LLM
    retriever_pintar = MultiQueryRetriever.from_llm(
        base_retriever, llm, prompt=QUERY_PROMPT
    )
    
    return retriever_pintar