# core/llm_service.py
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()

def ambil_model_chat(temperature=0.6):
    ollama_key = os.getenv("OLLAMA_API_KEY")

    if not ollama_key:
        raise ValueError("Waduh OLLAMA_API_KEY belum terpasang di file .env kamu!")

   
    llm = ChatOllama(
        base_url="https://ollama.com",  
        model="gemma4:31b-cloud",            
        temperature=temperature,
        headers={                      
            "Authorization": f"Bearer {ollama_key}"
        }
    )
    
    return llm