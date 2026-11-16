import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import os

st.set_page_config(page_title="Bandar Accumulation", page_icon="🕵️", layout="wide")
st.title("🕵️ Bandar Accumulation Score (7 Hari)")
st.write("Analisis akumulasi/distribusi bandar berdasarkan data IDX 7 hari terakhir.")
st.divider()

DATA_DIR = Path("/home/server/smart-money-idx/Data")

# ============================================================
# FUNGSI ANALISIS
# ============================================================
def robust_zscore(series):
    median = series.median()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return pd.Series(0, index=series.index)
    return (series - median) / iqr

@st.cache_data(ttl=3600)
def load_and_analyze():
    files = sorted(DATA_DIR.glob("*.xlsx"))
    if not files:
        return None, "Tidak ada file Excel di folder Data/"
    
    # Load semua
    dfs = []
    for f in files:
        temp = pd.read_excel(f)
        temp["source"] = f.stem
        dfs.append(temp)
    
    df = pd.concat(dfs, ignore_index=True)
    
    # Parse tanggal
    if "Tanggal Perdagangan Terakhir" in df.columns:
        df["Tanggal Perdagangan Terakhir"] = pd.to_datetime(
            df["Tanggal Perdagangan Terakhir"], format="%d %b %Y", errors="coerce"
        )
        df = df.sort_values(["Kode Saham", "Tanggal Perdagangan Terakhir"]).reset_index(drop=True)
    
    # Drop kolom tidak perlu
    drop_cols = [c for c in ["No", "Remarks"] if c in df.columns]
    df = df.drop(columns=drop_cols)
    
    # === FEATURE ENGINEERING ===
    df["return_close"] = df.groupby("Kode Saham")["Penutupan"].pct_change()
    df["range_harian"] = df["Tertinggi"] - df["Terendah"]
    df["gap_open"] = df["Open Price"] - df["Sebelumnya"]
    df["log_volume"] = np.log1p(df["Volume"])
    df["log_value"] = np.log1p(df["Nilai"])
    df["volume_change"] = df.groupby("Kode Saham")["Volume"].pct_change()
    
    df["foreign_net"] = df["Foreign Buy"] - df["Foreign Sell"]
    df["foreign_ratio"] = np.where(df["Volume"] > 0, df["foreign_net"] / df["Volume"], 0)
    df["bid_offer_imbalance"] = np.where(
        (df["Bid Volume"] + df["Offer Volume"]) > 0,
        (df["Bid Volume"] - df["Offer Volume"]) / (df["Bid Volume"] + df["Offer Volume"]),
        0
    )
    df["volatility_proxy"] = np.where(df["Penutupan"] > 0, df["range_harian"] / df["Penutupan"], 0)
    
    df["foreign_net_3d"] = df.groupby("Kode Saham")["foreign_net"].rolling(window=3, min_periods=1).sum().reset_index(level=0, drop=True)
    df["volume_ma3"] = df.groupby("Kode Saham")["Volume"].rolling(window=3, min_periods=1).mean().reset_index(level=0, drop=True)
    df["volume_spike"] = (df["Volume"] > 1.5 * df["volume_ma3"]).astype(int)
    
    # === Z-SCORES ===
    df["z_foreign_net_3d"] = robust_zscore(df["foreign_net_3d"])
    df["z_foreign_ratio"] = robust_zscore(df["foreign_ratio"])
    df["z_bid_offer"] = robust_zscore(df["bid_offer_imbalance"])
    df["z_return"] = robust_zscore(df["return_close"].fillna(0))
    
    # === BANDAR SCORE ===
    df["bandar_score"] = (
        0.35 * df["z_foreign_net_3d"] +
        0.20 * df["z_foreign_ratio"] +
        0.20 * df["z_bid_offer"] +
        0.15 * df["volume_spike"] +
        0.10 * df["z_return"]
    )
    
    # === AGGREGATE PER SAHAM ===
    score_7d = df.groupby("Kode Saham").agg(
        avg_bandar_score=("bandar_score", "mean"),
        sum_bandar_score=("bandar_score", "sum"),
        total_foreign_net=("foreign_net", "sum"),
        freq_volume_spike=("volume_spike", "sum"),
        avg_return=("return_close", "mean"),
        last_close=("Penutupan", "last"),
        avg_volume=("Volume", "mean"),
    ).sort_values("sum_bandar_score", ascending=False).reset_index()
    
    return df, score_7d, len(files)

# ============================================================
# ANALISIS
# ============================================================
with st.spinner("Memuat & menganalisis 7 file Excel..."):
    result = load_and_analyze()

if result[0] is None:
    st.error(result[1])
    st.stop()

df, score_7d, n_files = result

st.success(f"✅ Analisis selesai: {len(score_7d)} saham dari {n_files} file Excel")

# ============================================================
# METRIK RINGKASAN
# ============================================================
threshold_top = score_7d["sum_bandar_score"].quantile(0.90)
threshold_bot = score_7d["sum_bandar_score"].quantile(0.10)

top_accumulation = score_7d[score_7d["sum_bandar_score"] >= threshold_top]
top_distribution = score_7d[score_7d["sum_bandar_score"] <= threshold_bot]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Saham", len(score_7d))
c2.metric("🟢 Top Akumulasi (Top 10%)", len(top_accumulation))
c3.metric("🔴 Top Distribusi (Bot 10%)", len(top_distribution))
c4.metric("Data Range", f"{df['Tanggal Perdagangan Terakhir'].min().strftime('%d %b')} – {df['Tanggal Perdagangan Terakhir'].max().strftime('%d %b')}")

