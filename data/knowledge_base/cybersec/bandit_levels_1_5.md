# OVERTHEWIRE BANDIT WALKTHROUGH & CONCEPTS

## Bandit Level 1

- **Objective**: Menemukan password untuk Level 2 yang disimpan di dalam file bernama `-` (tanda strip) di home directory.
- **Concept**: Di Linux, file dengan nama `-` sering disalahartikan oleh command sebagai argumen/opsi, bukan nama file. Untuk membacanya, kita harus menentukan path eksplisitnya.
- **Commands**:
  - `cat ./-` (Membaca file di direktori saat ini)
  - `cat < -` (Menggunakan pengalihan input)

## Bandit Level 2

- **Objective**: Menemukan password untuk Level 3 yang disimpan di dalam file bernama `spaces in this filename` di home directory.
- **Concept**: File yang memiliki spasi pada namanya harus dibungkus dengan tanda kutip atau menggunakan karakter escape backslash `\` agar shell tidak menganggapnya sebagai banyak file berbeda.
- **Commands**:
  - `cat "spaces in this filename"`
  - `cat spaces\ in\ this\ filename`

## Bandit Level 3

- **Objective**: Menemukan password untuk Level 4 yang disimpan di dalam file tersembunyi di dalam direktori `inhere`.
- **Concept**: Di Linux, file tersembunyi diawali dengan tanda titik (.). Perintah `ls` biasa tidak akan memunculkannya, harus menggunakan opsi `-a` (all).
- **Commands**:
  - `cd inhere`
  - `ls -a` (Menampilkan semua file termasuk yang hidden)
  - `cat .hidden_file_name`

## Bandit Level 4

- **Objective**: Menemukan password untuk Level 5 di dalam direktori `inhere`, di mana password disimpan di satu-satunya file yang berisi teks yang bisa dibaca manusia (human-readable).
- **Concept**: Gunakan perintah `file` untuk mengecek tipe data sebuah file sebelum membacanya, atau gunakan `strings` untuk mengekstrak teks yang bisa dibaca dari file biner.
- **Commands**:
  - `file *` (Mengecek tipe semua file di folder)
  - Perhatikan file yang bertipe "ASCII text"
  - `cat <nama_file_ascii>`

## Bandit Level 5

- **Objective**: Menemukan password untuk Level 6 di direktori `inhere` dengan kriteria: human-readable, berukuran 1033 bytes, dan tidak bisa dieksekusi (not executable).
- **Concept**: Perintah `find` sangat kuat untuk memfilter file berdasarkan ukuran (`-size`) dan properti lainnya.
- **Commands**:
  - `find . -type f -size 1033c` ('c' berarti bytes)
  - `cat <jalur_file_yang_ditemukan>`
