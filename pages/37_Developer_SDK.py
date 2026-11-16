import streamlit as st

st.set_page_config(page_title="Developer SDK & Scraper", layout="wide")
st.title("🛠️ Developer SDK & Scraper")

st.markdown("""
Halaman ini merangkum proyek Open Source yang berjalan di *background* berbasis CLI/API/Scraper.

### 1. Invezgo SDK (Python & Go)
*Terletak di:* `/home/server/invezgo-python-sdk` dan `/home/server/invezgo-go-sdk`.
*Fungsi:* SDK untuk menarik data market, broker, dan *foreign flow* secara terprogram.

### 2. IDX-BEI Scraper
*Terletak di:* `/home/server/idx-bei`.
*Fungsi:* Scraper untuk menarik data laporan keuangan dan *broker summary* langsung dari web IDX.

### 3. IDX Dataset & Transaction Summary
*Terletak di:* `/home/server/idx_dataset` dan `/home/server/idx-transaction-summary`.
*Fungsi:* Kumpulan dataset historis dan ringkasan transaksi harian.

### 4. KTBKNIDX (Bot Telegram)
*Terletak di:* `/home/server/ktbknidx`.
*Fungsi:* Bot Telegram untuk memantau *Corporate Disclosure* IDX.

### 5. Quant Research Platform
*Terletak di:* `/home/server/idx-quant-research-platform`.
*Fungsi:* Platform riset kuantitatif dan *backtesting*.
""")
