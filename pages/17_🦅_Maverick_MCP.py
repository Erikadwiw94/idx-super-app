import streamlit as st
import httpx
import json
from datetime import datetime

st.title("🦅 Maverick MCP (52 Tools)")
st.write("Menjalankan 52 *tools* dari server `maverick-mcp` (Port 8003).")
st.divider()

MAVERICK_URL = "http://localhost:8003/mcp"

def parse_sse(text):
    for line in reversed(text.split("\n")):
        if line.startswith("data:"):
            ds = line[5:].strip()
            if ds:
                try: return json.loads(ds)
                except: pass
    try: return json.loads(text)
    except: return {}

def get_session(client):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "st", "version": "1.0"}}}
    resp = client.post(MAVERICK_URL, json=init, headers=headers)
    sid = resp.headers.get("mcp-session-id")
    if sid:
        headers["Mcp-Session-Id"] = sid
        client.post(MAVERICK_URL, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=headers)
    return headers

if "mcp_tools" not in st.session_state: st.session_state.mcp_tools = []

if not st.session_state.mcp_tools:
    with st.spinner("Memuat 52 tools..."):
        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as c:
                h = get_session(c)
                r = c.post(MAVERICK_URL, json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, headers=h)
                p = parse_sse(r.text)
                if "result" in p and "tools" in p["result"]:
                    st.session_state.mcp_tools = p["result"]["tools"]
        except Exception as e:
            st.error(f"Gagal load tools: {e}")

tools = st.session_state.mcp_tools
if not tools:
    st.warning("Tools belum termuat. Klik tombol di bawah untuk coba lagi.")
    if st.button("🔄 Muat Ulang Tools"): st.rerun()
    st.stop()

col1, col2 = st.columns([3, 1.5])
with col1:
    tool_names = [t['name'] for t in tools]
    selected = st.selectbox("Pilih Tool:", tool_names)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan", type="primary", use_container_width=True)

st.divider()

if mulai:
    sel_tool = next(t for t in tools if t['name'] == selected)
    st.subheader(f"🛠️ {selected}")
    st.info(sel_tool.get('description', '-'))
    
    schema = sel_tool.get('inputSchema', {})
    props = schema.get('properties', {})
    required = schema.get('required', [])
    
    args = {}
    with st.form("tool_form"):
        if not props:
            st.write("*Tidak perlu parameter.*")
        for pname, pschema in props.items():
            is_req = pname in required
            label = f"{pname}{'*' if is_req else ''}"
            ptype = pschema.get('type')
            if not ptype and 'anyOf' in pschema: ptype = pschema['anyOf'][0].get('type')
            default = pschema.get('default', "")
            
            if 'date' in pname.lower():
                d = st.date_input(label, value=datetime.today() if is_req else None)
                if d: args[pname] = d.strftime('%Y-%m-%d')
            elif ptype == 'string':
                v = st.text_input(label, value=str(default) if default else "")
                if v: args[pname] = v
            elif ptype == 'integer':
                args[pname] = st.number_input(label, value=int(default) if default else 0, step=1)
            elif ptype == 'number':
                args[pname] = st.number_input(label, value=float(default) if default else 0.0)
            elif ptype == 'boolean':
                args[pname] = st.checkbox(label, value=bool(default))
            elif ptype == 'array':
                vs = st.text_input(label + " (koma):", value="")
                if vs: args[pname] = [x.strip() for x in vs.split(",")]
        
        submit = st.form_submit_button("🚀 Jalankan Tool", type="primary")
    
    if submit:
        with st.spinner(f"Menjalankan {selected}..."):
            try:
                with httpx.Client(timeout=120.0, follow_redirects=True) as c:
                    h = get_session(c)
                    payload = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": selected, "arguments": args}}
                    r = c.post(MAVERICK_URL, json=payload, headers=h)
                    p = parse_sse(r.text)
                    if "result" in p and "content" in p["result"]:
                        for item in p["result"]["content"]:
                            if item.get("type") == "text":
                                try: st.json(json.loads(item["text"]))
                                except: st.markdown(item["text"])
                    else: st.json(p)
            except Exception as e:
                st.error(f"Error: {e}")
