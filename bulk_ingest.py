# bulk_ingest.py
import os
import pypdf
import requests
from bs4 import BeautifulSoup

# Ambil komponen inti LangChain yang DIJAMIN aman dan terus dirawat
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

BASE_DIR = "./data/knowledge_base"
PATH_DB = "./data/chroma_db"

def jalankan_pipeline_otak_hanum():
    if not os.path.exists(BASE_DIR):
        print(f"[*] Folder basis pengetahuan [{BASE_DIR}] belum ditemukan. Membuat otomatis...")
        os.makedirs(BASE_DIR, exist_ok=True)
        return

    bidang_folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
    
    embedding_model = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    vector_db = Chroma(persist_directory=PATH_DB, embedding_function=embedding_model, collection_name="memori_pakar_hanum")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    print(f"[+] Menemukan {len(bidang_folders)} bidang ilmu: {bidang_folders}")

    for bidang in bidang_folders:
        path_folder = os.path.join(BASE_DIR, bidang)
        semua_file = [f for f in os.listdir(path_folder) if f.endswith(('.pdf', '.md', '.txt'))]
        
        for nama_file in semua_file:
            jalur_file = os.path.join(path_folder, nama_file)
            print(f"--> Menscan ilmu baru: [{bidang}] -> {nama_file}")
            
            try:
                teks_mentah = ""
                
                # ========================================================
                # CARA MODERN: Membaca file secara mandiri tanpa Loader jadul
                # ========================================================
                if jalur_file.endswith('.pdf'):
                    # Baca PDF pakai pypdf standar
                    with open(jalur_file, "rb") as f:
                        pdf_reader = pypdf.PdfReader(f)
                        for page in pdf_reader.pages:
                            halaman_teks = page.extract_text()
                            if halaman_teks:
                                teks_mentah += halaman_teks + "\n"
                else:
                    # Baca file teks (.txt / .md) pakai bawaan Python
                    with open(jalur_file, 'r', encoding='utf-8') as f:
                        teks_mentah = f.read()
                
                # Bungkus teks mentah ke dalam format standar Document LangChain
                dokumen_baku = [Document(page_content=teks_mentah)]
                
                # Potong cerdas
                chunks = text_splitter.split_documents(dokumen_baku)
                
                # Suntikkan metadata bidang
                for chunk in chunks:
                    chunk.metadata["bidang"] = bidang
                    chunk.metadata["sumber_file"] = nama_file
                
                # Simpan ke database permanen
                vector_db.add_documents(chunks)
                print(f"   [SUKSES] {len(chunks)} koordinat memori disuntikkan ke klaster {bidang}.")
                
            except Exception as e:
                print(f"   [ERROR] Gagal membaca file {nama_file}: {e}")

def load_links_dari_file(jalur_file):
    """Fungsi scraper modern pengganti WebBaseLoader"""
    documents_web = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    with open(jalur_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
    for url in urls:
        print(f"      [Web] Men-scrape: {url}")
        try:
            # Scrape mandiri menggunakan requests dan BeautifulSoup
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Ambil teks bersihnya saja, buang tag script dan style css
                for script in soup(["script", "style"]):
                    script.decompose()
                teks_bersih = soup.get_text(separator="\n")
                
                # Bungkus jadi Objek Document
                doc = Document(page_content=teks_bersih, metadata={"source": url})
                documents_web.append(doc)
        except Exception as e:
            print(f"      [WARNING] Gagal men-scrape {url}: {e}")
            
    return documents_web

if __name__ == "__main__":
    jalankan_pipeline_otak_hanum()