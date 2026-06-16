# core/agent_router.py
import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

BASE_DIR = "./data/knowledge_base"

def tentukan_agen_dan_bidang(pertanyaan_user):

    if os.path.exists(BASE_DIR):
        bidang_tersedia = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
    else:
        bidang_tersedia = []
        
    daftar_pilihan = bidang_tersedia + ["umum"]
    

    system_instruction = (
        "Kamu adalah AI Agent Router kaku yang bertugas mengklasifikasikan pertanyaan user.\n"
        f"Tugasmu HANYA membalas dengan salah satu kata kunci dari daftar berikut: {daftar_pilihan}\n\n"
        "Aturan Ketat:\n"
        "1. JANGAN JAWAB DENGAN KALIMAT, PENJELASAN, ATAU BASA-BASI.\n"
        "2. HANYA KELUARKAN SATU KATA SAJA YANG ADA DI DALAM DAFTAR.\n"
        "3. Jika pertanyaan berupa sapaan (halo, hai) atau tidak cocok dengan bidang apa pun, "
        "wajib jawab dengan kata: 'umum'."
    )
    

    llm = ChatOllama(
        model="deepseek-r1:1.5b", 
        temperature=0
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("user", "{input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        raw_response = chain.invoke({"input": pertanyaan_user}).strip().lower()
        
        # Antisipasi wajib: Potong pemikiran internal (<think>...</think>) milik model lokal
        if "</think>" in raw_response:
            hasil_klasifikasi = raw_response.split("</think>")[-1].strip()
        else:
            hasil_klasifikasi = raw_response
            
        # 4. Validasi hasil pencocokan kata kunci
        for pilihan in daftar_pilihan:
            if pilihan.lower() in hasil_klasifikasi:
                return pilihan  # Mengembalikan nama folder asli (menjaga casing asli)
                
        return "umum"
        
    except Exception as e:
        print(f"[ROUTER ERROR] Gagal mengklasifikasikan bidang secara lokal: {e}")
        return "umum"