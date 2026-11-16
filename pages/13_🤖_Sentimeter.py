import streamlit as st
import httpx
import pandas as pd

st.title("🤖 Sentimeter (AI Sentiment & Recommendation)")
st.write("Analisis berita dan rekomendasi saham dari server lokal `sentimeter` (Port 3001).")
st.divider()

API_URL = "http://localhost:3001"

def fetch_api(ep, method="GET", json_data=None):
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.get(f"{API_URL}{ep}") if method == "GET" else client.post(f"{API_URL}{ep}", json=json_data)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        st.error(f"Gagal ke API ({ep}): {e}")
        return None

col1, col2, col3 = st.columns([2, 2, 1.5])
with col1:
    ticker_input = st.text_input("Kode Saham (tanpa .JK):", value="BBCA").upper()
with col2:
    aksi = st.selectbox("Jenis Analisis:", ["Analisis Ticker", "Market Outlook", "Rekomendasi"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Analisis", type="primary", use_container_width=True)

st.divider()

if mulai:
    if aksi == "Analisis Ticker":
        with st.spinner(f"Menganalisis {ticker_input}..."):
            res = fetch_api("/api/analyze-ticker", method="POST", json_data={"ticker": ticker_input})
            if res and res.get("success") and "data" in res:
                data = res["data"]
                st.markdown(f"### 🏢 {data.get('companyName', ticker_input)}")
                st.caption(f"Sektor: {data.get('sector', 'N/A')}")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Harga", f"Rp {data.get('currentPrice', 0):,.0f}", f"{data.get('priceChangePct', 0):.2f}%")
                c2.metric("Trend", data.get('technical', {}).get('trend', 'N/A'))
                c3.metric("Volatilitas", f"{data.get('technical', {}).get('volatilityPercent', 0):.2f}%")
                st.divider()
                
                cf, ct = st.columns(2)
                with cf:
                    st.markdown("#### 📊 Fundamental")
                    fund = data.get('fundamentals', {})
                    st.write(f"**PE:** {fund.get('peRatio', 'N/A')}")
                    st.write(f"**ROE:** {fund.get('roe', 'N/A')}")
                    st.write(f"**Div Yield:** {fund.get('dividendYield', 'N/A')}")
                with ct:
                    st.markdown("#### 📈 Teknikal")
                    tech = data.get('technical', {})
                    st.write(f"**SMA 20:** Rp {tech.get('sma20', 0):,.0f}")
                    st.write(f"**SMA 50:** Rp {tech.get('sma50', 0):,.0f}")
                    st.write(f"**Support:** {', '.join(map(str, tech.get('supports', [])))}")
                    st.write(f"**Resistance:** {', '.join(map(str, tech.get('resistances', [])))}")
                if data.get("analysis"):
                    st.info(f"**Kesimpulan AI:** {data['analysis']}")
            elif res:
                st.json(res)
    
    elif aksi == "Market Outlook":
        with st.spinner("Mengambil market outlook..."):
            data = fetch_api("/api/market-outlook")
            if data:
                if "ERROR" in data or "error" in data:
                    st.warning("⚠️ Fitur ini sedang bermasalah di backend.")
                    st.json(data)
                elif "data" in data: st.json(data["data"])
                else: st.json(data)
    
    else:
        with st.spinner("Mengambil rekomendasi..."):
            res = fetch_api("/api/recommendations")
            if res and "data" in res:
                data = res["data"]
                recs = data.get("recommendations", [])
                if not recs:
                    st.warning("Belum ada rekomendasi hari ini.")
                else:
                    st.dataframe(pd.DataFrame(recs), use_container_width=True)
