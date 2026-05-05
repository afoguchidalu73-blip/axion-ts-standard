import streamlit as st
import json
from axion.kernel import analyze_drift

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AXION Firewall",
    page_icon="🛡️",
    layout="wide"
)

# --- ADVANCED CSS (THE BEST OF BOTH) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=JetBrains+Mono&display=swap');

html, body, [class*="css"] {
    background-color: #0e1117;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
}

/* The AXION Logo Header */
.axion-title {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(90deg, #00f5a0 0%, #00d9f5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

.axion-sub {
    color: #8b949e;
    font-size: 1.1rem;
    font-weight: 400;
    margin-bottom: 30px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Pro Card Design */
.card {
    background: #161b22;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #30363d;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-top: 20px;
}

/* Status Indicators */
.pass { color: #3fb950; font-weight: 800; font-size: 1.8rem; border-left: 5px solid #3fb950; padding-left: 15px; }
.fail { color: #f85149; font-weight: 800; font-size: 1.8rem; border-left: 5px solid #f85149; padding-left: 15px; }

/* Code/JSON Areas */
code { font-family: 'JetBrains Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="axion-title">AXION</div>', unsafe_allow_html=True)
st.markdown('<div class="axion-sub">Deterministic Causal Integrity Protocol • v1.1</div>', unsafe_allow_html=True)

# --- SELECTION MODE ---
mode = st.radio("Select Audit Method:", ["📁 File Upload", "📝 Manual Text Entry"], horizontal=True)

st.divider()

current_data = None
baseline_data = None

# --- DUAL-MODE INPUT LOGIC ---
if mode == "📁 File Upload":
    col1, col2 = st.columns(2)
    with col1:
        c_file = st.file_uploader("Upload Current Trace", type="json")
        if c_file: current_data = json.load(c_file)
    with col2:
        b_file = st.file_uploader("Upload Baseline Trace", type="json")
        if b_file: baseline_data = json.load(b_file)

else:
    col1, col2 = st.columns(2)
    with col1:
        c_text = st.text_area("Paste Current JSON Trace", height=200, placeholder='{"action": "exec"}')
        if c_text: current_data = json.loads(c_text)
    with col2:
        b_text = st.text_area("Paste Baseline JSON Trace", height=200, placeholder='{"action": "exec"}')
        if b_text: baseline_data = json.loads(b_text)

# --- EXECUTION ---
if current_data and baseline_data:
    if st.button("EXECUTE INTEGRITY AUDIT"):
        try:
            result = analyze_drift(current_data, baseline_data)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            if result["status"] == "PASSED":
                st.markdown('<div class="pass">🛡️ SYSTEM SECURE: INTEGRITY VERIFIED</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown('<div class="fail">🚨 BREACH DETECTED: CAUSAL DRIFT</div>', unsafe_allow_html=True)
                
                st.write("### 🔍 Forensic Trace")
                st.code(result.get("cause", "Unknown Origin"))
                
                if "details" in result:
                    with st.expander("Show Edge Differences"):
                        st.json(result["details"])
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Kernel Fault: {e}")
else:
    st.info("Awaiting system traces for analysis...")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Authorized access only. All audits are logged and deterministic.")
  
