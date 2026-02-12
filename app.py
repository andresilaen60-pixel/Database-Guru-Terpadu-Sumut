import streamlit as st
import pandas as pd

st.set_page_config(page_title="Database Guru Terpadu Sumut", layout="wide")
st.title("🏛️ Sistem Informasi Guru Terpadu")
st.subheader("Dinas Pendidikan Provinsi Sumatera Utara")

try:
    raw_url = st.secrets["gsheets_url"]
    
    # Fungsi ambil data berdasarkan nama tab
    def get_data(sheet_name):
        # Menghapus bagian /edit dan menggantinya dengan export csv
        base_url = raw_url.split('/edit')[0]
        url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟦 DATA GURU PNS", use_container_width=True):
            df = get_data("Data_PNS")
            st.success("Menampilkan Data PNS")
            st.dataframe(df, use_container_width=True)

    with col2:
        if st.button("🟧 PPPK PENUH WAKTU", use_container_width=True):
            df = get_data("Data_PPPK_Penuh")
            st.warning("Menampilkan Data PPPK Penuh Waktu")
            st.dataframe(df, use_container_width=True)

    with col3:
        if st.button("🟩 PPPK PARUH WAKTU", use_container_width=True):
            df = get_data("Data_PPPK_Paruh")
            st.info("Menampilkan Data PPPK Paruh Waktu")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}. Pastikan link di Secrets sudah benar.")
