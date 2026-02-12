import streamlit as st
import pandas as pd

st.set_page_config(page_title="Database Guru Terpadu Sumut", layout="wide")
st.title("🏛️ Sistem Informasi Guru Terpadu")
st.subheader("Dinas Pendidikan Provinsi Sumatera Utara")

try:
    raw_url = st.secrets["gsheets_url"]
    
    def get_data(sheet_name):
        base_url = raw_url.split('/edit')[0]
        url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)

    # --- SIDEBAR FILTER (DUA KOTAK TERPISAH) ---
    st.sidebar.header("🔍 Filter Data")
    filter_nama = st.sidebar.text_input("Cari Berdasarkan Nama:")
    filter_nip = st.sidebar.text_input("Cari Berdasarkan NIP:")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    if 'current_df' not in st.session_state:
        st.session_state.current_df = None
        st.session_state.sheet_active = ""

    # Tombol Menu
    if col1.button("🟦 DATA GURU PNS", use_container_width=True):
        st.session_state.current_df = get_data("Data_PNS")
        st.session_state.sheet_active = "PNS"
    if col2.button("🟧 PPPK PENUH WAKTU", use_container_width=True):
        st.session_state.current_df = get_data("Data_PPPK_Penuh")
        st.session_state.sheet_active = "PPPK Penuh Waktu"
    if col3.button("🟩 PPPK PARUH WAKTU", use_container_width=True):
        st.session_state.current_df = get_data("Data_PPPK_Paruh")
        st.session_state.sheet_active = "PPPK Paruh Waktu"

    # Logika Tampilan Data
    if st.session_state.current_df is not None:
        df_display = st.session_state.current_df.copy()
        
        # Deteksi Nama Kolom
        col_nama = 'Nama' if 'Nama' in df_display.columns else 'Nama Lengkap'
        col_nip = 'NIP' if 'NIP' in df_display.columns else 'ID'

        # Filter 1: Berdasarkan Nama
        if filter_nama and col_nama in df_display.columns:
            df_display = df_display[df_display[col_nama].astype(str).str.contains(filter_nama, case=False, na=False)]
            
        # Filter 2: Berdasarkan NIP
        if filter_nip and col_nip in df_display.columns:
            df_display = df_display[df_display[col_nip].astype(str).str.contains(filter_nip, case=False, na=False)]

        st.write(f"### Menampilkan: {st.session_state.sheet_active}")
        st.write(f"Total Temuan: {len(df_display)} orang")
        # Menampilkan semua kolom asli dari Google Sheets
        st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kendala: {e}")
