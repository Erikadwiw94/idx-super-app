import streamlit as st

st.set_page_config(
    page_title="IDX Super Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { padding-top: 1rem; }
    [data-testid="stSidebarNav"] > div:first-child { display: none; }
    .main { background-color: #0e1117; }
</style>
""", unsafe_allow_html=True)

pages = {
    "🏠 Utama": [
        st.Page("pages/00_🏠_Home.py", title="Home", icon="🏠", default=True),
    ],
    "📊 Analisis Saham": [
        st.Page("pages/01_📊_Screener.py", title="Screener", icon="📊"),
        st.Page("pages/02_⚡_Ultimate_Analyzer.py", title="Ultimate Analyzer", icon="⚡"),
        st.Page("pages/03_📉_Pro_Technical.py", title="Pro Technical", icon="📉"),
        st.Page("pages/04_🔢_Dashboard_Angka.py", title="Dashboard Angka", icon="🔢"),
        st.Page("pages/05_📈_Multi_Stock.py", title="Multi Stock", icon="📈"),
    ],
    "🕵️ Bandarmology": [
        st.Page("pages/06_🕵️_Bandar_OBV.py", title="Bandar OBV", icon="🕵️"),
        st.Page("pages/07_🕵️_Bandar_Simulasi.py", title="Bandar Simulasi", icon="🕵️"),
        st.Page("pages/08_🕵️_Bandar_Accumulation.py", title="Bandar Accumulation", icon="🕵️"),
        st.Page("pages/09_💰_Broker_Summary.py", title="Broker Summary", icon="💰"),
    ],
    "⚙️ Backtest": [
        st.Page("pages/10_⚙️_Backtest_MA.py", title="Backtest MA", icon="⚙️"),
        st.Page("pages/11_⚙️_Backtest_Wyckoff.py", title="Backtest Wyckoff", icon="⚙️"),
    ],
    "📰 Berita & Sentimen": [
        st.Page("pages/12_📰_News_Sentiment.py", title="News Sentiment", icon="📰"),
        st.Page("pages/13_🤖_Sentimeter.py", title="Sentimeter", icon="🤖"),
        st.Page("pages/14_📰_Auto_News.py", title="Auto News", icon="📰"),
    ],
    "🤖 AI & ML": [
        st.Page("pages/15_🧠_StockAI.py", title="StockAI", icon="🧠"),
        st.Page("pages/16_🤖_AI_Saham.py", title="AI Saham", icon="🤖"),
        st.Page("pages/17_🦅_Maverick_MCP.py", title="Maverick MCP", icon="🦅"),
        st.Page("pages/18_🏦_Stock_MCP_Pro.py", title="Stock MCP Pro", icon="🏦"),
        st.Page("pages/19_🚀_Pulse_CLI.py", title="Pulse CLI", icon="🚀"),
    ],
    "📡 Data & API": [
        st.Page("pages/20_⚡_Live_Price.py", title="Live Price", icon="⚡"),
        st.Page("pages/21_🏦_IDX_SDK.py", title="IDX SDK", icon="🏦"),
        st.Page("pages/22_💰_Bursarium.py", title="Bursarium", icon="💰"),
        st.Page("pages/23_🏦_IDX_API.py", title="IDX API", icon="🏦"),
        st.Page("pages/24_📋_Indeks_Konstituen.py", title="Indeks Konstituen", icon="📋"),
        st.Page("pages/25_📑_IDXLens.py", title="IDXLens", icon="📑"),
        st.Page("pages/26_📊_Indo_Scraper.py", title="Indo Scraper", icon="📊"),
        st.Page("pages/27_📥_Bulk_Download.py", title="Bulk Download", icon="📥"),
    ],
    "🌐 Aplikasi Embed": [
        st.Page("pages/28_🚀_BOZ_NextJS.py", title="BOZ NextJS", icon="🚀"),
        st.Page("pages/29_💎_IDX_UI.py", title="IDX UI", icon="💎"),
        st.Page("pages/30_📊_Fundamental_UI.py", title="Fundamental UI", icon="📊"),
        st.Page("pages/31_📊_Stock_Analyst.py", title="Stock Analyst", icon="📊"),
        st.Page("pages/32_📈_Saham_Analyze.py", title="Saham Analyze", icon="📈"),
        st.Page("pages/33_🖥️_Stocks_Dashboard.py", title="Stocks Dashboard", icon="🖥️"),
    ],
    "🎯 Trading & Sistem": [
        st.Page("pages/34_🎯_Saftrade.py", title="Saftrade", icon="🎯"),
        st.Page("pages/35_🏢_Project_Hub.py", title="Project Hub", icon="🏢"),
        st.Page("pages/36_✅_System_Health_Check.py", title="System Health Check", icon="✅"),
    ],
}

pg = st.navigation(pages)
pg.run()
