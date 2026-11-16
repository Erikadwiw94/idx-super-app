import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

st.set_page_config(page_title="Screener Saham", page_icon="📊", layout="wide")
st.title("📊 Screener Saham IDX (Full Market)")
st.write("Analisis teknikal super cepat untuk 900+ saham menggunakan database lokal.")
st.divider()

# === FORM DI TENGAH ===
col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
with col1:
    hanya_bullish = st.checkbox("🟢 Hanya Bullish (Harga > MA20)")
with col2:
    hanya_oversold = st.checkbox("💡 Hanya Oversold (RSI < 30)")
with col3:
    min_rsi = st.slider("Min RSI", 0, 100, 0)
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Mulai Scan", type="primary", use_container_width=True)

st.divider()

def hitung_rsi(series, periode=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=periode).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periode).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if mulai:
    with st.spinner("Membaca 900+ saham..."):
        conn = sqlite3.connect('stock_data.db')
        df_all = pd.read_sql("SELECT ticker, date, close FROM daily_prices ORDER BY ticker, date ASC", conn)
        conn.close()
        
        if df_all.empty:
            st.error("Database kosong. Jalankan `python update_all_stocks.py`.")
            st.stop()
        
        hasil = []
        for ticker, group in df_all.groupby('ticker'):
            if len(group) < 20: continue
            close = group['close']
            harga = close.iloc[-1]
            ma20 = close.rolling(20).mean().iloc[-1]
            rsi = hitung_rsi(close).iloc[-1]
            
            status = "🟢 Bullish" if harga > ma20 else "🔴 Bearish"
            if rsi > 70: status += " | ⚠️ Overbought"
            elif rsi < 30: status += " | 💡 Oversold"
            
            hasil.append({"Ticker": ticker, "Harga": round(harga, 0), "MA20": round(ma20, 0), "RSI": round(rsi, 1), "Status": status})
        
        df_hasil = pd.DataFrame(hasil)
        if hanya_bullish: df_hasil = df_hasil[df_hasil['Status'].str.contains("Bullish")]
        if hanya_oversold: df_hasil = df_hasil[df_hasil['RSI'] < 30]
        if min_rsi > 0: df_hasil = df_hasil[df_hasil['RSI'] >= min_rsi]
        
        st.success(f"✅ {len(df_hasil)} saham cocok dengan filter")
        st.dataframe(df_hasil, use_container_width=True, hide_index=True)
