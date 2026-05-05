import streamlit as st
import json
from axion.kernel import analyze_drift

# --- PAGE CONFIG ---
st.set_page_config(page_title="AXION-TS Firewall", page_icon="🛡️", layout="wide")

# --- HIGH-END BOLD CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #0b0e14; color: #ffffff; }
    
    /* Massive White Designed Logo with Shield */
    .axion-header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 5px;
    }
    
    .axion-logo {
        font-family: 'Inter', sans-serif;
        font-size: 6rem; 
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -5px;
        line-height: 0.8;
    }

    .shield-icon {
        font-size: 5rem;
    }
    
    /* Bolder Subheading with Full Name */
    .axion-full-name { 
        color: #ffffff; 
        font-size: 1.4rem; 
        font-weight: 800;
        margin-bottom: 40px; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }

    /* THE RED AUDIT BUTTON */
    .stButton>button {
        width: 100%; 
        background: linear-gradient(45deg, #d63031, #ff7675);
        color: white; 
        border: none; 
        height: 4em; 
        font-weight: 900; 
        font-size: 1.3rem;
        border-radius: 8px; 
        box-shadow: 0 4px 20px rgba(214, 48, 49, 0.4);
        transition: 0.3s;
        margin-top: 30px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #ff7675;
        transform: scale(1.01);
    }

    /* Input Areas */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #ffffff !important; 
        border: 1px solid #30363d !important; 
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="axion-header-container">
        <span class="shield-icon">🛡️</span>
        <div class="axion-logo">AXION-TS</div>
    </div>
    <div class="axion-full-name">AXION-TS DETERMINISTIC CAUSAL INTEGRITY PROTOCOL</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
tab1, tab2 = st.tabs(["📝 MANUAL TEXT ENTRY", "📁 FILE UPLOAD"])

current_data, baseline_data = None, None

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        c_text = st.text_area("LIVE EXECUTION TRACE (JSON)", height=250)
    with col2:
        b_text = st.text_area("BASELINE GOLD STANDARD (JSON)", height=250)
    
    if c_text and b_text:
        try:
            current_data = json.loads(c_text)
            baseline_data = json.loads(b_text)
        except: st.error("Format Error: Ensure JSON is correct.")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        f1 = st.file_uploader("Upload Trace", type="json")
    with col2:
        f2 = st.file_uploader("Upload Baseline", type="json")
    if f1 and f2:
        current_data = json.load(f1)
        baseline_data = json.load(f2)

# --- THE RED BUTTON ---
if st.button("EXECUTE SYSTEM AUDIT"):
    if current_data and baseline_data:
        try:
            result = analyze_drift(current_data, baseline_data)
            if result["status"] == "PASSED":
                st.success("### ✅ INTEGRITY VERIFIED")
                st.balloons()
            else:
                st.error("### 🚨 BREACH DETECTED")
                st.markdown(f"**Root Cause Analysis:** `{result.get('cause')}`")
                with st.expander("View Forensic Data"):
                    st.json(result.get("details"))
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please provide data before execution.")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("AXION-TS v1.4.3 • Enterprise Integrity Monitoring")
  
