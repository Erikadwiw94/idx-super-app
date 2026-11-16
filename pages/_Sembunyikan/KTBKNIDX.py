import streamlit as st
import subprocess
import os
import pandas as pd

st.set_page_config(page_title="IDX Disclosure", page_icon="📢", layout="wide")

st.title("📢 IDX Corporate Disclosure (KTBKNIDX)")
st.write("Mengambil pengumuman resmi (Keterbukaan Informasi) dari Bursa Efek Indonesia.")

PROJECT_DIR = "/home/server/ktbknidx"
VENV_PYTHON = f"{PROJECT_DIR}/venv/bin/python"
SCRIPT_PATH = f"{PROJECT_DIR}/quick_scrape.py"

# Cek apakah script quick_scrape.py ada
if not os.path.exists(SCRIPT_PATH):
    st.error(f"Script tidak ditemukan di {SCRIPT_PATH}. Pastikan proyek ktbknidx sudah ter-clone dengan benar.")
    st.stop()

if st.button("🚀 Tarik Pengumuman Terbaru", type="primary"):
    with st.spinner("Menjalankan scraper IDX. Mohon tunggu..."):
        try:
            # Jalankan script python
            result = subprocess.run(
                [VENV_PYTHON, SCRIPT_PATH],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True,
                timeout=300 # Timeout 5 menit
            )
            
            if result.returncode == 0:
                st.success("✅ Scraper berhasil dijalankan!")
            else:
                st.warning(f"⚠️ Script selesai dengan kode {result.returncode}.")
            
            # Tampilkan output terminal
            if result.stdout:
                st.markdown("### 📄 Output Terminal")
                st.code(result.stdout, language="text")
                
            if result.stderr:
                with st.expander("⚠️ Lihat Log Error"):
                    st.code(result.stderr, language="text")
                    
            # Cek apakah ada file CSV/Excel yang baru dibuat
            csv_files = []
            for root, dirs, files in os.walk(PROJECT_DIR):
                for file in files:
                    if file.endswith('.csv') or file.endswith('.xlsx'):
                        csv_files.append(os.path.join(root, file))
                        
            if csv_files:
                latest_file = max(csv_files, key=os.path.getctime)
                st.markdown(f"### 📊 Hasil Terbaru: `{os.path.basename(latest_file)}`")
                try:
                    if latest_file.endswith('.csv'):
                        df = pd.read_csv(latest_file)
                    else:
                        df = pd.read_excel(latest_file)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.warning(f"Gagal membaca file hasil: {e}")
                    
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout! Proses memakan waktu lebih dari 5 menit.")
        except Exception as e:
            st.error(f"❌ Gagal mengeksekusi: {e}")
