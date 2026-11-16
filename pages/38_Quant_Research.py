import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Quant Research", layout="wide")
st.title("🧮 Quant Research Platform")

IP_SERVER = "172.19.175.140" 
st.info("Pastikan aplikasi Quant Research sudah berjalan di port 8503.")
components.iframe(f"http://{IP_SERVER}:8503", height=1000, scrolling=True)
