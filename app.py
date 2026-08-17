import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set halaman utama
st.set_page_config(page_title="Peminjaman Alat Studio", layout="wide")

# ==========================================
# 🔐 PENGATURAN LOGIN & GOOGLE SHEETS
# ==========================================
# Ganti kredensial admin sesuai kebutuhan kamu
USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = "admin123"

# Masukkan ID Google Sheets kamu di bawah ini (Ambil dari URL Google Sheets)
# Contoh URL: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit
SHEET_ID = "YOUR_SHEET_ID_HERE"

# Fungsi Koneksi & Ambil Data dari Google Sheets
def load_data_from_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(SHEET_ID).sheet1
        records = sheet.get_all_records()
        df = pd.DataFrame(records)
        
        # Jika sheet masih kosong, buat kolom default
        if df.empty:
            return pd.DataFrame(columns=["Nama Peminjam", "No. Telp", "Pemberi Pinjaman", "Nama Alat", "Jumlah", "Tgl Pinjam", "Tgl Kembali", "Status Pengembalian", "Kondisi Alat"])
        
        # Pengaman & Pengisi nilai default untuk kolom Status Pengembalian
        if "Status Pengembalian" in df.columns:
            df["Status Pengembalian"] = df["Status Pengembalian"].apply(lambda x: "Belum Dikembalikan" if str(x).strip() in ["", "nan", "None"] else x)
        else:
            df["Status Pengembalian"] = "Belum Dikembalikan"
            
        # Pengaman & Pengisi nilai default untuk kolom Kondisi Alat
        if "Kondisi Alat" in df.columns:
            df["Kondisi Alat"] = df["Kondisi Alat"].apply(lambda x: "Lengkap" if str(x).strip() in ["", "nan", "None"] else x)
        else:
            df["Kondisi Alat"] = "Lengkap"
            
        return df
    except Exception as e:
        st.error(f"Gagal terhubung ke Google Sheets: {e}")
        return pd.DataFrame(columns=["Nama Peminjam", "No. Telp", "Pemberi Pinjaman", "Nama Alat", "Jumlah", "Tgl Pinjam", "Tgl Kembali", "Status Pengembalian", "Kondisi Alat"])

# Fungsi untuk Menambah Baris Baru ke Google Sheets
def append_data_to_sheets(new_row_list):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        if len(sheet.get_all_values()) == 0:
            sheet.append_row(["Nama Peminjam", "No. Telp", "Pemberi Pinjaman", "Nama Alat", "Jumlah", "Tgl Pinjam", "Tgl Kembali", "Status Pengembalian", "Kondisi Alat"])
            
        sheet.append_row(new_row_list)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets: {e}")
        return False

# Fungsi untuk Menyimpan Massal Perubahan dari Tabel ke Google Sheets
def save_all_to_sheets(dataframe):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Bersihkan data lama di Sheets (kecuali header) dan tulis ulang data terbaru
        sheet.resize(rows=1)
        
        data_matrix = dataframe.values.tolist()
        for row in data_matrix:
            sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Gagal memperbarui data di Google Sheets: {e}")
        return False

# Load data awal dari cloud ke session state
if 'data_lokal' not in st.session_state:
    st.session_state.data_lokal = load_data_from_sheets()

