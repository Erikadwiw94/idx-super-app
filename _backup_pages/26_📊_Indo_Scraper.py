import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Indo Stock Scraper", page_icon="📊", layout="wide")

st.title("📊 Indo Stock Scraper (Modern Version)")
st.write("Mengambil data harga dan fundamental dari Yahoo Finance (menggantikan script lama `indonesia-stocks-scraper`).")

ticker_input = st.sidebar.text_input("Kode Saham (tanpa .JK):", value="BBRI").upper()

tab1, tab2 = st.tabs(["💰 Harga Harian", "📈 Fundamental"])

# TAB 1: HARGA HARIAN (Menggantikan fungsi Stock_Price_Fetcher)
with tab1:
    st.subheader("Harga Penutupan (Close Price)")
    
    if st.button("Ambil Harga Terbaru", type="primary"):
        with st.spinner(f"Mengambil harga {ticker_input}..."):
            try:
                tkr = yf.Ticker(f"{ticker_input}.JK")
                # Ambil data 5 hari terakhir
                hist = tkr.history(period="5d")
                
                if hist.empty:
                    st.error("Data tidak ditemukan untuk saham tersebut.")
                else:
                    # Ambil harga penutupan terakhir
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else last_close
                    
                    change = last_close - prev_close
                    pct_change = (change / prev_close) * 100
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Harga Terakhir", f"Rp {last_close:,.0f}", f"{change:,.0f} ({pct_change:.2f}%)")
                    col2.metric("Harga Penutupan Kemarin", f"Rp {prev_close:,.0f}")
                    
                    st.markdown("### 📋 Riwayat 5 Hari Terakhir")
                    st.dataframe(hist[['Open', 'High', 'Low', 'Close', 'Volume']], use_container_width=True)
            except Exception as e:
                st.error(f"Gagal mengambil data: {e}")

# TAB 2: FUNDAMENTAL (Menggantikan fungsi RTI/IDX Scraper)
with tab2:
    st.subheader("Data Fundamental")
    
    if st.button("Ambil Data Fundamental", type="primary"):
        with st.spinner(f"Mengambil data fundamental {ticker_input}..."):
            try:
                tkr = yf.Ticker(f"{ticker_input}.JK")
                info = tkr.info
                
                # Tampilkan dalam bentuk tabel/metrik
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Market Cap", f"Rp {info.get('marketCap', 0):,.0f}")
                col1.metric("PE Ratio", info.get('trailingPE', 'N/A'))
                col1.metric("PBV Ratio", info.get('priceToBook', 'N/A'))
                
                col2.metric("ROE", f"{info.get('returnOnEquity', 0) * 100:.2f}%" if info.get('returnOnEquity') else 'N/A')
                col2.metric("EPS", info.get('trailingEps', 'N/A'))
                col2.metric("Dividend Yield", f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A')
                
                col3.metric("Sektor", info.get('sector', 'N/A'))
                col3.metric("Industri", info.get('industry', 'N/A'))
                col3.metric("Karyawan", f"{info.get('fullTimeEmployees', 0):,.0f}")
                
                st.info(f"**Deskripsi Perusahaan:**\n{info.get('longBusinessSummary', 'Tidak ada deskripsi.')}")
                
            except Exception as e:
                st.error(f"Gagal mengambil data fundamental: {e}")
