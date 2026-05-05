import streamlit as st
import json
from axion.kernel import analyze_drift

# --- PAGE CONFIG ---
st.set_page_config(page_title="AXION Firewall", page_icon="🛡️", layout="wide")

# --- PREMIUM DARK THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #0b0e14; color: #ffffff; }
    
    /* The Designed White Logo */
    .axion-logo {
        font-family: 'Inter', sans-serif;
        font-size: 5.5rem; 
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -4px;
        line-height: 1;
        margin-bottom: 5px;
    }
    
    .axion-tagline { 
        color: #636e72; 
        font-size: 1rem; 
        margin-bottom: 40px; 
        text-transform: uppercase; 
        letter-spacing: 5px; 
    }

    /* Executive Audit Button */
    .stButton>button {
        width: 100%; 
        background-color: #ffffff; 
        color: #000000; 
        border: none; 
        height: 3.5em; 
        font-weight: 800; 
        font-size: 1.1rem;
        border-radius: 4px; 
        transition: 0.3s;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background-color: #dfe6e9;
        transform: translateY(-2px);
    }

    /* Professional Input Boxes */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #ffffff !important; 
        border: 1px solid #30363d !important; 
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="axion-logo">AXION</div>', unsafe_allow_html=True)
st.markdown('<div class="axion-tagline">Causal Integrity Firewall</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
st.subheader("📊 System Analysis Input")
mode = st.tabs(["📝 MANUAL TEXT ENTRY", "📁 FILE UPLOAD"])

current_data = None
baseline_data = None

with mode[0]:
    col1, col2 = st.columns(2)
    with col1:
        c_text = st.text_area("Live Execution Trace (Paste JSON)", height=250, placeholder='{"id": 1, "parents": []}')
    with col2:
        b_text = st.text_area("Baseline Gold Standard (Paste JSON)", height=250, placeholder='{"id": 1, "parents": []}')
    
    if c_text and b_text:
        try:
            current_data = json.loads(c_text)
            baseline_data = json.loads(b_text)
        except Exception as e:
            st.error(f"JSON Format Error: {e}")

with mode[1]:
    col1, col2 = st.columns(2)
    with col1:
        f1 = st.file_uploader("Upload Current Trace", type="json")
    with col2:
        f2 = st.file_uploader("Upload Baseline Trace", type="json")
    if f1 and f2:
        current_data = json.load(f1)
        baseline_data = json.load(f2)

st.divider()

# --- THE AUDIT TRIGGER ---
if st.button("RUN SECURITY AUDIT"):
    if current_data and baseline_data:
        try:
            result = analyze_drift(current_data, baseline_data)
            
            if result["status"] == "PASSED":
                st.success("✅ INTEGRITY VERIFIED: No Causal Drift Detected.")
                st.balloons()
            else:
                st.error("🚨 CAUSAL BREACH DETECTED")
                st.markdown(f"**Root Cause Analysis:** `{result.get('cause')}`")
                with st.expander("Forensic Details"):
                    st.json(result.get("details"))
        except Exception as e:
            st.error(f"Execution Error: {e}")
    else:
        st.warning("Action Required: Please provide both Trace and Baseline data.")

# --- FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.caption("AXION v1.3 • Deterministic Security Framework")
          
