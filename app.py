import streamlit as st
import pandas as pd

st.set_page_config(page_title="Database Guru Terpadu Sumut", layout="wide")
st.title("🏛️ Sistem Informasi Guru Terpadu")
st.subheader("Dinas Pendidikan Provinsi Sumatera Utara")

try:
    # Mengambil URL utama dari Secrets
    raw_url = st.secrets["gsheets_url"]
    
    # Fungsi untuk mengambil data berdasarkan nama Sheet
    # Kita gunakan parameter 'sheet_name' agar lebih mudah daripada GID
    def get_data(sheet_name):
        url = raw_url.replace("/edit?usp=sharing", f"/export?format=csv&sheet={sheet_name}")
        return pd.read_csv(url)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    # 1. Tombol Data PNS
    with col1:
        if st.button("🟦 DATA GURU PNS", use_container_width=True):
            df_pns = get_data("Data_PNS")
            st.success(f"Menampilkan Data dari Sheet: Data_PNS")
            st.dataframe(df_pns, use_container_width=True)

    # 2. Tombol Data PPPK Penuh
    with col2:
        if st.button("🟧 PPPK PENUH WAKTU", use_container_width=True):
            df_full = get_data("Data_PPPK_Penuh")
            st.warning("Menampilkan Data dari Sheet: Data_PPPK_Penuh")
            st.dataframe(df_full, use_container_width=True)

    # 3. Tombol Data PPPK Paruh
    with col3:
        if st.button("🟩 PPPK PARUH WAKTU", use_container_width=True):
            df_part = get_data("Data_PPPK_Paruh")
            st.info("Menampilkan Data dari Sheet: Data_PPPK_Paruh")
            st.dataframe(df_part, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
    st.info("Pastikan nama tab di Google Sheets sesuai (Data_PNS, Data_PPPK_Penuh, Data_PPPK_Paruh)")
