import streamlit as st
import subprocess
import os

st.title("🧠 StockAI (AI Trading Toolkit)")
st.write("Antarmuka web untuk menjalankan *engine* dari proyek `stockai`.")
st.divider()

STOCKAI_DIR = "/home/server/stockai"
STOCKAI_BIN = f"{STOCKAI_DIR}/venv/bin/stockai"

def run_stockai(args):
    try:
        r = subprocess.run([STOCKAI_BIN] + args, cwd=STOCKAI_DIR, capture_output=True, text=True, timeout=300)
        out = r.stdout
        if r.stderr: out += f"\n\n--- STDERR ---\n{r.stderr}"
        return out
    except subprocess.TimeoutExpired:
        return "❌ Timeout!"
    except Exception as e:
        return f"❌ Error: {e}"

col1, col2, col3 = st.columns([2, 3, 1.5])
with col1:
    ticker = st.text_input("Kode Saham:", value="BBCA").upper()
with col2:
    aksi = st.selectbox("Perintah CLI:", ["morning", "evening", "analyze", "paper status"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan", type="primary", use_container_width=True)

st.divider()

if mulai:
    cmd = aksi.split()
    if "analyze" in cmd: cmd = ["analyze", ticker]
    
    with st.spinner(f"Menjalankan `stockai {' '.join(cmd)}`..."):
        out = run_stockai(cmd)
        st.code(out, language="text")
