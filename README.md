# 🛒 Proyek E-commerce Toko XYZ

Proyek ini adalah platform e-commerce sederhana yang dibangun dengan Django. Fitur-fiturnya meliputi etalase produk, keranjang belanja, sistem autentikasi pengguna, dan alur _checkout_.

## ✨ Fitur Utama
* **Etalase Produk**: Menampilkan daftar produk yang tersedia.
* **Keranjang Belanja**: Sistem berbasis sesi untuk menambahkan, menghapus, dan memperbarui kuantitas produk.
* **Autentikasi Pengguna**: Login, registrasi, dan manajemen pengguna.
* **Proses Checkout**: Mengubah keranjang belanja menjadi pesanan yang tersimpan di _database_.
* **Riwayat Belanja**: Halaman khusus untuk pelanggan melihat semua pesanan mereka.
* **Dashboard Admin**: Antarmuka admin yang efisien untuk mengelola produk, pesanan, dan pengguna.

## 🚀 Instalasi dan Menjalankan Proyek

Ikuti langkah-langkah sederhana ini untuk menjalankan proyek di komputer lokal Anda.

### 1. Kloning Repositori

Buka terminal atau Git Bash dan kloning repositori ini ke komputer Anda.

```bash
git clone https://github.com/Hendrasetiawanolybunga/e-commerce-barokah.git
````

Setelah kloning selesai, navigasi ke direktori proyek.

```bash
cd e-commerce-barokah
```

### 2\. Penyiapan Lingkungan Virtual

Sangat disarankan untuk menggunakan lingkungan virtual untuk mengisolasi dependensi proyek.

**Pada Windows:**

```bash
python -m venv env
.\env\Scripts\activate
```

**Pada macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### 3\. Instalasi Dependensi

Semua pustaka yang dibutuhkan tercantum dalam file `requirements.txt`. Instal semuanya dengan satu perintah.

```bash
pip install -r requirements.txt
```

### 4\. Migrasi Basis Data

Proyek ini menggunakan *database* SQLite3. Anda perlu menerapkan migrasi untuk membuat tabel yang diperlukan.

```bash
python manage.py migrate
```

### 5\. Membuat Akun Admin

Untuk mengakses *dashboard* admin dan mengelola data, buat akun superuser.

```bash
python manage.py createsuperuser
```

Ikuti petunjuk di terminal untuk membuat *username* dan *password*.

### 6\. Menjalankan Server

Sekarang, proyek sudah siap dijalankan\!

```bash
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` di peramban Anda untuk melihat etalase produk. Untuk mengakses *dashboard* admin, kunjungi `http://127.0.0.1:8000/admin/` dan masuk menggunakan akun superuser yang sudah Anda buat.

Selamat\! Proyek Anda sudah berjalan. ✨
