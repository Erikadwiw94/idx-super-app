import streamlit as st
import subprocess

st.set_page_config(page_title="IDXLens Extractor", page_icon="📑", layout="wide")

st.title("📑 IDXLens (Financial Report Extractor)")
st.write("Ekstrak data laporan keuangan IDX (XLSX, XBRL, PDF) menggunakan proyek `idxlens`.")

IDXLENS_DIR = "/home/server/idxlens"
IDXLENS_BIN = f"{IDXLENS_DIR}/bin/idxlens"

st.sidebar.header("Parameter Ekstraksi")
ticker = st.sidebar.text_input("Kode Saham (misal: BBCA):", value="BBCA").upper()

tahun_input = st.sidebar.number_input("Tahun Laporan:", min_value=2010, max_value=2025, value=2023)

# Pilihan periode sesuai help: Q1, Q2, Q3, FY
periode = st.sidebar.selectbox("Periode:", ["FY", "Q1", "Q2", "Q3"], index=0)

if st.sidebar.button("🚀 Jalankan IDXLens", type="primary"):
    with st.spinner(f"Menjalankan `idxlens fetch {ticker} -y {tahun_input} -p {periode}`..."):
        try:
            # Perintah sesuai dengan --help: fetch TICKER -y TAHUN -p PERIODE
            cmd = [IDXLENS_BIN, "fetch", ticker, "-y", str(tahun_input), "-p", periode]
            
            result = subprocess.run(
                cmd,
                cwd=IDXLENS_DIR,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                st.success(f"✅ Berhasil menarik data **{ticker}** ({periode} {tahun_input})!")
            else:
                st.warning(f"⚠️ Proses selesai dengan kode keluar {result.returncode}.")
            
            if result.stdout:
                st.markdown("### 📄 Output (Stdout)")
                st.code(result.stdout, language="text")
                
            if result.stderr:
                st.markdown("### ⚠️ Log / Error (Stderr)")
                st.code(result.stderr, language="text")
                
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout! Proses memakan waktu lebih dari 5 menit.")
        except Exception as e:
            st.error(f"❌ Gagal mengeksekusi: {e}")
