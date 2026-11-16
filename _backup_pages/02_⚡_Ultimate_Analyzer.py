import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser, urllib.parse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Ultimate Analyzer", page_icon="🧠", layout="wide")
st.title("🧠 Ultimate AI Analyzer")
st.write("Analisis komprehensif: Teknikal + Fundamental + Bandarmology + Sentimen.")
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    ticker_input = st.text_input("Kode Saham (tanpa .JK):", value="BBCA").upper()
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    tombol = st.button("🔍 Analisis Menyeluruh", type="primary", use_container_width=True)

st.divider()

@st.cache_data(ttl=300)
def get_stock_data(t):
    df = yf.download(f"{t}.JK", period="1y", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    return df

def hitung_rsi(s, p=14):
    d = s.diff(1)
    g = (d.where(d > 0, 0)).rolling(p).mean()
    l = (-d.where(d < 0, 0)).rolling(p).mean()
    return 100 - (100 / (1 + g/l))

def get_sentiment(t):
    q = urllib.parse.quote(f"{t} Indonesia stock IDX")
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en")
    if not feed.entries: return 50
    an = SentimentIntensityAnalyzer()
    score = sum(an.polarity_scores(e.title)['compound'] for e in feed.entries[:5])
    return (score/5)*50 + 50

if tombol:
    with st.spinner(f"AI menganalisis {ticker_input}..."):
        try:
            df = get_stock_data(ticker_input)
            if df.empty: st.error("Data tidak ditemukan."); st.stop()
            info = yf.Ticker(f"{ticker_input}.JK").info
            
            close = df['Close'].squeeze()
            ma20, ma50 = close.rolling(20).mean().iloc[-1], close.rolling(50).mean().iloc[-1]
            rsi = hitung_rsi(close).iloc[-1]
            harga = close.iloc[-1]
            
            s_t = 50
            if harga > ma20: s_t += 15
            if ma20 > ma50: s_t += 15
            if 40 < rsi < 70: s_t += 20
            elif rsi < 30: s_t += 10
            
            s_f = 50
            pe, pb = info.get('trailingPE', 0), info.get('priceToBook', 0)
            if 0 < pe < 15: s_f += 25
            elif 15 < pe < 25: s_f += 10
            if 0 < pb < 2: s_f += 25
            
            vol = df['Volume'].squeeze()
            obv = (np.sign(close.diff()) * vol).fillna(0).cumsum()
            slope = obv.iloc[-1] - obv.iloc[-20] if len(obv) > 20 else 0
            s_b = 50 + (30 if slope > 0 else 0) + (20 if close.iloc[-1] > close.iloc[-2] else 0)
            
            s_s = get_sentiment(ticker_input)
            skor = min(100, max(0, s_t*0.4 + s_f*0.3 + s_b*0.2 + s_s*0.1))
            
            cg, cs = st.columns([1, 2])
            with cg:
                fig = go.Figure(go.Indicator(mode="gauge+number", value=skor,
                    title={'text': "SKOR AKHIR"},
                    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "white"},
                        'steps': [{'range': [0,40], 'color': "#ff4b4b"},
                                  {'range': [40,65], 'color': "#ffa726"},
                                  {'range': [65,100], 'color': "#00c853"}]}))
                fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                st.plotly_chart(fig, use_container_width=True)
            with cs:
                st.markdown("### Kesimpulan AI")
                if skor >= 65: st.success(f"🔥 **BUY** — {ticker_input} sangat layak beli.")
                elif skor >= 40: st.warning(f"⚖️ **HOLD** — {ticker_input} belum ada sinyal kuat.")
                else: st.error(f"🚨 **SELL** — {ticker_input} sedang tertekan.")
                st.write(f"Harga: **Rp {harga:,.0f}** | PE: **{pe}** | PBV: **{pb}**")
            
            st.markdown("#### Rincian Skor")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Teknikal (40%)", f"{s_t:.0f}"); c2.metric("Fundamental (30%)", f"{s_f:.0f}")
            c3.metric("Bandarmology (20%)", f"{s_b:.0f}"); c4.metric("Sentimen (10%)", f"{s_s:.0f}")
        except Exception as e:
            st.error(f"Error: {e}")
