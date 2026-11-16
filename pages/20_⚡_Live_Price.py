import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.title("⚡ Live Price (Auto-Refresh)")
st.write("Pergerakan harga saham IDX secara *real-time* (update setiap X detik).")
st.divider()

col1, col2, col3 = st.columns([2, 2, 1.5])
with col1: ticker = st.text_input("Kode Saham (tanpa .JK):", value="BBCA").upper()
with col2: refresh_rate = st.slider("Interval Refresh (detik):", 5, 60, 10)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    aktif = st.checkbox("🟢 Aktifkan Live", value=True)

count = st_autorefresh(interval=refresh_rate*1000, limit=None, key="live") if aktif else 0
st.caption(f"🔄 Refresh ke-{count}")

try:
    df = yf.download(f"{ticker}.JK", period="1d", interval="1m", progress=False)
    if df.empty: st.warning("Data live tidak tersedia.")
    else:
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        lp = float(df['Close'].iloc[-1]); op = float(df['Open'].iloc[0])
        hi = float(df['High'].max()); lo = float(df['Low'].min())
        ch = lp - op; pct = (ch/op)*100
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Harga Terakhir", f"Rp {lp:,.0f}", f"{ch:+,.0f} ({pct:+.2f}%)")
        c2.metric("Low Hari Ini", f"Rp {lo:,.0f}")
        c3.metric("High Hari Ini", f"Rp {hi:,.0f}")
        c4.metric("Volume", f"{df['Volume'].sum():,.0f}")
        st.divider()
        st.line_chart(df['Close'], color="#00c853")
except Exception as e:
    st.error(f"Error: {e}")
