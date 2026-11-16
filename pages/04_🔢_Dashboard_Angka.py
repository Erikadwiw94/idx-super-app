import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta_classic as ta
import numpy as np
from datetime import datetime

st.title("🔢 Dashboard Indikator (Mode Angka)")
st.write("Melihat nilai terkini dari puluhan indikator tanpa membaca grafik.")
st.divider()

col1, col2, col3 = st.columns([2, 3, 1.5])
with col1:
    ticker = st.text_input("Kode Saham (tanpa .JK):", value="BBCA").upper()
with col2:
    tf = st.radio("Timeframe:", ["Harian", "Mingguan", "Bulanan"], horizontal=True)
with col3:
    st.markdown("<br><br>", unsafe_allow_html=True)
    mulai = st.button("Hitung Indikator", type="primary", use_container_width=True)

st.divider()

if mulai:
    interval, period = ("1d", "1y") if tf == "Harian" else (("1wk", "3y") if tf == "Mingguan" else ("1mo", "10y"))
    
    with st.spinner(f"Menarik data {tf}..."):
        df = yf.download(f"{ticker}.JK", period=period, interval=interval, progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        if df.empty or len(df) < 2: st.error("Data tidak cukup."); st.stop()
        
        c = float(df['Close'].iloc[-1])
        hasil = []
        def add(cat, name, val, sig): hasil.append({"Kategori": cat, "Indikator": name, "Nilai": val, "Sinyal": sig})
        
        def fmt(v, d=2): return "N/A" if pd.isna(v) else f"{v:,.{d}f}"
        
        sma = ta.sma(df['Close'], 20).iloc[-1]; add("Trend", "SMA 20", fmt(sma), "🟢" if c>sma else "🔴")
        ema = ta.ema(df['Close'], 50).iloc[-1]; add("Trend", "EMA 50", fmt(ema), "🟢" if c>ema else "🔴")
        m = ta.macd(df['Close']); add("Trend", "MACD", fmt(m.iloc[-1,0]), "🟢" if m.iloc[-1,0]>m.iloc[-1,1] else "🔴")
        a = ta.adx(df['High'], df['Low'], df['Close']); add("Trend", "ADX", fmt(a.iloc[-1,0]), "🔥" if a.iloc[-1,0]>25 else "⚪")
        
        r = ta.rsi(df['Close'], 14).iloc[-1]; add("Momentum", "RSI", fmt(r), "⚠️" if r>70 else ("💡" if r<30 else "⚪"))
        s = ta.stoch(df['High'], df['Low'], df['Close']).iloc[-1,0]; add("Momentum", "Stoch %K", fmt(s), "⚠️" if s>80 else ("💡" if s<20 else "⚪"))
        cci = ta.cci(df['High'], df['Low'], df['Close']).iloc[-1]; add("Momentum", "CCI", fmt(cci), "⚠️" if cci>100 else ("💡" if cci<-100 else "⚪"))
        
        bb = ta.bbands(df['Close'], 20, 2); add("Volatilitas", "BB Upper", fmt(bb.iloc[-1,2]), "Resistance"); add("Volatilitas", "BB Lower", fmt(bb.iloc[-1,0]), "Support")
        atr = ta.atr(df['High'], df['Low'], df['Close']).iloc[-1]; add("Volatilitas", "ATR", fmt(atr), "Volatilitas")
        
        obv = ta.obv(df['Close'], df['Volume']); sl = obv.iloc[-1]-obv.iloc[-5] if len(obv)>=5 else 0
        add("Bandar", "OBV", fmt(obv.iloc[-1], 0), "🟢 Akumulasi" if sl>0 else "🔴 Distribusi")
        cmf = ta.cmf(df['High'], df['Low'], df['Close'], df['Volume']).iloc[-1]; add("Bandar", "CMF", fmt(cmf, 4), "🟢" if cmf>0 else "🔴")
        
        res = pd.DataFrame(hasil)
        st.success(f"**{ticker}** | {tf} | Harga: **Rp {c:,.0f}**")
        
        t1, t2, t3, t4 = st.tabs(["📈 Trend", "⚡ Momentum", "🌊 Volatilitas", "🕵️ Bandar"])
        with t1: st.dataframe(res[res.Kategori=="Trend"].drop(columns='Kategori'), use_container_width=True, hide_index=True)
        with t2: st.dataframe(res[res.Kategori=="Momentum"].drop(columns='Kategori'), use_container_width=True, hide_index=True)
        with t3: st.dataframe(res[res.Kategori=="Volatilitas"].drop(columns='Kategori'), use_container_width=True, hide_index=True)
        with t4: st.dataframe(res[res.Kategori=="Bandar"].drop(columns='Kategori'), use_container_width=True, hide_index=True)
