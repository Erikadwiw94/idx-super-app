import streamlit as st
import feedparser
import urllib.parse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="News Sentiment", page_icon="📰", layout="wide")
st.title("📰 Sentiment AI (Berita Global & IDX)")
st.write("Analisis sentimen berita terbaru via Google News RSS & NLP.")
st.divider()

col1, col2, col3 = st.columns([3, 2, 1.5])
with col1:
    ticker_input = st.text_input("Kode Saham IDX (tanpa .JK):", value="BBCA").upper()
with col2:
    max_berita = st.slider("Jumlah Berita:", 5, 30, 15)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🔍 Analisis", type="primary", use_container_width=True)

st.divider()

if mulai:
    query = urllib.parse.quote(f"{ticker_input} Indonesia stock IDX")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    
    with st.spinner(f"Mencari berita {ticker_input}..."):
        analyzer = SentimentIntensityAnalyzer()
        feed = feedparser.parse(rss_url)
        berita = feed.entries[:max_berita]
        
        if not berita:
            st.warning(f"Tidak ada berita ditemukan untuk {ticker_input}.")
        else:
            st.success(f"✅ Ditemukan {len(berita)} berita")
            
            total, valid = 0, 0
            for item in berita:
                judul = item.title
                penerbit = item.source.title if hasattr(item, 'source') else "Google News"
                link = item.link
                
                skor = analyzer.polarity_scores(judul)
                compound = skor['compound']
                total += compound; valid += 1
                
                if compound >= 0.05: label = "🟢 POSITIF"
                elif compound <= -0.05: label = "🔴 NEGATIF"
                else: label = "⚪ NETRAL"
                
                with st.expander(f"{label} | {judul}"):
                    st.write(f"**Penerbit:** {penerbit}")
                    st.write(f"**Skor:** {compound:.3f}")
                    st.markdown(f"[Baca berita]({link})")
            
            st.divider()
            st.subheader("📊 Kesimpulan Pasar")
            if valid > 0:
                avg = total / valid
                if avg >= 0.1: st.success(f"**POSITIF** (Skor: {avg:.2f})")
                elif avg <= -0.1: st.error(f"**NEGATIF** (Skor: {avg:.2f})")
                else: st.info(f"**NETRAL** (Skor: {avg:.2f})")
