import streamlit as st
import httpx
import time

st.set_page_config(page_title="Auto News", page_icon="📰", layout="wide")
st.title("📰 Auto News (Live API)")
st.write("Berita dan laporan dari server `auto-news` lokal (Port 3131 & 13052).")
st.divider()

REPORT_API_URL = "http://localhost:3131"
STOCK_API_URL = "http://localhost:13052"

col1, col2, col3 = st.columns([2.5, 2, 1.5])
with col1:
    layanan = st.radio("Pilih Layanan:", ["Laporan Harian", "Berita Saham"], horizontal=True)
with col2:
    ticker = st.text_input("Kode Saham (untuk berita):", value="BBCA").upper() if layanan == "Berita Saham" else ""
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    tarik = st.button("🔍 Tarik Data", type="primary", use_container_width=True)

st.divider()

if tarik:
    if layanan == "Laporan Harian":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Generate Laporan Baru (AI)", type="primary", use_container_width=True):
                with st.spinner("Memerintahkan AI..."):
                    try:
                        with httpx.Client(timeout=120.0) as client:
                            client.get(f"{STOCK_API_URL}/api/news/analyze")
                            st.success("✅ Laporan sedang dibuat!")
                    except Exception as e: st.error(f"Gagal: {e}")
        with c2:
            if st.button("📥 Tarik Laporan", type="secondary", use_container_width=True):
                with st.spinner("Mengambil laporan..."):
                    try:
                        with httpx.Client(timeout=10.0) as client:
                            r = client.get(f"{REPORT_API_URL}/")
                            if "Report Not Found" in r.text:
                                st.warning("⚠️ Belum ada laporan. Generate dulu.")
                            else:
                                st.success("✅ Laporan!")
                                st.markdown(r.text, unsafe_allow_html=True)
                    except Exception as e: st.error(f"Error: {e}")
    else:
        with st.spinner(f"Mencari berita {ticker}..."):
            try:
                with httpx.Client(timeout=30.0) as client:
                    ep = f"/api/news/analyze?ticker={ticker}"
                    r = client.get(f"{STOCK_API_URL}{ep}")
                    try: st.json(r.json())
                    except:
                        st.error("Respons bukan JSON:")
                        st.code(r.text, language="text")
            except Exception as e: st.error(f"Error: {e}")
