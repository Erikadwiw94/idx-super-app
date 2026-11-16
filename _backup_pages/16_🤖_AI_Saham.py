import streamlit as st
import subprocess
import os

st.set_page_config(page_title="AI Saham", page_icon="🤖", layout="wide")
st.title("🤖 AI Saham (CLI Cockpit)")
st.write("Antarmuka web untuk menjalankan *engine* dari proyek `ai-saham`.")
st.divider()

SAHAM_DIR = "/home/server/ai-saham"
SAHAM_BIN = f"{SAHAM_DIR}/.venv/bin/saham"

def run_cmd(args, stdin_text=None):
    try:
        r = subprocess.run([SAHAM_BIN] + args, cwd=SAHAM_DIR, capture_output=True, text=True,
                          timeout=300, input=stdin_text)
        out = r.stdout
        if r.stderr: out += f"\n\n--- STDERR ---\n{r.stderr}"
        return out
    except Exception as e:
        return f"❌ {e}"

col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
with col1:
    universe = st.selectbox("Universe:", ["lq45", "idx80", "kompas100", "all"])
with col2:
    aksi = st.selectbox("Perintah:", ["today", "fetch market", "screen accum", "plan swing"])
with col3:
    ticker = st.text_input("Ticker (untuk plan swing):", value="BBRI").upper()
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan", type="primary", use_container_width=True)

st.divider()

if mulai:
    if aksi == "fetch market": cmd = ["fetch", "market", "--universe", universe]
    elif aksi == "screen accum": cmd = ["screen", "accum", "--universe", universe, "--multi"]
    elif aksi == "plan swing": cmd = ["plan", "swing", ticker, "--capital", "10000000"]
    else: cmd = ["today"]
    
    with st.spinner(f"Menjalankan `{aksi}`..."):
        out = run_cmd(cmd)
        st.code(out, language="text")
