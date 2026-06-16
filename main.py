# main.py
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style as PromptStyle

from langchain_core.prompts import ChatPromptTemplate


from core.agent_router import tentukan_agen_dan_bidang
from core.llm_service import ambil_model_chat


console = Console()

def tampilkan_banner_hermes():
    """Fungsi untuk mencetak Banner Utama yang estetik saat startup"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = Text()
    banner.append("⚡ HANUM AGENTIC AI SYSTEM v2.0 ⚡\n", style="bold magenta")
    banner.append("────────────────────────────────────────────────\n", style="dim white")
    banner.append("🧠 Core Brain : ", style="cyan")
    banner.append("Gemma 4 31b-cloud (Cloud Remote Host)\n", style="bold green")
    banner.append("────────────────────────────────────────────────\n", style="dim white")
    banner.append("Tips: Tekan [Alt + Enter] untuk mengirim perintah", style="italic italic_black")

    console.print(
        Panel(
            banner, 
            title="[bold neon_green]SYSTEM ONLINE[/bold neon_green]", 
            border_style="bright_blue",
            expand=False
        )
    )

def main():
    tampilkan_banner_hermes()
    
    # Konfigurasi style untuk prompt_toolkit input
    style_prompt = PromptStyle.from_dict({
    # Ganti 'bold neon_cyan' dengan kode Hex '#00ffff' (Cyan Neon asli)
    'prompt': 'bold #00ffff',  
})

    while True:
        try:
            console.print("\n[bold magenta]❯❯ USER INPUT[/bold magenta] [dim](Alt+Enter untuk kirim)[/dim]")
            
            # Menggunakan prompt_toolkit dengan prefix simbol yang keren
            user_input = prompt(" ──> ", multiline=True, style=style_prompt)
            
            # Validasi jika input kosong
            if not user_input.strip():
                continue
                
            # Fitur keluar dari aplikasi
            if user_input.strip().lower() in ['exit', 'quit', 'keluar']:
                console.print("\n[bold red]──> Mematikan Hanum Agent. Sampai jumpa, Bro![/bold red]\n")
                break

            # 2. PROSES LOKAL ROUTER (Dengan tampilan log berwarna)
            console.print("\n[bold dim white]─── [ Processing Route ] ───[/bold dim white]")
            bidang = tentukan_agen_dan_bidang(user_input)
            
            console.print(f"[*] Jalur Agen Terkunci: [bold yellow][{bidang.upper()}][/bold yellow]")

            # 3. PROSES CLOUD GENERATION (Menggunakan Spinner Animasi)
            # Mengunci terminal dalam kondisi loading yang interaktif
            with console.status("[bold cyan]Hanum sedang merenung dan menganalisis cloud...", spinner="bouncingBar") as status:
                
                # Memanggil model cloud kita kemarin
                llm = ambil_model_chat(temperature=0.6)

                system_instruction_hanum = (
                    "Kamu adalah Hanum Agentic AI, sebuah AI Agent cerdas, mandiri, dan "
                    "bertenaga tinggi yang dibangun dan dikembangkan oleh Azhar Aufa.\n\n"
                )
                
                # Satukan instruksi sistem dengan input dari user
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", system_instruction_hanum),
                    ("user", "{input}")
                ])
                
                # Bangun rantai eksekusi (Chain)
                chain = prompt_template | llm
                
                # Eksekusi ke Cloud Server
                response = chain.invoke({"input": user_input})
                konten_jawaban = response.content

            # 4. MERENDER JAWABAN (Ubah teks mentah ke Markdown Berwarna)
            console.print("\n[bold bright_green]❯❯ HANUM RESPONSE[/bold bright_green]")
            console.print("────────────────────────────────────────────────", style="dim white")
            
            # Rich otomatis mewarnai codeblocks (cat, ssh, bash) di dalam markdown ini
            console.print(Markdown(konten_jawaban))
            
            console.print("────────────────────────────────────────────────", style="dim white")

        except KeyboardInterrupt:
            # Mengamankan jika user tidak sengaja menekan Ctrl+C agar tidak crash berantakan
            console.print("\n\n[bold red][!] Sinyal interupsi dideteksi. Keluar...[/bold red]\n")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[bold red][ERROR SYSTEM]: {e}[/bold red]")

if __name__ == "__main__":
    main()