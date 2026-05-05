import streamlit as st
import json
from axion.kernel import analyze_drift

# --- PAGE CONFIG ---
st.set_page_config(page_title="AXION-TS", page_icon="🛡️", layout="wide")

# --- REFINED PRO CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #0b0e14; color: #ffffff; }
    
    /* Balanced Header */
    .header-box {
        display: flex;
        align-items: center;
        gap: 15px;
        padding-top: 10px;
    }
    
    .axion-logo {
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem; /* Scaled down for mobile sanity */
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
    }

    .shield-emoji {
        font-size: 2.2rem;
    }
    
    .axion-full-name { 
        color: #8b949e; 
        font-size: 0.85rem; 
        font-weight: 700;
        margin-top: -5px;
        margin-bottom: 30px; 
        text-transform: uppercase; 
        letter-spacing: 1.5px;
    }

    /* THE COMMAND RED BUTTON */
    .stButton>button {
        width: 100%; 
        background-color: #ff4b4b;
        color: white; 
        border: none; 
        height: 3.5em; 
        font-weight: 700; 
        font-size: 1rem;
        border-radius: 6px; 
        transition: 0.2s;
        margin-top: 20px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
    }

    /* Clean Input Areas */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #ffffff !important; 
        border: 1px solid #30363d !important; 
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="header-box">
        <div class="axion-logo">AXION-TS <span class="shield-emoji">🛡️</span></div>
    </div>
    <div class="axion-full-name">Deterministic Causal Integrity Protocol</div>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["📝 MANUAL ENTRY", "📁 FILE UPLOAD"])

current_data, baseline_data = None, None

with tab1:
    c_text = st.text_area("LIVE EXECUTION TRACE", height=180, placeholder="Paste JSON here...")
    b_text = st.text_area("BASELINE GOLD STANDARD", height=180, placeholder="Paste JSON here...")
    
    if c_text and b_text:
        try:
            current_data = json.loads(c_text)
            baseline_data = json.loads(b_text)
        except: st.error("Format Error: Ensure JSON syntax is correct.")

with tab2:
    f1 = st.file_uploader("Upload Live Trace", type="json")
    f2 = st.file_uploader("Upload Baseline", type="json")
    if f1 and f2:
        current_data = json.load(f1)
        baseline_data = json.load(f2)

# --- THE RED BUTTON ---
if st.button("EXECUTE SYSTEM AUDIT"):
    if current_data and baseline_data:
        try:
            result = analyze_drift(current_data, baseline_data)
            st.divider()
            if result["status"] == "PASSED":
                st.success("✅ INTEGRITY VERIFIED")
                st.balloons()
            else:
                st.error("🚨 BREACH DETECTED")
                st.markdown(f"**Root Cause Analysis:** `{result.get('cause')}`")
        except Exception as e:
            st.error(f"Audit Failed: {e}")
    else:
        st.warning("Please input data before running audit.")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("AXION-TS v1.5.0 • Enterprise Security")
          
