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

    # --- SIDEBAR FILTER ---
    st.sidebar.header("🔍 Filter Data")
    search_query = st.sidebar.text_input("Cari Nama atau NIP Guru:")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    if 'current_df' not in st.session_state:
        st.session_state.current_df = None
        st.session_state.sheet_active = ""

    # Tombol Menu Utama
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
        
        # Penyesuaian Nama Kolom Otomatis
        col_nama = 'Nama' if 'Nama' in df_display.columns else ('Nama Lengkap' if 'Nama Lengkap' in df_display.columns else None)
        col_nip = 'NIP' if 'NIP' in df_display.columns else ('ID' if 'ID' in df_display.columns else None)

        # Filter Berdasarkan Pencarian
        if search_query:
            conditions = []
            if col_nama:
                conditions.append(df_display[col_nama].astype(str).str.contains(search_query, case=False, na=False))
            if col_nip:
                conditions.append(df_display[col_nip].astype(str).str.contains(search_query, case=False, na=False))
            
            if conditions:
                df_display = df_display[pd.concat(conditions, axis=1).any(axis=1)]

        # --- HANYA TAMPILKAN NAMA DAN NIP ---
        cols_to_show = [c for c in [col_nip, col_nama] if c is not None]
        
        st.write(f"### Menampilkan: {st.session_state.sheet_active}")
        st.write(f"Total: {len(df_display)} orang")
        
        if cols_to_show:
            st.dataframe(df_display[cols_to_show], use_container_width=True)
        else:
            st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kendala: {e}")
