import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Multi Stock", page_icon="📈", layout="wide")
st.title("📈 Multi-Stock Analysis (idx-stock-analysis)")
st.write("Analisis komparatif multi-saham, korelasi, dan visualisasi.")
st.divider()

# Form tengah
col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
with col1:
    tickers_input = st.text_area("Daftar Saham (pisahkan dengan koma):", value="BBCA, TLKM, ASII", height=68)
with col2:
    start_date = st.date_input("Tanggal Mulai:", datetime(2023, 1, 1))
with col3:
    end_date = st.date_input("Tanggal Akhir:", datetime.now())
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("Analisis Sekarang", type="primary", use_container_width=True)

st.divider()

if mulai:
    tickers_list = [t.strip().upper() + ".JK" for t in tickers_input.split(",") if t.strip()]
    if not tickers_list:
        st.warning("Masukkan minimal satu kode saham.")
        st.stop()
    
    with st.spinner(f"Mengunduh data {len(tickers_list)} saham..."):
        try:
            all_data = yf.download(tickers_list, start=start_date, end=end_date)
            if all_data.empty:
                st.error("Data tidak ditemukan."); st.stop()
            
            close_data = all_data['Close'] if isinstance(all_data.columns, pd.MultiIndex) else all_data[['Close']]
            if not isinstance(all_data.columns, pd.MultiIndex):
                close_data.columns = tickers_list
            
            st.success(f"✅ Data berhasil diunduh ({start_date} s/d {end_date})")
            
            # 1. Grafik Normalisasi
            st.subheader("📈 Perbandingan Harga (Normalisasi 100)")
            norm = (close_data / close_data.iloc[0]) * 100
            fig1 = go.Figure()
            for t in norm.columns:
                fig1.add_trace(go.Scatter(x=norm.index, y=norm[t], mode='lines', name=t.replace('.JK','')))
            fig1.update_layout(height=500, template="plotly_dark", hovermode="x unified")
            st.plotly_chart(fig1, use_container_width=True)
            
            # 2. Statistik
            st.subheader("📋 Ringkasan Statistik")
            stats = pd.DataFrame({
                "Harga Terakhir": close_data.iloc[-1],
                "Tertinggi": close_data.max(),
                "Terendah": close_data.min(),
                "Return Total (%)": ((close_data.iloc[-1] / close_data.iloc[0]) - 1) * 100,
                "Volatilitas (%)": close_data.pct_change().std() * 100,
            })
            st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)
            
            # 3. Korelasi
            st.subheader("🔗 Matriks Korelasi")
            ret = close_data.pct_change().dropna()
            corr = ret.corr()
            fig2 = go.Figure(data=go.Heatmap(z=corr.values,
                x=[c.replace('.JK','') for c in corr.columns],
                y=[i.replace('.JK','') for i in corr.index],
                colorscale='RdBu', zmin=-1, zmax=1,
                text=corr.round(2).values, texttemplate="%{text}", textfont={"size": 14}))
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            
            # 4. Candlestick
            t_name = tickers_list[0].replace('.JK','')
            st.subheader(f"🕯️ Candlestick: {t_name}")
            td = all_data.xs(tickers_list[0], axis=1, level=1) if isinstance(all_data.columns, pd.MultiIndex) else all_data
            fig3 = go.Figure(data=[go.Candlestick(x=td.index, open=td['Open'], high=td['High'], low=td['Low'], close=td['Close'], name=t_name)])
            fig3.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
