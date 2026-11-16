import streamlit as st
import streamlit.components.v1 as components

# CSS: hilangkan padding & header, TAPI sidebar tetap ada
st.markdown("""
<style>
    /* === SEMBUNYIKAN HEADER STREAMLIT (toolbar atas) === */
    header[data-testid="stHeader"] { display: none !important; }

    /* === HILANGKAN PADDING DI AREA KANAN (main content) === */
    .block-container { 
        padding: 0 !important; 
        max-width: 100% !important; 
    }
    .main { padding: 0 !important; }
    [data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="element-container"] { margin: 0 !important; }

    /* === IFRAME MEMENUHI SELURUH AREA KANAN === */
    iframe {
        height: 100vh !important;
        width: 100% !important;
        border: none !important;
        display: block !important;
    }

    /* === HILANGKAN HEADER SIDEBAR (logo Streamlit di sidebar) === */
    [data-testid="stSidebarHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# URL BOZ
BOZ_URL = "http://172.19.175.140:21526"

# Render iframe — height di sini akan di-override oleh CSS 100vh
components.iframe(BOZ_URL, height=1080, scrolling=True)
