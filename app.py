import streamlit as st
from governor import AxionGovernor

# --- UI SETTINGS ---
st.set_page_config(page_title="AXION-TS v5.1", page_icon="🛡️", layout="wide")

# Custom Terminal Theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #05070a; color: #e0e0e0; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: 800; border: 1px solid #30363d; background-color: #161b22; color: white; }
    .stButton>button:hover { border-color: #58a6ff; color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# Persistent Governor Instance
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Gateway & Telemetry")
st.caption("Stateful Governance Mesh // Enforcement Kernel v5.1")

# --- 1. OBSERVABILITY LAYER (Snapshot) ---
snapshot = st.session_state.axion.get_state_snapshot()

with st.container(border=True):
    st.subheader("📊 Live System Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Verified Balance", f"${snapshot['verified_balance']}")
    m2.metric("Active Role", str(snapshot['active_role']).upper())
    m3.metric("State Integrity", snapshot['state_integrity_hash'])
    m4.metric("Events", snapshot['transaction_count'])

st.divider()

# --- 2. ENFORCEMENT LAYER (Agent Mesh) ---
st.subheader("🤖 Agent-Mesh Proposal Buffer")
st.write("Intercept and audit autonomous AI proposals here.")

default_json = '{"type": "TRANSFER", "amount": 500, "note": "Valid transaction"}'
ai_input = st.text_area("RAW AGENT OUTPUT (JSON)", value=default_json, height=120)

if st.button("RUN ENFORCEMENT AUDIT"):
    outcome = st.session_state.axion.analyze_proposal(ai_input)
    
    if outcome["status"] == "BLOCK":
        st.error(f"🛑 INTERCEPTED: {outcome['reason']}")
    else:
        st.success(f"✅ AUTHORIZED: {outcome['msg']}")
        st.info(f"Forensic Token: {outcome['token'][:32]}...")

# --- 3. CONFIGURATION & AUDIT (Sidebar/Expander) ---
with st.sidebar:
    st.header("⚙️ Admin Console")
    u_limit = st.number_input("Set Initial Balance", value=5000)
    u_role = st.selectbox("Define Role", ["guest", "admin"])
    if st.button("LOCK SYSTEM STATE"):
        st.session_state.axion.enforce({"type": "SET_LIMIT", "value": u_limit, "role": u_role})
        st.rerun()

if st.session_state.axion.history:
    with st.expander("🔍 Forensic Audit Trail"):
        st.table(st.session_state.axion.history)
      
