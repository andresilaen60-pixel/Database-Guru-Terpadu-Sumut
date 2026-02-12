mport streamlit as st import pandas as pd

st.set_page_config(page_title="SIMPEG Terpadu Sumut", layout="wide")

def get_data(sheet_name): try: raw_url = st.secrets["gsheets_url"] base_url = raw_url.split('/edit')[0] url = f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}" return pd.read_csv(url) except: return None

if 'logged_in' not in st.session_state: st.session_state.logged_in = False if 'view' not in st.session_state: st.session_state.view = 'menu' if 'selected_guru' not in st.session_state: st.session_state.selected_guru = None

if not st.session_state.logged_in: st.markdown("<h2 style='text-align: center;'>🔐 Login SIMPEG Terpadu</h2>", unsafe_allow_html=True) _, col_login, _ = st.columns([1, 1.5, 1]) with col_login: u_input = st.text_input("Username") p_input = st.text_input("Password", type="password") if st.button("Masuk", use_container_width=True): df_u = get_data("Users") if df_u is not None: check = df_u[(df_u['username'] == u_input) & (df_u['password'].astype(str) == p_input)] if not check.empty: st.session_state.logged_in = True st.session_state.role = check.iloc[0]['role'] st.session_state.wilayah = check.iloc[0]['wilayah'] st.rerun() else: st.error("Username atau Password salah!") st.stop()

with st.sidebar: st.success(f"👤 {st.session_state.role}") if st.session_state.wilayah != 'Semua': st.info(f"📍 {st.session_state.wilayah}") if st.button("🚪 Log Out", use_container_width=True): st.session_state.logged_in = False st.session_state.view = 'menu' st.rerun()

st.markdown("<h1 style='text-align: center;'>🏛️ Sistem Informasi Guru Terpadu</h1>", unsafe_allow_html=True) st.markdown("<p style='text-align: center;'>Dinas Pendidikan Provinsi Sumatera Utara</p>", unsafe_allow_html=True) st.markdown("---")

if st.session_state.view == 'menu': c1, c2, c3 = st.columns(3) if c1.button("🟦 DATA GURU PNS", use_container_width=True): st.session_state.category = "Data_PNS"; st.session_state.view = 'cabdis'; st.rerun() if c2.button("🟧 PPPK PENUH WAKTU", use_container_width=True): st.session_state.category = "Data_PPPK_Penuh"; st.session_state.view = 'cabdis'; st.rerun() if c3.button("🟩 PPPK PARUH WAKTU", use_container_width=True): st.session_state.category = "Data_PPPK_Paruh"; st.session_state.view = 'cabdis'; st.rerun()

elif st.session_state.view == 'cabdis': if st.button("⬅️ Kembali ke Menu Utama"): st.session_state.view = 'menu'; st.rerun()

elif st.session_state.view == 'list': if st.button("⬅️ Kembali ke Pilih Cabdis"): st.session_state.view = 'cabdis'; st.rerun()

elif st.session_state.view == 'profile': g = st.session_state.selected_guru if st.button("⬅️ Kembali ke Daftar Guru"): st.session_state.view = 'list'; st.rerun()
