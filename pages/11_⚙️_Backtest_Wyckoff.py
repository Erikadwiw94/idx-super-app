import streamlit as st
import subprocess
import pandas as pd
import os, glob

st.title("📐 Quant Research Screener (Wyckoff & Minervini)")
st.write("Menjalankan *backend* `idx-quant-research-platform` dan menampilkan hasilnya.")
st.divider()

PROJECT_DIR = "/home/server/idx-quant-research-platform"
VENV_PYTHON = f"{PROJECT_DIR}/venv/bin/python"
SCRIPT_PATH = f"{PROJECT_DIR}/run_screener.py"

col1, col2 = st.columns([3, 1.5])
with col1:
    watchlist_options = {
        "LQ45 (45 Saham - Cepat)": f"{PROJECT_DIR}/data/watchlists/lq45_watchlist.csv",
        "Seluruh Pasar (900+ Saham - Lambat)": f"{PROJECT_DIR}/data/watchlists/idx_watchlist.csv"
    }
    selected_watchlist_name = st.selectbox("Pilih Watchlist:", list(watchlist_options.keys()))
    selected_watchlist_path = watchlist_options[selected_watchlist_name]
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan Screener", type="primary", use_container_width=True)

st.divider()

if mulai:
    with st.spinner(f"Menjalankan screening untuk {selected_watchlist_name}..."):
        try:
            input_text = f"{selected_watchlist_path}\nN\n"
            result = subprocess.run([VENV_PYTHON, SCRIPT_PATH], cwd=PROJECT_DIR,
                capture_output=True, text=True, timeout=900, input=input_text)
            
            st.success("✅ Screening Selesai!")
            
            search_dir = os.path.join(PROJECT_DIR, "output", "screeners")
            csv_files = glob.glob(os.path.join(search_dir, "*.csv"))
            xlsx_files = glob.glob(os.path.join(search_dir, "*.xlsx"))
            
            latest = None
            if csv_files: latest = max(csv_files, key=os.path.getctime)
            elif xlsx_files: latest = max(xlsx_files, key=os.path.getctime)
            
            if latest:
                st.markdown(f"### 📊 Hasil: `{os.path.basename(latest)}`")
                df = pd.read_csv(latest) if latest.endswith('.csv') else pd.read_excel(latest)
                st.dataframe(df, use_container_width=True, hide_index=True)
                with open(latest, "rb") as f:
                    st.download_button("📥 Download Hasil", f, os.path.basename(latest))
            else:
                st.warning("File hasil tidak ditemukan.")
                with st.expander("Lihat Log"): st.code(result.stdout[-2000:])
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout! (>15 menit)")
        except Exception as e:
            st.error(f"❌ Error: {e}")
