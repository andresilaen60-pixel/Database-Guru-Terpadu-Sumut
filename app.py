import streamlit as st
import pandas as pd

st.set_page_config(page_title="Database Guru Terpadu Sumut", layout="wide")

# Header Utama
st.markdown("<h1 style='text-align: center;'>🏛️ Sistem Informasi Guru Terpadu</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dinas Pendidikan Provinsi Sumatera Utara</h3>", unsafe_allow_html=True)
st.markdown("---")

try:
    raw_url = st.secrets["gsheets_url"]
    
    def get_data(sheet_name):
        base_url = raw_url.split('/edit')[0]
        url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)

    # Inisialisasi state menu
    if 'menu' not in st.session_state:
        st.session_state.menu = "PNS"

    # Barisan Tombol Menu
    col1, col2, col3 = st.columns(3)
    if col1.button("🟦 DATA GURU PNS", use_container_width=True):
        st.session_state.menu = "PNS"
    if col2.button("🟧 PPPK PENUH WAKTU", use_container_width=True):
        st.session_state.menu = "PPPK Penuh Waktu"
    if col3.button("🟩 PPPK PARUH WAKTU", use_container_width=True):
        st.session_state.menu = "PPPK Paruh Waktu"

    st.markdown(f"### 📍 Menu: {st.session_state.menu}")

    # Logika Pengambilan Data Berdasarkan Menu
    sheet_map = {
        "PNS": "Data_PNS",
        "PPPK Penuh Waktu": "Data_PPPK_Penuh",
        "PPPK Paruh Waktu": "Data_PPPK_Paruh"
    }
    
    df_raw = get_data(sheet_map[st.session_state.menu])
    
    # --- BAGIAN FILTER (Tampil di Tengah, Bukan Sidebar) ---
    c1, c2 = st.columns(2)
    with c1:
        f_nama = st.text_input("🔍 Cari Nama Guru:", placeholder="Ketik nama di sini...")
    with c2:
        f_nip = st.text_input("🆔 Cari NIP Guru:", placeholder="Ketik NIP di sini...")

    # Logika Filter
    df_filtered = df_raw.copy()
    col_nama = 'Nama' if 'Nama' in df_filtered.columns else 'Nama Lengkap'
    col_nip = 'NIP' if 'NIP' in df_filtered.columns else 'ID'

    if f_nama:
        df_filtered = df_filtered[df_filtered[col_nama].astype(str).str.contains(f_nama, case=False, na=False)]
    if f_nip:
        df_filtered = df_filtered[df_filtered[col_nip].astype(str).str.contains(f_nip, case=False, na=False)]

    # Tampilan Hasil
    st.info(f"Ditemukan {len(df_filtered)} data dalam kategori {st.session_state.menu}")
    st.dataframe(df_filtered, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kendala: {e}")
