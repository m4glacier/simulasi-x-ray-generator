# app.py
import streamlit as st
import requests, json

BACKEND = "http://localhost:8000"

# Konfigurasi halaman
st.set_page_config(
    page_title="Panel Kontrol Simulasi Pesawat Roentgen",
    layout="wide",
)

st.title("Panel Kontrol Simulasi Pesawat Roentgen")

# Inisialisasi session state
if "kv" not in st.session_state: st.session_state.kv = 00
if "ma" not in st.session_state: st.session_state.ma = 00
if "sec" not in st.session_state: st.session_state.sec = 0
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
    st.session_state.kv = 00
    st.session_state.ma = 00
    st.session_state.sec = 0

# Status
st.subheader("Kontrol Paparan")
kode = st.radio("Status", ["OFF", "PRE", "ON"], horizontal=True)

# Payload dikirim ke backend
payload = {
    "kv": st.session_state.kv,
    "mA": st.session_state.ma,
    "Sec": st.session_state.sec,
    "kode": "e" if kode == "ON" else "p" if kode == "PRE" else "x"
}

if payload != st.session_state.sent_payload:
    try:
        requests.post(f"{BACKEND}/update", json=payload, timeout=0.2)
        st.session_state.sent_payload = payload
    except requests.exceptions.RequestException:
        st.warning("⚠️ Flask server belum aktif di port 8000")

# Info nilai parameter
st.markdown("---")
st.markdown(f"""
**Tegangan:** {st.session_state.kv} kV  
**Arus:** {st.session_state.ma} mA  
**Waktu:** {st.session_state.sec} detik  
**Status:** {kode}
""")

# === Bagian Bawah: Simulasi ===
st.subheader("Simulasi Pesawat Roentgen")
st.markdown(f"""
<iframe src="{BACKEND}/web/index.html"
        width="100%" height="800" frameborder="0"
        style="background:#000;"></iframe>
""", unsafe_allow_html=True)
