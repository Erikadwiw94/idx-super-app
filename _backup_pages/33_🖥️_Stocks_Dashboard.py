import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Stocks Dashboard IDX",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: fullscreen iframe, sidebar tetap (identik BOZ/IDX-UI/SAHAM)
st.markdown("""
<style>
    /* Sembunyikan header Streamlit */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }

    /* Hilangkan padding di area kanan */
    .block-container { 
        padding: 0 !important; 
        max-width: 100% !important; 
    }
    .main { padding: 0 !important; }
    [data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="element-container"] { margin: 0 !important; }

    /* Iframe full screen */
    iframe {
        height: 100vh !important;
        width: 100% !important;
        border: none !important;
        display: block !important;
    }

    /* Sembunyikan header sidebar */
    [data-testid="stSidebarHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# URL Stocks Dashboard (Next.js, port 3100)
STOCKS_URL = "http://172.19.175.140:3100"

# Render iframe full-screen
components.iframe(STOCKS_URL, height=1080, scrolling=True)
