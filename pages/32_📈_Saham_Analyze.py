import streamlit as st
import streamlit.components.v1 as components

# CSS: fullscreen iframe, sidebar tetap (identik BOZ/IDX-UI)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .main { padding: 0 !important; }
    [data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="element-container"] { margin: 0 !important; }
    iframe {
        height: 100vh !important;
        width: 100% !important;
        border: none !important;
        display: block !important;
    }
    [data-testid="stSidebarHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# URL tanpa credential (Basic Auth sudah disabled)
SAHAM_URL = "http://172.19.175.140:8765"

components.iframe(SAHAM_URL, height=1080, scrolling=True)
