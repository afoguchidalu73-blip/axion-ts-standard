import streamlit as st
import json
from axion.kernel import analyze_drift

# --- PAGE CONFIG ---
st.set_page_config(page_title="AXION Firewall", page_icon="🛡️", layout="wide")

# --- CLEAN ENTERPRISE CSS ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; color: #ffffff; }
    .axion-logo {
        font-size: 5rem; font-weight: 800;
        background: linear-gradient(90deg, #00f5a0, #00d9f5);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: -10px;
    }
    .axion-tagline { color: #8b949e; font-size: 1.2rem; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button {
        width: 100%; background: linear-gradient(45deg, #ff4b4b, #ff7676);
        color: white; border: none; height: 3.5em; font-weight: bold; font-size: 1.2rem;
        border-radius: 12px; margin-top: 20px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stTextArea textarea { background-color: #161b22 !important; color: #00ff00 !important; font-family: 'Courier New', monospace !important; border: 1px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="axion-logo">AXION</div>', unsafe_allow_html=True)
st.markdown('<div class="axion-tagline">Causal Integrity Firewall | Enterprise Edition</div>', unsafe_allow_html=True)

st.divider()

# --- INPUT SECTION ---
# This creates a tab system: One for Files, one for Text. No more confusion.
tab1, tab2 = st.tabs(["📝 MANUAL TEXT ENTRY", "📁 FILE UPLOAD"])

current_data = None
baseline_data = None

with tab1:
    st.info("Paste your JSON traces below for an instant audit.")
    col1, col2 = st.columns(2)
    with col1:
        c_text = st.text_area("Live Trace JSON", height=200, placeholder='{"id": 1, "parents": []}')
    with col2:
        b_text = st.text_area("Baseline JSON", height=200, placeholder='{"id": 1, "parents": []}')
    
    if c_text and b_text:
        try:
            current_data = json.loads(c_text)
            baseline_data = json.loads(b_text)
        except: st.error("Invalid JSON format in text boxes.")

with tab2:
    st.warning("Upload .json files from your device.")
    col1, col2 = st.columns(2)
    with col1:
        f1 = st.file_uploader("Current Trace File", type="json")
    with col2:
        f2 = st.file_uploader("Baseline Trace File", type="json")
    if f1 and f2:
        current_data = json.load(f1)
        baseline_data = json.load(f2)

st.divider()

# --- THE BIG BUTTON ---
if st.button("RUN CAUSAL INTEGRITY AUDIT"):
    if current_data and baseline_data:
        try:
            result = analyze_drift(current_data, baseline_data)
            
            if result["status"] == "PASSED":
                st.balloons()
                st.success("### ✅ AUDIT PASSED: SYSTEM SECURE")
                st.write("No unauthorized causal deviations detected in the execution trace.")
            else:
                st.error("### ❌ BREACH DETECTED")
                st.write("#### Forensic Explanation:")
                st.info(f"**Threat Level:** High\n\n**Root Cause:** {result.get('cause')}")
                with st.expander("View Raw Discrepancies"):
                    st.json(result.get("details"))
        except Exception as e:
            st.error(f"Kernel Error: {e}")
    else:
        st.error("Missing Data: Please paste text or upload files before running the audit.")

st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.caption("AXION v1.2.1 • Built for Professional Integrity Monitoring")
  
