Hanum Agentic AI (Prototype)

Proyek eksperimen mandiri untuk membangun Agen AI otonom yang cerdas, memiliki memori, dan mampu berinteraksi secara dinamis. Proyek ini dibangun dari nol menggunakan ekosistem modern **LangChain** dan **LangGraph**, dengan otak utama menggunakan model **Gemma 4 (31B) Cloud**.

> **Status Proyek:** *Work in Progress (WIP)* / Tahap Belajar & Eksplorasi. Repositori ini digunakan sebagai jurnal eksperimen arsitektur AI, manajemen memori, dan eksplorasi *Agentic Workflow*.

---

## Fitur Utama & Eksperimen yang Berjalan

### 1. Otak Kognitif (Gemma 4 Cloud via LangChain)
* Mengintegrasikan model **Gemma 4:31b-cloud** sebagai mesin penggerak logika utama.

### 2. Dual-Layer Persistence (Memori LangGraph)
Proyek ini mengimplementasikan konsep memori canggih sesuai standar dokumentasi LangGraph:
* **Short-Term Memory (Checkpointer):** Menggunakan `InMemorySaver` untuk melacak status percakapan dalam satu *thread* (sesi chat). AI mampu mengingat konteks obrolan sebelumnya dalam sesi yang sama.
* **Long-Term Memory (Store):** Menggunakan `InMemoryStore` untuk menyimpan preferensi user (seperti hobi, kopi kesukaan, dll.) secara permanen yang bisa diakses lintas *thread* (sesi baru).

### 3. Eksperimen Masa Depan (Roadmap)
Proyek ini dirancang untuk tidak sekadar menjadi chatbot biasa, melainkan berevolusi menjadi ekosistem **Multi-Agent yang mandiri (Self-Learning & Self-Improving)**. Berikut adalah cetak biru teknis pengembangannya:

#### 📬 FASE 1: Otomatisasi Memori & Kognitif Mandiri (Self-Learning)
* [ ] **Automated Reflection Node:** Mengimplementasikan node evaluasi otomatis di akhir percakapan. Gemma 4 akan menganalisis transkrip obrolan secara mandiri, mengekstrak fakta penting/koreksi dari user, lalu mengeksekusi `store.put()` tanpa campur tangan kode manual.
* [ ] **Memory Pruning & Consolidation:** Membuat sistem yang bisa menyaring memori jangka panjang. Agen dapat menghapus informasi yang sudah tidak valid (misal: user mengubah preferensi kopinya) atau menggabungkan fakta-fakta kecil menjadi satu profil utuh agar menghemat penyimpanan.
* [ ] **Semantic Memory Search:** Mengintegrasikan model *Embedding* pada `InMemoryStore`/`PostgresStore` agar Hanum bisa mencari memori jangka panjang bukan cuma berdasarkan kata kunci (*keyword matching*), melainkan berdasarkan kedekatan makna/konteks (*semantic search*).

#### 🧰 FASE 2: Memperluas Gudang Senjata (Agentic Tools Integration)
* [ ] **Cybersecurity & OSINT Suite:** Membekali agen dengan fungsi (Tools) Python khusus untuk melakukan otomatisasi tugas teknis seperti *vulnerability scanning*, integrasi API *Sherlock/Shodan*, dan analisis header HTTP secara aman di lokal.
* [ ] **HRD Toolkit & Psychometrics Parser:** Membuat *tools* khusus untuk mendukung sub-agen Psikologi Industri, seperti:
  * *Resume/CV Parser* (menggunakan library Python seperti PyPDF2/Docx) untuk mengekstrak data kandidat secara otomatis.
  * *Sentiment & Text Analytics Dashboard* untuk memetakan emosi dan tingkat stres karyawan berdasarkan survei internal atau kuesioner skala psikologi (seperti Skala Likert).
  * *Job-Desc Matcher* menggunakan kalkulasi kesamaan teks (Cosine Similarity) untuk mencocokkan kualifikasi kandidat dengan standar kebutuhan perusahaan.
* [ ] **Local Database Integration:** Migrasi dari penyimpanan ram (*In-Memory*) ke database persisten tangguh untuk kebutuhan produksi menggunakan `PostgresSaver` (Short-term) dan `PostgresStore` (Long-term).

#### 🤖 FASE 3: Arsitektur Multi-Agent (Banyak Agen, Satu Ekosistem)
Hanum akan dipecah menjadi beberapa sub-agen spesialis yang dikendalikan oleh satu Agen Utama (**Supervisor/Orchestrator**):
* [ ] **Hanum Orchestrator (The Boss):** Agen utama yang bertugas menerima perintah user, membedah intensi, dan mendelegasikan tugas ke sub-agen yang tepat via *Conditional Edges* di LangGraph.
* [ ] **SecOps Agent (The Pentester):** Sub-agen khusus yang hanya fokus pada instruksi keamanan siber, analisis kode, dan riset kerentanan.
* [ ] **Hanum HRD & Psychometrics Agent (The Evaluator):** Sub-agen spesialis bidang Psikologi Industri dan Organisasi (PIO). Bertugas menyusun indikator penilaian performa karyawan (KPI/OKRs), melakukan analisis sentimen budaya kerja dari survei karyawan, membuat skenario *interview* berbasis kompetensi (BEI), hingga melakukan screening awal CV (*Resume Parsing*) berdasarkan kecocokan psikologis jabatan.

#### 🔄 FASE 4: Evaluasi Mandiri & Penguatan (Self-Improving)
* [ ] **Self-Correction Loops:** Jika sub-agen menghasilkan output yang *error* atau tidak sesuai format, agen akan menangkap pesan error tersebut, membacanya kembali, memperbaiki kodenya sendiri, dan mengeksekusi ulang (*Auto-debugging loop*).
* [ ] **LangSmith Golden Dataset Evaluation:** Menyusun kumpulan studi kasus (Dataset) di LangSmith untuk menguji performa logika seluruh jaringan agen secara otomatis setiap kali ada pembaruan arsitektur.

---
