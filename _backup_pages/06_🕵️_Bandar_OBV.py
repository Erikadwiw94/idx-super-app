import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Bandar OBV", page_icon="🕵️", layout="wide")
st.title("🕵️ Big Money Tracker (Bandarmology)")
st.write("Lacak akumulasi/distribusi bandar via On-Balance Volume & Volume Spike.")
st.divider()

col1, col2, col3 = st.columns([2, 2, 1.5])
with col1:
    ticker = st.text_input("Kode Saham (tanpa .JK):", value="BBCA").upper()
with col2:
    periode = st.selectbox("Periode:", ["3mo", "6mo", "1y"], index=1)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    tombol = st.button("🔍 Lacak Bandar", type="primary", use_container_width=True)

st.divider()

if tombol:
    with st.spinner(f"Menganalisis {ticker}..."):
        df = yf.download(f"{ticker}.JK", period=periode, interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        if df.empty: st.error("Data tidak ditemukan."); st.stop()
        
        c, v = df['Close'].squeeze(), df['Volume'].squeeze()
        df['OBV'] = (np.sign(c.diff()) * v).fillna(0).cumsum()
        df['Vol_MA20'] = v.rolling(20).mean()
        df['Spike'] = v > df['Vol_MA20'] * 2
        df = df.dropna()
        
        ca, cb = float(c.iloc[0]), float(c.iloc[-1])
        oa, ob = float(df['OBV'].iloc[0]), float(df['OBV'].iloc[-1])
        dp = ((cb-ca)/ca)*100
        do = ((ob-oa)/abs(oa))*100 if oa != 0 else 0
        
        st.subheader(f"Analisis {ticker} ({periode})")
        m1, m2, m3 = st.columns(3)
        m1.metric("Perubahan Harga", f"{dp:.2f}%")
        m2.metric("Perubahan OBV", f"{do:.2f}%")
        
        if dp>0 and do>0: status = "🟢 AKUMULASI (Bandar Masuk)"
        elif dp<0 and do<0: status = "🔴 DISTRIBUSI (Bandar Keluar)"
        elif dp<0 and do>0: status = "🟡 DIVERGENSI BULLISH (Bandar Beli Diam-diam)"
        else: status = "⚪ NETRAL"
        m3.metric("Status", status)
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.6,0.4],
                           subplot_titles=("Harga & Volume Spike", "OBV"))
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)
        sp = df[df['Spike']]
        if not sp.empty:
            fig.add_trace(go.Scatter(x=sp.index, y=sp['Close'], mode='markers', name='Volume Spike', marker=dict(color='red', size=12, symbol='star')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], name='OBV', line=dict(color='purple', width=2)), row=2, col=1)
        fig.update_layout(height=700, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
