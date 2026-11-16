import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Pulse CLI", page_icon="🚀", layout="wide")
st.title("🚀 Pulse CLI (AI & ML)")
st.write("Antarmuka web untuk `Pulse-CLI` — AI + Machine Learning Trading.")
st.divider()

PULSE_DIR = "/home/server/Pulse-CLI"
PULSE_BIN = f"{PULSE_DIR}/venv/bin/pulse"

def run_pulse(args):
    try:
        r = subprocess.run([PULSE_BIN] + args, cwd=PULSE_DIR, capture_output=True, text=True, timeout=300)
        out = r.stdout
        if r.stderr: out += f"\n\n--- STDERR ---\n{r.stderr}"
        return out
    except Exception as e:
        return f"❌ {e}"

col1, col2, col3 = st.columns([2, 3, 1.5])
with col1: ticker = st.text_input("Kode Saham:", value="BBCA").upper()
with col2: aksi = st.selectbox("Perintah:", ["analyze", "screen", "sapta", "plan", "broker"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan", type="primary", use_container_width=True)

st.divider()

if mulai:
    cmd = [aksi, ticker] if aksi in ["analyze", "sapta", "plan", "broker"] else [aksi]
    with st.spinner(f"Menjalankan `pulse {' '.join(cmd)}`..."):
        out = run_pulse(cmd)
        st.code(out, language="text")
