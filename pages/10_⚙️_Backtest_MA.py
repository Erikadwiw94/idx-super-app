import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("⚙️ Backtest Strategi MA Crossover")
st.write("Uji strategi Moving Average Crossover (Golden Cross / Death Cross) pada saham IDX.")
st.divider()

col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
with col1: ticker = st.text_input("Kode Saham", value="BBCA").upper()
with col2: period = st.selectbox("Periode", ["1y", "2y", "5y", "10y"], index=2)
with col3: ma_c = st.number_input("MA Cepat", 5, 50, 20)
with col4: ma_l = st.number_input("MA Lambat", 20, 200, 50)
with col5: st.markdown("<br>", unsafe_allow_html=True); go_btn = st.button("🚀 Backtest", type="primary", use_container_width=True)

st.divider()

if go_btn:
    with st.spinner("Menjalankan backtest..."):
        df = yf.download(f"{ticker}.JK", period=period, interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        if df.empty: st.error("Data tidak ditemukan."); st.stop()
        
        df['MA_C'] = df['Close'].rolling(ma_c).mean()
        df['MA_L'] = df['Close'].rolling(ma_l).mean()
        df['Sinyal'] = (df['MA_C'] > df['MA_L']).astype(int)
        df['Ret'] = df['Close'].pct_change()
        df['Ret_S'] = df['Ret'] * df['Sinyal'].shift(1)
        df['Eq_S'] = 10000000 * (1 + df['Ret_S']).cumprod()
        df['Eq_BH'] = 10000000 * (1 + df['Ret']).cumprod()
        df = df.dropna()
        
        fe_s, fe_bh = df['Eq_S'].iloc[-1], df['Eq_BH'].iloc[-1]
        roi = ((fe_s-10000000)/10000000)*100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Ekuitas Strategi", f"Rp {fe_s:,.0f}", f"{roi:+.2f}%")
        c2.metric("Buy & Hold", f"Rp {fe_bh:,.0f}", f"{((fe_bh/10000000)-1)*100:+.2f}%")
        c3.metric("Profit", f"Rp {fe_s-10000000:,.0f}")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Eq_S'], name='Strategi', line=dict(color='green', width=2)))
        fig.add_trace(go.Scatter(x=df.index, y=df['Eq_BH'], name='Buy & Hold', line=dict(color='gray', width=2, dash='dash')))
        fig.update_layout(height=400, template="plotly_dark", title="Perbandingan Ekuitas")
        st.plotly_chart(fig, use_container_width=True)