st.divider()

# ============================================================
# TABEL TOP AKUMULASI & DISTRIBUSI
# ============================================================
t1, t2, t3 = st.tabs(["🟢 Top 20 Akumulasi", "🔴 Top 20 Distribusi", "📋 Semua Saham"])

def render_table(df_sub):
    out = df_sub.copy()
    out["avg_bandar_score"] = out["avg_bandar_score"].round(3)
    out["sum_bandar_score"] = out["sum_bandar_score"].round(3)
    out["total_foreign_net"] = (out["total_foreign_net"] / 1e9).round(2).astype(str) + " M"
    out["avg_return"] = (out["avg_return"] * 100).round(2).astype(str) + "%"
    out["last_close"] = out["last_close"].apply(lambda x: f"Rp {x:,.0f}")
    out["avg_volume"] = (out["avg_volume"] / 1e6).round(2).astype(str) + " Jt"
    out.columns = ["Ticker", "Avg Score", "Sum Score", "Foreign Net", "Vol Spike", "Avg Return", "Harga", "Avg Vol"]
    return out

with t1:
    st.markdown("#### 20 Saham dengan Skor Akumulasi Tertinggi")
    st.caption("Indikasi bandar sedang mengumpulkan saham (akumulasi).")
    st.dataframe(render_table(top_accumulation.head(20)), use_container_width=True, hide_index=True)

with t2:
    st.markdown("#### 20 Saham dengan Skor Distribusi Tertinggi")
    st.caption("Indikasi bandar sedang melepas saham (distribusi).")
    st.dataframe(render_table(top_distribution.head(20)), use_container_width=True, hide_index=True)

with t3:
    st.markdown("#### Semua Saham (urut skor akumulasi)")
    st.dataframe(render_table(score_7d), use_container_width=True, hide_index=True)
    csv = score_7d.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "bandar_accumulation_score_7d.csv", "text/csv")

st.divider()

# ============================================================
# GRAFIK TOP 15 AKUMULASI & DISTRIBUSI
# ============================================================
st.subheader("📊 Visualisasi Skor Akumulasi vs Distribusi")

col_a, col_b = st.columns(2)

with col_a:
    fig1 = go.Figure(go.Bar(
        x=top_accumulation.head(15)["Kode Saham"],
        y=top_accumulation.head(15)["sum_bandar_score"],
        marker_color="#00c853",
        text=top_accumulation.head(15)["sum_bandar_score"].round(2),
        textposition="outside",
    ))
    fig1.update_layout(title="🟢 Top 15 Akumulasi", template="plotly_dark", height=400,
                       xaxis_title="Saham", yaxis_title="Sum Bandar Score", showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = go.Figure(go.Bar(
        x=top_distribution.head(15)["Kode Saham"],
        y=top_distribution.head(15)["sum_bandar_score"],
        marker_color="#ff4b4b",
        text=top_distribution.head(15)["sum_bandar_score"].round(2),
        textposition="outside",
    ))
    fig2.update_layout(title="🔴 Top 15 Distribusi", template="plotly_dark", height=400,
                       xaxis_title="Saham", yaxis_title="Sum Bandar Score", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# DISTRIBUSI SKOR
# ============================================================
st.subheader("📈 Distribusi Skor Akumulasi")
fig3 = go.Figure(go.Histogram(x=score_7d["sum_bandar_score"], nbinsx=50, marker_color="#00c853"))
fig3.update_layout(template="plotly_dark", height=350,
                   xaxis_title="Sum Bandar Score", yaxis_title="Jumlah Saham")
st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# DETAIL SAHAM
# ============================================================
st.divider()
st.subheader("🔍 Detail Per Saham")

col_x, col_y = st.columns([2, 1.5])
with col_x:
    selected_ticker = st.selectbox("Pilih Saham:", score_7d["Kode Saham"].tolist())
with col_y:
    st.markdown("<br>", unsafe_allow_html=True)
    show_detail = st.button("Tampilkan Detail", type="primary", use_container_width=True)

if show_detail:
    stock_df = df[df["Kode Saham"] == selected_ticker].sort_values("Tanggal Perdagangan Terakhir")
    info = score_7d[score_7d["Kode Saham"] == selected_ticker].iloc[0]
    
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Sum Bandar Score", f"{info['sum_bandar_score']:.2f}")
    d2.metric("Avg Bandar Score", f"{info['avg_bandar_score']:.2f}")
    d3.metric("Foreign Net", f"Rp {info['total_foreign_net']/1e9:.2f} M")
    d4.metric("Vol Spike", f"{int(info['freq_volume_spike'])}x")
    
    # Grafik harga + score per hari
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=stock_df["Tanggal Perdagangan Terakhir"], y=stock_df["Penutupan"],
                             mode="lines+markers", name="Harga", line=dict(color="#00c853", width=2),
                             yaxis="y1"))
    fig4.add_trace(go.Bar(x=stock_df["Tanggal Perdagangan Terakhir"], y=stock_df["bandar_score"],
                         name="Bandar Score", marker_color="#ff9800", yaxis="y2"))
    fig4.update_layout(
        template="plotly_dark", height=400,
        title=f"{selected_ticker} — Harga & Bandar Score Harian",
        yaxis=dict(title="Harga (Rp)"),
        yaxis2=dict(title="Bandar Score", overlaying="y", side="right"),
        hovermode="x unified",
    )
    st.plotly_chart(fig4, use_container_width=True)
