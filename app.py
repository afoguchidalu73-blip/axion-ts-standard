import streamlit as st
import json
from axion.kernel import analyze_drift

# --- EXCLUSIVE UI CONFIG ---
st.set_page_config(page_title="AXION PRO", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #ff4b4b, #ff7676); color: white; border: none; height: 3em; font-weight: bold; border-radius: 8px; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AXION PRO")
st.markdown("#### *Causal Integrity Firewall | Enterprise Edition*")
st.divider()

col1, col2 = st.columns(2)
with col1:
    base_file = st.file_uploader("📥 Upload Baseline (Gold Standard)", type="json")
with col2:
    curr_file = st.file_uploader("📡 Upload Live Execution Trace", type="json")

if st.button("EXECUTE SYSTEM AUDIT"):
    if base_file and curr_file:
        try:
            # Logic from your kernel
            res = analyze_drift(json.load(curr_file), json.load(base_file))
            
            if res["status"] == "PASSED":
                st.balloons()
                st.success("### ✅ AUDIT PASSED: Integrity Verified")
                m1, m2 = st.columns(2)
                m1.metric("Security Score", "100%", delta="Optimal")
                m2.metric("Threats", "0", delta="Secure")
            else:
                st.error("### ❌ CAUSAL BREACH DETECTED")
                st.metric("Security Score", "CRITICAL", delta="-40%", delta_color="inverse")
                with st.expander("🔍 VIEW FORENSIC LOGS", expanded=True):
                    st.json(res)
        except Exception as e:
            st.error(f"Kernel Panic: {e}")
    else:
        st.warning("Awaiting data: Please upload both JSON traces.")
          
