import streamlit as st
import pandas as pd

# Judul Dashboard
st.set_page_config(page_title="Database Guru Terpadu Sumut", layout="wide")
st.title("🏛️ Sistem Informasi Guru Terpadu")
st.subheader("Dinas Pendidikan Provinsi Sumatera Utara")

# Ambil data dari Secrets
try:
    SHEET_URL = st.secrets["gsheets_url"]
    # Link otomatis untuk ekspor ke CSV
    csv_url = SHEET_URL.replace("/edit?usp=sharing", "/export?format=csv")
    
    df = pd.read_csv(csv_url)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟦 DATA GURU PNS", use_container_width=True):
            st.success("Menampilkan Data Guru PNS")
            st.dataframe(df) # Menampilkan tabel data
    with col2:
        st.button("🟧 PPPK PENUH WAKTU", use_container_width=True)
    with col3:
        st.button("🟩 PPPK PARUH WAKTU", use_container_width=True)

except Exception as e:
    st.error("Data belum terhubung. Silakan isi gsheets_url di Advanced Settings (Secrets).")
