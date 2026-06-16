# Write-up OverTheWire: Bandit Level 0 to Level 1

## Tujuan
Mendapatkan SSH password untuk level berikutnya dengan membaca file 'readme' di home direktori.

## Langkah Penyelesaian
1. Konek ke server menggunakan SSH dengan perintah:
   ssh bandit0@bandit.labs.overthewire.org -p 2220
2. Gunakan password: `bandit0`
3. Setelah berhasil masuk, cek isi folder menggunakan perintah `ls`.
4. Buka file readme dengan perintah: `cat readme`
5. Password untuk level 1 berhasil didapatkan.
