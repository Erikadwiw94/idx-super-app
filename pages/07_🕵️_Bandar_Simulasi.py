import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title("🕵️ Simulasi Bandarmology")
st.write("Simulasi data transaksi broker untuk latihan analisis. **Bukan data asli.**")
st.divider()

# ============ FORM DI TENGAH ============
col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
with col1:
    ticker = st.text_input("Kode Saham:", value="BBCA").upper()
with col2:
    hari = st.selectbox("Periode:", ["1 Hari", "1 Minggu", "1 Bulan", "3 Bulan"], index=2)
with col3:
    seed = st.number_input("Seed (Random):", 1, 9999, 42, help="Ganti untuk simulasi berbeda")
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🎲 Generate Simulasi", type="primary", use_container_width=True)

st.divider()

# ============ LOGIKA SIMULASI ============
if mulai:
    np.random.seed(seed)
    
    n_days = {"1 Hari": 1, "1 Minggu": 5, "1 Bulan": 22, "3 Bulan": 66}[hari]
    
    # Daftar broker IDX populer (kode 2 huruf)
    brokers = ["BK", "CC", "AK", "YP", "DX", "ZP", "NI", "RX", "MG", "CD",
               "CP", "KZ", "XL", "PD", "SQ", "DR", "GR", "IF", "HP", "EP"]
    broker_types = {
        "BK": "Asing", "AK": "Asing", "DX": "Asing", "ZP": "Asing", "RX": "Asing",
        "KZ": "Asing", "DR": "Asing", "IF": "Asing",
        "CC": "BUMN", "NI": "BUMN", "MG": "Lokal", "CD": "Lokal", "CP": "Lokal",
        "PD": "Lokal", "GR": "Lokal", "HP": "Lokal", "EP": "Lokal",
        "YP": "Retail", "XL": "Retail", "SQ": "Retail",
    }
    
    # Harga dasar simulasi
    base_price = np.random.uniform(1000, 10000)
    
    # Data per broker
    results = []
    for b in brokers:
        buy_vol = int(np.random.uniform(10000, 5000000))
        sell_vol = int(np.random.uniform(10000, 5000000))
        avg_buy = base_price * np.random.uniform(0.98, 1.02)
        avg_sell = base_price * np.random.uniform(0.98, 1.02)
        
        net_vol = buy_vol - sell_vol
        net_val = net_vol * base_price
        
        results.append({
            "Broker": b,
            "Tipe": broker_types.get(b, "Lokal"),
            "Buy Lot": buy_vol // 100,
            "Buy Value": buy_vol * avg_buy,
            "Sell Lot": sell_vol // 100,
            "Sell Value": sell_vol * avg_sell,
            "Net Lot": net_vol // 100,
            "Net Value": net_val,
            "Avg Buy": avg_buy,
            "Avg Sell": avg_sell,
        })
    
    df = pd.DataFrame(results)
    df = df.sort_values("Net Value", ascending=False).reset_index(drop=True)
    
    # ============ METRIK ============
    total_buy = df['Buy Value'].sum()
    total_sell = df['Sell Value'].sum()
    net_total = total_buy - total_sell
    
    st.success(f"✅ Simulasi {ticker} — {hari} — Seed: {seed}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Beli", f"Rp {total_buy/1e9:.2f} M")
    m2.metric("Total Jual", f"Rp {total_sell/1e9:.2f} M")
    m3.metric("Net Value", f"Rp {net_total/1e9:.2f} M", "🟢 Akumulasi" if net_total > 0 else "🔴 Distribusi")
    m4.metric("Simulasi Harga", f"Rp {base_price:,.0f}")
    
    st.divider()
    
    # ============ TOP BROKER ============
    st.subheader("🏆 Peringkat Broker (berdasarkan Net Value)")
    
    tab1, tab2, tab3 = st.tabs(["📊 Semua Broker", "🟢 Top 5 Akumulasi", "🔴 Top 5 Distribusi"])
    
    with tab1:
        df_display = df.copy()
        df_display['Buy Value'] = df_display['Buy Value'].apply(lambda x: f"Rp {x/1e9:.2f} M")
        df_display['Sell Value'] = df_display['Sell Value'].apply(lambda x: f"Rp {x/1e9:.2f} M")
        df_display['Net Value'] = df_display['Net Value'].apply(lambda x: f"Rp {x/1e9:+.2f} M")
        df_display['Avg Buy'] = df_display['Avg Buy'].apply(lambda x: f"Rp {x:,.0f}")
        df_display['Avg Sell'] = df_display['Avg Sell'].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(df_display[['Broker','Tipe','Buy Lot','Buy Value','Sell Lot','Sell Value','Net Lot','Net Value']],
                    use_container_width=True, hide_index=True)
    
    with tab2:
        top_buy = df[df['Net Value'] > 0].head(5)
        if not top_buy.empty:
            for _, row in top_buy.iterrows():
                col_a, col_b, col_c = st.columns([1, 3, 2])
                col_a.markdown(f"### {row['Broker']}")
                col_b.markdown(f"**{row['Tipe']}** — Net: {row['Net Lot']:,} lot")
                col_c.markdown(f"**Rp {row['Net Value']/1e9:+.2f} M**")
        else:
            st.info("Tidak ada broker dengan net buy pada simulasi ini.")
    
    with tab3:
        top_sell = df[df['Net Value'] < 0].tail(5).iloc[::-1]
        if not top_sell.empty:
            for _, row in top_sell.iterrows():
                col_a, col_b, col_c = st.columns([1, 3, 2])
                col_a.markdown(f"### {row['Broker']}")
                col_b.markdown(f"**{row['Tipe']}** — Net: {row['Net Lot']:,} lot")
                col_c.markdown(f"**Rp {row['Net Value']/1e9:+.2f} M**")
        else:
            st.info("Tidak ada broker dengan net sell pada simulasi ini.")
    
    st.divider()
    
    # ============ GRAFIK ============
    st.subheader("📊 Distribusi Net Value per Broker")
    
    fig = go.Figure()
    colors = ['#00c853' if v > 0 else '#ff4b4b' for v in df['Net Value']]
    fig.add_trace(go.Bar(
        x=df['Broker'], y=df['Net Value'] / 1e9,
        marker_color=colors,
        text=[f"{v/1e9:+.2f}M" for v in df['Net Value']],
        textposition='outside',
        name='Net Value'
    ))
    fig.update_layout(
        height=400, template="plotly_dark",
        xaxis_title="Broker", yaxis_title="Net Value (Miliar Rp)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.info("💡 **Catatan:** Ini adalah data **simulasi** dengan seed acak. Untuk data asli, gunakan menu **08_Bandar_Summary_Live** atau **25_Idx_Broker_Summary**.")
