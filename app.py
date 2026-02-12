import streamlit as st
import pandas as pd
st.set_page_config(page_title="SIMPEG Sumut", layout="wide")
def get_data(sheet_name):
    try:
                raw_url = st.secrets["gsheets_url"]
                base_url = raw_url.split('/edit')[0]
                url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
                return pd.read_csv(url)
    except: return None
if 'logged_in' not in st.session_state:
                        st.session_state.logged_in = False
if 'view' not in st.session_state:
                                st.session_state.view = 'menu'
if 'selected_guru' not in st.session_state:
                                    st.session_state.selected_guru = None
if not st.session_state.logged_in:
                                        st.markdown("## 🔐 Login SIMPEG")
                                        u = st.text_input("Username")
                                        p = st.text_input("Password", type="password")
if st.button("Masuk", use_container_width=True):
                                                    df_u = get_data("Users")
if df_u is not None:
                                                                check = df_u[(df_u['username'] == u) & (df_u['password'].astype(str) == p)]
                                                                if not check.empty:
                                                                    st.session_state.logged_in = True
                                                                    st.session_state.role = check.iloc[0]['role']
                                                                    st.session_state.wilayah = check.iloc[0]['wilayah']
                                                                    st.rerun()
                                                                else: st.error("Akses Ditolak!")
                                                                                        st.stop()
                                                        st.title("🏛️ SIMPEG Terpadu Sumut")
st.sidebar.success(f"Role: {st.session_state.role}")
if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.rerun()
st.markdown("---")
if st.session_state.view == 'menu':
        c1, c2, c3 = st.columns(3)
if c1.button("🟦 DATA GURU PNS", use_container_width=True):
                st.session_state.category = "Data_PNS"
        st.session_state.view = 'cabdis'
        st.rerun()
if c2.button("🟧 PPPK PENUH WAKTU", use_container_width=True):
                st.session_state.category = "Data_PPPK_Penuh"
        st.session_state.view = 'cabdis'
        st.rerun()
if c3.button("🟩 PPPK PARUH WAKTU", use_container_width=True):
                st.session_state.category = "Data_PPPK_Paruh"
        st.session_state.view = 'cabdis'
        st.rerun()
elif st.session_state.view == 'cabdis':
if st.button("⬅️ Kembali ke Menu Utama"):
                st.session_state.view = 'menu'
        st.rerun()
    st.subheader(f"📍 Pilih Wilayah ({st.session_state.category})")
    list_cabdis = [f"Cabdis Wilayah {i}" for i in range(1, 15)]
if st.session_state.role == "Admin Cabdis":
                list_cabdis = [st.session_state.wilayah]
    grid = st.columns(4)
    for idx, cab in enumerate(list_cabdis):
if grid[idx % 4].button(cab, use_container_width=True):
                                st.session_state.cab_selected = cab
            st.session_state.view = 'list'
            st.rerun()
elif st.session_state.view == 'list':
if st.button("⬅️ Kembali ke Pilih Cabdis"):
                st.session_state.view = 'cabdis'
        st.rerun()
    st.subheader(f"📋 Daftar Guru - {st.session_state.cab_selected}")
    df = get_data(st.session_state.category)
if df is not None:
                df_f = df[df['Cabdis'] == st.session_state.cab_selected]
        for i, row in df_f.iterrows():
                        label = f"👤 {row['Nama']} | NIP: {row['NIP']} | NIK: {row['NIK']}"
if st.button(label, key=f"btn_{i}", use_container_width=True):
                                st.session_state.selected_guru = row
                st.session_state.view = 'profile'
                st.rerun()
elif st.session_state.view == 'profile':
    g = st.session_state.selected_guru
if st.button("⬅️ Kembali ke Daftar"):
                st.session_state.view = 'list'
        st.rerun()
    st.success(f"📊 PROFIL LENGKAP: {g['Nama']}")
    t1, t2, t3, t4, t5, t6, t7 = st.tabs(["👤 Pribadi", "🏢 Kerja", "🎓 Edukasi", "📜 Sertifikat", "📖 Mapel", "🚀 Karir", "📂 Dokumen"])
    with t1: st.write(f"TTL: {g['Tempat_Lahir']}, {g['Tanggal_Lahir']}\n\nAlamat: {g['Alamat']}")
            with t2: st.write(f"Jabatan: {g['Jabatan']}\n\nUnit: {g['Unit_Kerja']}\n\nGol: {g['Golongan']}")
                    with t3: st.write(f"Pendidikan: {g['Pendidikan_Terakhir']} - {g['Jurusan']}\n\nKampus: {g['Kampus']}")
                            with t7:
if pd.notna(g['Link_Ijazah']): st.markdown(f"")
if pd.notna(g['Link_SK_Pangkat']): st.markdown(f"")
