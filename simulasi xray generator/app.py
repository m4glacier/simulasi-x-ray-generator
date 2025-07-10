import streamlit as st
import requests
import streamlit.components.v1 as components
import os

# BACKEND = "http://localhost:8000"  # HANYA untuk SSE, sekarang TIDAK dipakai

# Konfigurasi halaman
st.set_page_config(
    page_title="Panel Kontrol Simulasi Pesawat Roentgen",
    layout="wide",
)

st.title("Panel Kontrol Simulasi Pesawat Roentgen")

# Inisialisasi session state
if "kv" not in st.session_state: st.session_state.kv = 0
if "ma" not in st.session_state: st.session_state.ma = 0
if "sec" not in st.session_state: st.session_state.sec = 1
if "sent_payload" not in st.session_state: st.session_state.sent_payload = {}

# === Bagian Atas: Kontrol Parameter ===
st.subheader("Parameter Kontrol")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Tegangan (kV)**")
    st.markdown(f"<div style='font-size:40px; font-weight:bold;'>{st.session_state.kv} kV</div>", unsafe_allow_html=True)
    if st.button("🔼", key="kv_up"): st.session_state.kv += 1
    if st.button("🔽", key="kv_down"): st.session_state.kv -= 1

with col2:
    st.markdown("**Arus (mA)**")
    st.markdown(f"<div style='font-size:40px; font-weight:bold;'>{st.session_state.ma} mA</div>", unsafe_allow_html=True)
    if st.button("🔼", key="ma_up"): st.session_state.ma += 1
    if st.button("🔽", key="ma_down"): st.session_state.ma -= 1

with col3:
    st.markdown("**Waktu (detik)**")
    st.markdown(f"<div style='font-size:40px; font-weight:bold;'>{st.session_state.sec} detik</div>", unsafe_allow_html=True)
    if st.button("🔼", key="sec_up"): st.session_state.sec += 1
    if st.button("🔽", key="sec_down"): st.session_state.sec = max(1, st.session_state.sec - 1)

# Tombol reset
if st.button("🔄 RESET"):
    st.session_state.kv = 0
    st.session_state.ma = 0
    st.session_state.sec = 1

# Status
st.subheader("Kontrol Paparan")
kode = st.radio("Status", ["OFF", "PRE", "ON"], horizontal=True)

# Tampilkan nilai parameter
st.markdown("---")
st.markdown(f"""
**Tegangan:** {st.session_state.kv} kV  
**Arus:** {st.session_state.ma} mA  
**Waktu:** {st.session_state.sec} detik  
**Status:** {kode}
""")

# === Bagian Bawah: Simulasi ===
st.subheader("Simulasi Pesawat Roentgen")

try:
    html_path = os.path.join("web", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

        # Sisipkan nilai-nilai parameter ke dalam HTML
        html_content = html_content.replace("{{kv}}", str(st.session_state.kv))
        html_content = html_content.replace("{{ma}}", str(st.session_state.ma))
        html_content = html_content.replace("{{sec}}", str(st.session_state.sec))
        html_content = html_content.replace("{{kode}}", kode.lower())

        components.html(html_content, height=800, scrolling=True)

except FileNotFoundError:
    st.error("⚠️ File `web/index.html` tidak ditemukan.")
