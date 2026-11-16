import streamlit as st
import asyncio, os, json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

st.set_page_config(page_title="Stock MCP Pro", page_icon="🏦", layout="wide")
st.title("🏦 Stock MCP Pro (Advanced)")
st.write("7 tools + Market Segmentation dari server stdio `stock_mcp`.")
st.divider()

STOCK_MCP_DIR = "/home/server/stock_mcp"
VENV_PYTHON = f"{STOCK_MCP_DIR}/venv/bin/python"

if not os.path.exists(VENV_PYTHON):
    st.error(f"Venv tidak ditemukan di {VENV_PYTHON}"); st.stop()

async def call_tool_async(tool_name, arguments):
    env = {**os.environ, "PYTHONPATH": STOCK_MCP_DIR}
    sp = StdioServerParameters(command=VENV_PYTHON, args=["-m", "src.mcp_server"], cwd=STOCK_MCP_DIR, env=env)
    async with stdio_client(sp) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await s.call_tool(tool_name, arguments)

def display(result):
    if hasattr(result, 'content') and result.content:
        for item in result.content:
            if hasattr(item, 'text'):
                try: st.json(json.loads(item.text))
                except: st.markdown(item.text)
            else: st.write(item)
    else: st.write(result)

col1, col2, col3 = st.columns([2, 2, 1.5])
with col1:
    tool = st.selectbox("Tool:", ["get_stock_price","get_technical_indicators","get_fundamentals","get_historical_data","get_market_movers","get_recommendation_history"])
with col2:
    ticker = st.text_input("Kode Saham:", value="BBCA").upper() if tool in ["get_stock_price","get_technical_indicators","get_fundamentals","get_historical_data"] else ""
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan", type="primary", use_container_width=True)

st.divider()

if mulai:
    with st.spinner(f"Memanggil `{tool}`..."):
        try:
            args = {"symbol": ticker} if ticker else {}
            result = asyncio.run(call_tool_async(tool, args))
            st.success(f"✅ `{tool}` berhasil!")
            display(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Pastikan `mcp<2` terinstall di venv stock_mcp dan web-gabungan.")
