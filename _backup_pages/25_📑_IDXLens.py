import streamlit as st
import subprocess, os, json, re
import pandas as pd

st.set_page_config(page_title="IDXLens", page_icon="📑", layout="wide")
st.title("📑 IDXLens (Laporan Keuangan IDX)")
st.write("Ekstrak laporan keuangan langsung dari portal IDX.")
st.divider()

IDXLENS_DIR = "/home/server/idxlens"
IDXLENS_BIN = f"{IDXLENS_DIR}/bin/idxlens"
ENV = os.environ.copy()
ENV["CHROME_PATH"] = "/snap/bin/chromium"

def camel_to_readable(s):
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    return s.replace("TextBlock", "").strip()

def format_idr(v, d=""):
    if v == 0 or v is None: return "-"
    try:
        val = float(v)
        di = int(d) if d else 0
        actual = val * (10 ** (-di)) if di < 0 else val
        if abs(actual) >= 1e12: return f"Rp {actual/1e12:.2f} T"
        elif abs(actual) >= 1e9: return f"Rp {actual/1e9:.2f} M"
        elif abs(actual) >= 1e6: return f"Rp {actual/1e6:.2f} Jt"
        return f"Rp {actual:,.0f}"
    except: return str(v)

def parse_facts(data):
    bc, bp, ic, ip, meta = {}, {}, {}, {}, {}
    for f in data.get("facts", []):
        c = f.get("concept", ""); v = f.get("value", 0); p = f.get("period", ""); d = f.get("decimals", "")
        if "_" in p: continue
        if c.startswith("idx-dei:"):
            k = c.replace("idx-dei:", "")
            if v != 0: meta[k] = v
        elif c.startswith("idx-cor:"):
            k = c.replace("idx-cor:", "")
            if "Instant" in p:
                if "PriorEndYear" in p: bp[k] = (v, d)
                elif "CurrentYear" in p: bc[k] = (v, d)
            elif "Duration" in p:
                if "PriorYear" in p: ip[k] = (v, d)
                elif "CurrentYear" in p: ic[k] = (v, d)
    return bc, bp, ic, ip, meta

# Form tengah
col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.5])
with col1: ticker = st.text_input("Kode Saham:", value="BBCA").upper()
with col2: tahun = st.number_input("Tahun:", 2010, 2026, 2026)
with col3: periode = st.selectbox("Periode:", ["FY", "Q1", "Q2", "Q3"])
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🔬 Ekstrak", type="primary", use_container_width=True)

st.divider()

if mulai:
    with st.spinner(f"Mengekstrak {ticker} {periode} {tahun}..."):
        try:
            r = subprocess.run([IDXLENS_BIN, "analyze", ticker, "--year", str(tahun)],
                cwd=IDXLENS_DIR, capture_output=True, text=True, timeout=300, env=ENV)
            
            out = r.stdout.strip()
            js, je = out.find('{'), out.rfind('}') + 1
            if js == -1 or je == 0:
                st.error("Data JSON tidak ditemukan.")
                st.code(out[-2000:])
                st.stop()
            
            data = json.loads(out[js:je])
            st.success(f"✅ Berhasil mengekstrak {ticker}")
            
            bc, bp, ic, ip, meta = parse_facts(data)
            
            st.markdown(f"### 🏢 {meta.get('EntityName', ticker)}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sektor", meta.get('Sector', '-'))
            c2.metric("Industri", meta.get('Industry', '-'))
            c3.metric("Sub-Sektor", meta.get('Subsector', '-'))
            c4.metric("Entitas", meta.get('TypeOfEntity', '-'))
            
            st.divider()
            
            def g(d, k):
                v, dd = d.get(k, (0, ""))
                try:
                    di = int(dd) if dd else 0
                    return float(v) * (10 ** (-di)) if di < 0 else float(v)
                except: return 0
            
            as_cur, as_prev = g(bc, "Assets"), g(bp, "Assets")
            li = g(bc, "Liabilities"); eq = g(bc, "Equity")
            pr_cur, pr_prev = g(ic, "ProfitLoss"), g(ip, "ProfitLoss")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Aset", format_idr(as_cur, "-6"), f"{((as_cur-as_prev)/as_prev*100):+.1f}%" if as_prev else None)
            c2.metric("Total Liabilitas", format_idr(li, "-6"))
            c3.metric("Total Ekuitas", format_idr(eq, "-6"))
            c4.metric("Laba Bersih", format_idr(pr_cur, "-6"), f"{((pr_cur-pr_prev)/pr_prev*100):+.1f}%" if pr_prev else None)
            
            st.divider()
            st.markdown("### 📋 Laporan Keuangan")
            t1, t2 = st.tabs(["📊 Neraca", "💰 Laba Rugi"])
            
            def build_df(cur, pri, keys):
                rows = []
                for k in keys:
                    if k in cur or k in pri:
                        cv, cd = cur.get(k, (0, ""))
                        pv, pd_ = pri.get(k, (0, ""))
                        gr = f"{((cv-pv)/abs(pv)*100):+.2f}%" if pv and pv != 0 else "-"
                        rows.append({"Item": camel_to_readable(k), "Tahun Ini": format_idr(cv, cd), "Tahun Lalu": format_idr(pv, pd_), "Pertumbuhan": gr})
                return pd.DataFrame(rows)
            
            with t1:
                df_b = build_df(bc, bp, ["Assets","Cash","LoansThirdParties","GovernmentBonds","Liabilities","CurrentAccountsThirdParties","SavingsThirdParties","TimeDepositsThirdParties","Equity","CommonStocks","UnappropriatedRetainedEarnings"])
                st.dataframe(df_b, use_container_width=True, hide_index=True)
            with t2:
                df_i = build_df(ic, ip, ["InterestIncome","InterestExpenses","ProfitFromOperation","ProfitLossBeforeIncomeTax","TaxBenefitExpenses","ProfitLoss","BasicEarningsLossPerShareFromContinuingOperations"])
                st.dataframe(df_i, use_container_width=True, hide_index=True)
            
            st.download_button("📥 Download JSON Lengkap", out[js:je], f"{ticker}_{tahun}_xbrl.json", "application/json")
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
