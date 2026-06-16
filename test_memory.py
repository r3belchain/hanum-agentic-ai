# test_memory.py
import os
from typing import Annotated, TypedDict
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from rich.console import Console
from rich.panel import Panel


from core.llm_service import ambil_model_chat


console = Console()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def hanum_chat_node(state: AgentState, config, *, store):
  
    user_id = config["configurable"].get("user_id", "guest_user")
    namespace = ("users", user_id, "profile")
    

    memories = store.search(namespace)
    
    konteks_long_term = ""
    if memories:
        konteks_long_term = "\n[MEMORI JANGKA PANJANG KAMU] Kamu mengingat fakta permanen ini tentang user:\n"
        for item in memories:
            konteks_long_term += f"- {item.key}: {item.value}\n"
            
        console.print(f"[bold yellow][STORE] Mengambil memori jangka panjang untuk {user_id}...[/bold yellow]")
    

    system_instruction = (
        "Kamu adalah Hanum Agentic AI yang dibangun oleh Azhar Aufa. "
        "Gaya bicaramu santai, sopan, dan panggil user dengan 'Kamu'."
    )
    
    # Jika ada memori jangka panjang, suntikkan ke dalam instruksi sistem
    if konteks_long_term:
        system_instruction += konteks_long_term

    # Susun ulang pesan yang akan dikirim ke Gemma 4 Cloud
    full_messages = [SystemMessage(content=system_instruction)] + state["messages"]
    
    # Panggil model Gemma 4 Cloud lu
    llm = ambil_model_chat(temperature=0.6)
    response = llm.invoke(full_messages)
    
    return {"messages": [response]}

# 3. PERAKITAN GRAF (COMPILING ARTIFACTS)
workflow = StateGraph(AgentState)
workflow.add_node("hanum_core", hanum_chat_node)
workflow.add_edge(START, "hanum_core")
workflow.add_edge("hanum_core", END)

# Inisialisasi dua lapisan memori sesuai dokumentasi
checkpointer = InMemorySaver()  # Short-term (per thread)
long_term_store = InMemoryStore()  # Long-term (lintas thread)

# Satukan semuanya saat kompilasi
graph = workflow.compile(checkpointer=checkpointer, store=long_term_store)

# =================================================================
# JALUR EKSPERIMEN SIMULASI MEMORI
# =================================================================
def jalankan_tes_memori():
    console.print(Panel("[bold green]MEMULAI EKSPERIMEN MEMORI LANGGRAPH (GEMMA 4 CLOUD)[/bold green]", border_style="green"))

    # -------------------------------------------------------------
    # SKENARIO 1: Menguji Short-Term Memory (Thread 1)
    # -------------------------------------------------------------
    console.print("\n[bold cyan]=== SKENARIO 1: Sesi Chat Dimulai (Thread: thread-1) ===[/bold cyan]")
    config_1 = {"configurable": {"thread_id": "thread-1", "user_id": "azhar_aufa"}}
    
    # Kirim perkenalan diri
    input_1 = {"messages": [HumanMessage(content="Halo Hanum! Nama aku Azhar Aufa. Ingat ya.")]}
    output_1 = graph.invoke(input_1, config=config_1)
    console.print(f"[bold green]User :[/bold green] {input_1['messages'][0].content}")
    console.print(f"[bold magenta]Hanum:[/bold magenta] {output_1['messages'][-1].content}\n")
    
    # Tanya ulang di thread yang sama untuk membuktikan short-term memory bekerja
    input_2 = {"messages": [HumanMessage(content="Eh, siapa nama aku tadi?")]}
    output_2 = graph.invoke(input_2, config=config_1)
    console.print(f"[bold green]User :[/bold green] {input_2['messages'][0].content}")
    console.print(f"[bold magenta]Hanum:[/bold magenta] {output_2['messages'][-1].content}")

    # -------------------------------------------------------------
    # SKENARIO 2: Membuktikan Isolasi Thread (Short-Term Amnesia)
    # -------------------------------------------------------------
    console.print("\n[bold red]=== SKENARIO 2: Membuka Sesi Baru (Thread: thread-2) ===[/bold red]")
    config_2 = {"configurable": {"thread_id": "thread-2", "user_id": "azhar_aufa"}}
    
    # Tanya nama di thread berbeda. Seharusnya Hanum lupa karena checkpointer diisolasi per thread.
    input_3 = {"messages": [HumanMessage(content="Kamu tahu ngga siapa nama aku?")]}
    output_3 = graph.invoke(input_3, config=config_2)
    console.print(f"[bold green]User :[/bold green] {input_3['messages'][0].content}")
    console.print(f"[bold magenta]Hanum:[/bold magenta] {output_3['messages'][-1].content}")

    # -------------------------------------------------------------
    # SKENARIO 3: Menyuntikkan & Menguji Long-Term Memory (Store)
    # -------------------------------------------------------------
    console.print("\n[bold red]=== SKENARIO 3: Menyuntikkan Memori Jangka Panjang Lintas Thread ===[/bold red]")
    
    # Kita simpan fakta permanen secara manual ke dalam Store (di luar graf)
    # Analogi: Proses ini nantinya akan dilakukan secara otomatis oleh "Reflection Node"
    namespace_permanen = ("users", "azhar_aufa", "profile")
    long_term_store.put(
        namespace_permanen, 
        "hobi_dan_kopi", 
        {"hobi": "Web Pentesting & Coding", "kopi_favorit": "Spanish Aren Latte"}
    )
    console.print("[bold green][✔] Berhasil menyimpan data permanen ke SSD (InMemoryStore).[/bold green]")
    
    # Sekarang kita buka Sesi Chat Ketiga (Thread Baru Total)
    console.print("\n[bold cyan]=== Membuka Sesi Chat Ketiga (Thread: thread-3) ===[/bold cyan]")
    config_3 = {"configurable": {"thread_id": "thread-3", "user_id": "azhar_aufa"}}
    
    # Tanya tentang kesukaan. Hanum harusnya tahu dari data Store lintas thread yang kita suntikkan.
    input_4 = {"messages": [HumanMessage(content="Buatin sapaan keren yang relevan sama hobi atau kopi kesukaan aku dong!")]}
    output_4 = graph.invoke(input_4, config=config_3)
    console.print(f"[bold green]User :[/bold green] {input_4['messages'][0].content}")
    console.print(f"[bold magenta]Hanum:[/bold magenta] {output_4['messages'][-1].content}")

if __name__ == "__main__":
    jalankan_tes_memori()