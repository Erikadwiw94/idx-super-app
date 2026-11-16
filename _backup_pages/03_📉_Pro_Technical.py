import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta_classic as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Pro Technical", page_icon="📉", layout="wide")

st.title("📉 Pro Technical Indicators")
st.write("Analisis teknikal lanjutan menggunakan library `pandas_ta` (Setara Stockbit Pro).")

# ==========================================
# FORM INPUT DI TENGAH LAYAR
# ==========================================
st.markdown("### ⚙️ Parameter Analisis")

# Daftar Indikator (dipindah ke atas agar bisa dipakai di selectbox)
indicator_options = [
    "MACD", "Bollinger Bands", "RSI", "Stochastic", "Supertrend", 
    "Ichimoku Cloud", "Parabolic SAR", "VWAP", "On Balance Volume (OBV)", 
    "Average Directional Index (ADX)", "Commodity Channel Index (CCI)",
    "Awesome Oscillator", "Chaikin Money Flow", "Williams %R"
]

col1, col2, col3, col4 = st.columns([2, 2, 3, 1.5])

with col1:
    ticker = st.text_input("Kode Saham (tanpa .JK)", value="BBCA").upper()

with col2:
    period = st.selectbox("Periode", ["3mo", "6mo", "1y", "2y"], index=2)

with col3:
    selected_indicator = st.selectbox("Pilih Indikator", indicator_options)

with col4:
    st.markdown("<br>", unsafe_allow_html=True) # Spasi agar tombol sejajar dengan input
    tombol_tampil = st.button("Tampilkan Chart", type="primary", use_container_width=True)

st.divider()

# ==========================================
# LOGIKA GRAFIK
# ==========================================
if tombol_tampil:
    with st.spinner(f"Menarik data dan menghitung {selected_indicator}..."):
        try:
            df = yf.download(f"{ticker}.JK", period=period, interval="1d", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            if df.empty:
                st.error("Data tidak ditemukan.")
                st.stop()

            # Setup Subplots (Baris 2 jika indikator butuh panel terpisah di bawah)
            butuh_panel_bawah = ["MACD", "RSI", "Stochastic", "OBV", "ADX", "CCI", "Awesome Oscillator", "Chaikin Money Flow", "Williams %R"]
            rows = 2 if selected_indicator in butuh_panel_bawah else 1
            
            fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.05, 
                                row_heights=[0.7, 0.3] if rows == 2 else [1])

            # 1. SELALU TAMPILKAN CANDLESTICK DI ATAS
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)

            # 2. LOGIKA MENGGAMBAR INDIKATOR
            if selected_indicator == "MACD":
                macd = df.ta.macd(fast=12, slow=26, signal=9)
                fig.add_trace(go.Scatter(x=df.index, y=macd.iloc[:,0], name='MACD', line=dict(color='blue')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=macd.iloc[:,1], name='Signal', line=dict(color='orange')), row=2, col=1)
                fig.add_trace(go.Bar(x=df.index, y=macd.iloc[:,2], name='Histogram', marker_color='gray'), row=2, col=1)

            elif selected_indicator == "Bollinger Bands":
                bbands = df.ta.bbands(length=20, std=2)
                fig.add_trace(go.Scatter(x=df.index, y=bbands.iloc[:,0], name='Lower', line=dict(color='green', dash='dash')), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=bbands.iloc[:,1], name='Middle', line=dict(color='gray')), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=bbands.iloc[:,2], name='Upper', line=dict(color='red', dash='dash')), row=1, col=1)

            elif selected_indicator == "RSI":
                rsi = df.ta.rsi(length=14)
                fig.add_trace(go.Scatter(x=df.index, y=rsi, name='RSI', line=dict(color='purple')), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

            elif selected_indicator == "Stochastic":
                stoch = df.ta.stoch(k=14, d=3, smooth_k=3)
                fig.add_trace(go.Scatter(x=df.index, y=stoch.iloc[:,0], name='%K', line=dict(color='blue')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=stoch.iloc[:,1], name='%D', line=dict(color='orange')), row=2, col=1)
                fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)

            elif selected_indicator == "Supertrend":
                supertrend = df.ta.supertrend(length=10, multiplier=3)
                fig.add_trace(go.Scatter(x=df.index, y=supertrend.iloc[:,0], name='Supertrend', line=dict(color='red', width=2)), row=1, col=1)

            elif selected_indicator == "Ichimoku Cloud":
                ichimoku = df.ta.ichimoku()
                if not ichimoku[0].empty:
                    ich_df = ichimoku[0]
                    fig.add_trace(go.Scatter(x=df.index, y=ich_df.iloc[:,0], name='Tenkan', line=dict(color='blue')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=ich_df.iloc[:,1], name='Kijun', line=dict(color='red')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=ich_df.iloc[:,2], name='Senkou A', line=dict(color='green', dash='dot')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=ich_df.iloc[:,3], name='Senkou B', line=dict(color='orange', dash='dot')), row=1, col=1)

            elif selected_indicator == "Parabolic SAR":
                psar = df.ta.psar()
                fig.add_trace(go.Scatter(x=df.index, y=psar.iloc[:,0], name='PSAR Long', mode='markers', marker=dict(color='green', symbol='circle', size=5)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=psar.iloc[:,1], name='PSAR Short', mode='markers', marker=dict(color='red', symbol='circle', size=5)), row=1, col=1)

            elif selected_indicator == "VWAP":
                vwap = df.ta.vwap()
                fig.add_trace(go.Scatter(x=df.index, y=vwap, name='VWAP', line=dict(color='orange', width=2)), row=1, col=1)

            elif selected_indicator == "On Balance Volume (OBV)":
                obv = df.ta.obv()
                fig.add_trace(go.Scatter(x=df.index, y=obv, name='OBV', line=dict(color='purple')), row=2, col=1)

            elif selected_indicator == "Average Directional Index (ADX)":
                adx = df.ta.adx(length=14)
                fig.add_trace(go.Scatter(x=df.index, y=adx.iloc[:,0], name='ADX', line=dict(color='black')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=adx.iloc[:,1], name='DI+', line=dict(color='green')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=adx.iloc[:,2], name='DI-', line=dict(color='red')), row=2, col=1)

            elif selected_indicator == "Commodity Channel Index (CCI)":
                cci = df.ta.cci(length=20)
                fig.add_trace(go.Scatter(x=df.index, y=cci, name='CCI', line=dict(color='blue')), row=2, col=1)
                fig.add_hline(y=100, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=-100, line_dash="dash", line_color="green", row=2, col=1)
                
            elif selected_indicator == "Awesome Oscillator":
                ao = df.ta.ao()
                fig.add_trace(go.Bar(x=df.index, y=ao, name='AO', marker_color='teal'), row=2, col=1)

            elif selected_indicator == "Chaikin Money Flow":
                cmf = df.ta.cmf()
                fig.add_trace(go.Scatter(x=df.index, y=cmf, name='CMF', line=dict(color='brown')), row=2, col=1)
                fig.add_hline(y=0, line_dash="dash", line_color="white", row=2, col=1)

            elif selected_indicator == "Williams %R":
                wr = df.ta.willr()
                fig.add_trace(go.Scatter(x=df.index, y=wr, name='Williams %R', line=dict(color='magenta')), row=2, col=1)
                fig.add_hline(y=-20, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=-80, line_dash="dash", line_color="green", row=2, col=1)

            fig.update_layout(height=800, template="plotly_dark", xaxis_rangeslider_visible=False, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghitung indikator: {e}")
