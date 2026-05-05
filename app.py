import streamlit as st
from governor import AxionGovernor

# --- PRO TERMINAL STYLING ---
st.set_page_config(page_title="AXION-TS Governor", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #05070a; color: #e0e0e0; font-family: monospace; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: 800; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# Persistent Governor Session
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Logic Governor")
st.caption("Stateful Runtime Enforcement v4.2")

# --- SIDEBAR TELEMETRY ---
st.sidebar.header("Verified Ledger")
st.sidebar.json(st.session_state.axion.ledger)
st.sidebar.divider()
st.sidebar.write("Current Chain Hash:")
st.sidebar.code(st.session_state.axion.chain_hash[:24] + "...")

# --- STEP 1: INITIALIZATION ---
with st.container(border=True):
    st.subheader("1. Define System Policy")
    c1, c2 = st.columns(2)
    with c1:
        u_limit = st.number_input("Authorized Limit ($)", value=5000)
    with c2:
        u_role = st.selectbox("Assign Identity Role", ["guest", "admin"])
    
    if st.button("COMMIT POLICY TO LEDGER"):
        res = st.session_state.axion.enforce({"type": "SET_LIMIT", "value": u_limit, "role": u_role})
        st.success(res.get("msg", "System Initialized"))

st.divider()

# --- STEP 2: EXECUTION ---
with st.container(border=True):
    st.subheader("2. Execute Autonomous Action")
    req_amount = st.number_input("Proposed Action Amount ($)", value=0)
    
    if st.button("RUN ENFORCEMENT AUDIT"):
        action = {"type": "TRANSFER", "amount": req_amount}
        outcome = st.session_state.axion.enforce(action)
        
        if outcome.get("status") == "BLOCK":
            st.error(f"🚨 {outcome.get('reason')}")
            st.toast("Logic Violation Detected", icon="❌")
        else:
            st.success(f"✅ {outcome.get('msg')}")
            st.info(f"Execution Token: {outcome.get('token')[:32]}...")
            st.balloons()

# --- AUDIT TRAIL ---
if st.session_state.axion.history:
    with st.expander("View Forensic Audit Trail"):
        st.write(st.session_state.axion.history)
  
