# 🎬 Sistem Peminjaman Alat Studio

Aplikasi manajemen dan pencarian peminjaman alat studio berbasis web yang dibangun menggunakan **Python (Streamlit)** dan terintegrasi secara *real-time* dengan **Google Sheets** sebagai basis data cloud.

---

## 🚀 Fitur Utama

- **🔐 Sistem Login Admin & Otentikasi Sederhana:** Mengamankan halaman dashboard utama dari akses tanpa izin.
- **📝 Form Peminjaman Alat:** Memudahkan input data peminjam, nomor kontak, pemberi pinjaman, nama alat, jumlah, hingga estimasi tanggal pengembalian.
- **📊 Tabel Data Interaktif & Dropdown Editor:** Mengubah status pengembalian (`Belum Dikembalikan` / `Sudah Dikembalikan`) dan kondisi alat (`Lengkap`, `Rusak`, `Tidak Lengkap`, `Hilang`) langsung melalui pilihan dropdown pada tabel.
- **🔍 Pencarian Real-Time:** Filter pencarian cepat berdasarkan nama alat studio maupun nama peminjam.
- **☁️ Integrasi Google Sheets Cloud:** Data tersimpan otomatis dan tersinkronisasi secara dua arah (membaca & memperbarui) menggunakan Google Sheets API.
- **📥 Ekspor Data CSV:** Dukungan *download* cadangan data peminjaman dalam format CSV kapan saja.

---

## 📂 Struktur File

```text
peminjaman-studio/
├── app.py                # Kode utama aplikasi Streamlit
├── creds.json.example    # Template/contoh format kredensial Google Service Account
├── README.md             # Dokumentasi dan panduan penggunaan
└── requirements.txt      # Daftar dependensi library Python
```

---

## ⚙️ Bagaimana Cara Aplikasi Ini Bekerja?

Aplikasi bekerja dengan alur integrasi antara **Streamlit (Frontend & App Logic)**, **gspread / OAuth2 (API Protocol)**, dan **Google Sheets (Backend Database)**:

```
[ Form Input / Editor (Streamlit) ]
                 │
                 ▼
[ Google Service Account (creds.json) ] ── (Autentikasi OAuth2)
                 │
                 ▼
[ Google Sheets API (via gspread) ]
                 │
                 ▼
[ Google Sheets Database (Spreadsheet Cloud) ]
```

1. **Autentikasi Sesi:** Pengguna melakukan login di halaman awal. Setelah login berhasil, status disimpan ke dalam `st.session_state`.
2. **Koneksi Service Account:** Aplikasi membaca kunci rahasia dari `creds.json` untuk mengotorisasi akses ke Google Drive & Sheets API.
3. **Pembacaan Data (`load_data_from_sheets`):** Aplikasi mengambil seluruh baris data dari Google Sheets dan mengonversinya menjadi `pandas.DataFrame` untuk ditampilkan secara rapi di Streamlit.
4. **Penambahan Data (`append_data_to_sheets`):** Saat form peminjaman dikirim, baris baru ditambahkan langsung (*append*) di bagian bawah spreadsheet Google.
5. **Pembaruan Massal (`save_all_to_sheets`):** Saat pengguna mengubah status/kondisi alat di tabel `st.data_editor`, seluruh data yang telah diperbarui akan ditulis ulang ke spreadsheet secara aman.

---

## 🔑 Cara Mendapatkan Kredensial Google (Private Key & Sheet ID)

Untuk menghubungkan aplikasi ini ke Google Sheets milik Anda sendiri, ikuti langkah-langkah berikut:

### Langkah 1: Buat Google Cloud Project & Service Account

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat proyek baru (*Create Project*) atau pilih proyek yang sudah ada.
3. Di bilah pencarian atas, cari dan aktifkan **Google Sheets API** dan **Google Drive API**.
4. Buka menu **IAM & Admin** > **Service Accounts** > klik **Create Service Account**.
5. Isi nama service account (misal: `studio-app`), lalu klik **Create and Continue**.
6. Klik **Done** (peran/role opsional).

### Langkah 2: Unduh File `creds.json`

1. Klik pada Service Account yang baru dibuat.
2. Buka tab **Keys** > klik **Add Key** > **Create new key**.
3. Pilih format **JSON**, lalu klik **Create**. File JSON akan otomatis terunduh ke komputer Anda.
4. Ubah nama file JSON yang diunduh tersebut menjadi **`creds.json`** dan letakkan di dalam folder proyek Anda.
5. Catat alamat email yang ada pada kolom `client_email` di dalam file JSON tersebut (contoh: `studio-app@your-project.iam.gserviceaccount.com`).

### Langkah 3: Menyiapkan Google Sheets

1. Buat spreadsheet baru di [Google Sheets](https://sheets.google.com/).
2. Berikan akses edit ke Service Account dengan cara:
   - Klik tombol **Share (Bagikan)** di kanan atas Google Sheets.
   - Masukkan alamat email Service Account (`client_email` dari Langkah 2).
   - Pastikan perannya adalah **Editor**, lalu klik **Send**.
3. Salin **Sheet ID** dari URL browser Anda.
   - URL Google Sheets: `https://docs.google.com/spreadsheets/d/****`
   - Sheet ID adalah kode acak di antara `/d/` dan `/edit`: `1iJ****`

---

## 🛠️ Panduan Instalasi & Menjalankan Aplikasi

### 1. Prasyarat
Pastikan Python versi 3.8 atau yang lebih baru sudah terpasang di komputer Anda.

### 2. Instal Dependensi
Buka Terminal / Command Prompt pada direktori proyek, lalu jalankan:

```
pip install streamlit pandas gspread oauth2client
```

*(Atau jika ada `requirements.txt`: `pip install -r requirements.txt`)*

### 3. Konfigurasi Kode `app.py`
Buka file `app.py`, lalu sesuaikan variabel berikut:

```python
# Kredensial Login Admin
USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = "admin123"

# Masukkan Sheet ID Anda dari Langkah 3
SHEET_ID = "MASUKKAN_SHEET_ID_ANDA_DI_SINI"
```

### 4. Jalankan Aplikasi

```
streamlit run app.py
```

Aplikasi akan otomatis berjalan di peramban web Anda (default: `http://localhost:8501`).

---

## 📄 Lisensi & Kontribusi

Proyek ini dibuat open-source dan bebas untuk dimodifikasi maupun dibagikan secara gratis.
