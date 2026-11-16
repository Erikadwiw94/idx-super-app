import streamlit as st
import subprocess
import os, glob
import pandas as pd
from datetime import datetime, timedelta

st.title("📥 IDX & Stockbit Bulk Downloader")
st.write("Mengunduh data Broker Summary dan Ringkasan Transaksi IDX.")
st.divider()

PROJECT_DIR = "/home/server/Bulk-Download-Table-From-IDX"
VENV_PYTHON = f"{PROJECT_DIR}/venv/bin/python"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "Stock Summary Folder")
yesterday = datetime.now() - timedelta(days=1)

col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
with col1: sumber = st.selectbox("Sumber:", ["IDX Daily Summary", "Stockbit Broker Summary"])
with col2: date_input = st.date_input("Tanggal:", yesterday, max_value=datetime.now())
with col3: ticker = st.text_input("Kode Saham (khusus Stockbit):", value="BBCA").upper()
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("📥 Unduh", type="primary", use_container_width=True)

st.divider()

def run_script(script_name, args):
    try:
        r = subprocess.run([VENV_PYTHON, script_name] + args, cwd=PROJECT_DIR,
            capture_output=True, text=True, timeout=300, input="\n".join(args) + "\n")
        return r.stdout + (f"\n--- STDERR ---\n{r.stderr}" if r.stderr else "")
    except Exception as e:
        return f"❌ {e}"

if mulai:
    with st.spinner(f"Mengunduh {sumber}..."):
        date_str = date_input.strftime("%Y-%m-%d")
        if sumber == "IDX Daily Summary":
            out = run_script("idx-download.py", [date_str])
        else:
            out = run_script("broker_download.py", [ticker, date_str, date_str])
        
        st.success("✅ Selesai!")
        with st.expander("Lihat Log"):
            st.code(out, language="text")
        
        if os.path.exists(OUTPUT_DIR):
            files = glob.glob(os.path.join(OUTPUT_DIR, "*.xlsx")) + glob.glob(os.path.join(OUTPUT_DIR, "*.csv"))
            if files:
                latest = max(files, key=os.path.getctime)
                st.markdown(f"### 📄 Hasil: `{os.path.basename(latest)}`")
                try:
                    df = pd.read_csv(latest) if latest.endswith('.csv') else pd.read_excel(latest)
                    st.dataframe(df, use_container_width=True)
                    with open(latest, "rb") as f:
                        st.download_button("📥 Download File", f, os.path.basename(latest))
                except Exception as e:
                    st.error(f"Gagal baca file: {e}")
            else:
                st.warning("Tidak ada file hasil.")