# -------------------------------------------------------------------
# SISTEM LOGIN
# -------------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.html("<h2 style='text-align: center;'>🎬 Login Sistem Peminjaman Studio</h2>")
    
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        with st.form(key="login_form"):
            username = st.text_input("Username admin")
            password = st.text_input("Password admin", type="password")
            login_button = st.form_submit_button(label="Login")
            
            if login_button:
                if username == USERNAME_ADMIN and password == PASSWORD_ADMIN:
                    st.session_state.logged_in = True
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")
else:
    # -------------------------------------------------------------------
    # TAMPILAN UTAMA APLIKASI (SETELAH LOGIN)
    # -------------------------------------------------------------------
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("🎬 Sistem Peminjaman Alat Studio")
    with col_logout:
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.rerun()

    # Layout kolom
    col1, col2 = st.columns([1, 2])

    # KOLOM 1: FORM INPUT DATA
    with col1:
        st.header("📝 Form Peminjaman")
        with st.form(key="form_pinjam", clear_on_submit=True):
            nama_peminjam = st.text_input("Nama Peminjam")
            no_telp = st.text_input("Nomor Telpon Peminjam")
            pemberi_pinjaman = st.text_input("Nama Pemberi Pinjaman")
            nama_alat = st.text_input("Nama Alat Studio")
            jumlah_alat = st.number_input("Jumlah Alat", min_value=1, step=1)
            
            tgl_pinjam = st.date_input("Tanggal Meminjam", datetime.now())
            tgl_kembali = st.date_input("Tanggal Pengembalian", datetime.now())
            
            submit_button = st.form_submit_button(label="Simpan Data")
            
            if submit_button:
                if nama_peminjam and nama_alat and pemberi_pinjaman:
                    row_to_insert = [
                        nama_peminjam,
                        str(no_telp),
                        pemberi_pinjaman,
                        nama_alat,
                        int(jumlah_alat),
                        tgl_pinjam.strftime('%Y-%m-%d'),
                        tgl_kembali.strftime('%Y-%m-%d'),
                        "Belum Dikembalikan",
                        "Lengkap"
                    ]
                    
                    sukses = append_data_to_sheets(row_to_insert)
                    
                    if sukses:
                        st.success(f"Data {nama_alat} berhasil tersimpan ke Google Sheets!")
                        st.session_state.data_lokal = load_data_from_sheets()
                        st.rerun()
                else:
                    st.error("Mohon isi nama peminjam, nama alat, dan pemberi pinjaman!")

    # KOLOM 2: FITUR SEARCH & TABEL DATA
    with col2:
        st.header("📊 Data Peminjaman & Pencarian")
        
        col_refresh, col_save = st.columns([1, 1])
        with col_refresh:
            if st.button("🔄 Segarkan Data dari Cloud"):
                st.session_state.data_lokal = load_data_from_sheets()
                st.rerun()
        
        search_query = st.text_input("🔍 Cari berdasarkan Nama Alat atau Nama Peminjam:")
        df_tampil = st.session_state.data_lokal
        
        # Logika Filter Pencarian
        if search_query and not df_tampil.empty:
            if 'Nama Alat' in df_tampil.columns and 'Nama Peminjam' in df_tampil.columns:
                df_filtered = df_tampil[
                    df_tampil['Nama Alat'].astype(str).str.contains(search_query, case=False, na=False) | 
                    df_tampil['Nama Peminjam'].astype(str).str.contains(search_query, case=False, na=False)
                ]
            else:
                df_filtered = df_tampil
        else:
            df_filtered = df_tampil
            
        # Menampilkan Data Interaktif
        if not df_filtered.empty:
            st.info("💡 Klik dua kali pada kolom 'Status Pengembalian' atau 'Kondisi Alat' untuk merubah status menggunakan tombol pilihan.")
            
            edited_df = st.data_editor(
                df_filtered,
                use_container_width=True,
                hide_index=True,
                disabled=["Nama Peminjam", "No. Telp", "Pemberi Pinjaman", "Nama Alat", "Jumlah", "Tgl Pinjam", "Tgl Kembali"],
                column_config={
                    "Status Pengembalian": st.column_config.SelectboxColumn(
                        "Status Pengembalian",
                        options=["Belum Dikembalikan", "Sudah Dikembalikan"],
                        required=True,
                    ),
                    "Kondisi Alat": st.column_config.SelectboxColumn(
                        "Kondisi Alat",
                        options=["Lengkap", "Rusak", "Tidak Lengkap", "Hilang"],
                        required=True,
                    )
                }
            )
            
            if not edited_df.equals(df_filtered):
                with col_save:
                    if st.button("💾 Simpan Perubahan", type="primary"):
                        st.session_state.data_lokal = edited_df
                        if save_all_to_sheets(edited_df):
                            st.success("Perubahan berhasil disimpan ke Google Sheets!")
                            st.rerun()
            
            st.write("---")
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Backup CSV", data=csv, file_name="peminjaman.csv", mime="text/csv")
        else:
            st.info("Belum ada data peminjaman atau data tidak ditemukan.")