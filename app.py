import streamlit as st
from governor import AxionGovernor

# --- UI CONFIG ---
st.set_page_config(page_title="AXION-TS Governor", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #05070a; color: #e0e0e0; font-family: monospace; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: 800; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Logic Governor")
st.caption("Stateful Runtime Enforcement v4.2")

# --- SIDEBAR ---
st.sidebar.header("Verified Ledger")
st.sidebar.json(st.session_state.axion.ledger)
st.sidebar.divider()
st.sidebar.write("Current Chain Hash:")
st.sidebar.code(st.session_state.axion.chain_hash[:24] + "...")

# --- 1. INITIALIZATION ---
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

# --- 2. EXECUTION ---
with st.container(border=True):
    st.subheader("2. Execute Autonomous Action")
    req_amount = st.number_input("Proposed Action Amount ($)", value=0)
    
    if st.button("RUN ENFORCEMENT AUDIT"):
        action = {"type": "TRANSFER", "amount": req_amount}
        outcome = st.session_state.axion.enforce(action)
        
        if outcome.get("status") == "BLOCK":
            st.error(f"🚨 {outcome.get('reason')}")
        else:
            # Balloons removed from here
            st.success(f"✅ {outcome.get('msg')}")
            st.info(f"Execution Token: {outcome.get('token')[:32]}...")

# --- AUDIT TRAIL ---
if st.session_state.axion.history:
    with st.expander("View Forensic Audit Trail"):
        st.write(st.session_state.axion.history)

      # Add this at the bottom of your existing app.py

st.divider()
st.header("🤖 Agent-Mesh Sandbox")
st.caption("Testing AXION against simulated AI Agent outputs")

# This mimics an LLM generating a thought
ai_thought = st.text_area(
    "AI Agent Proposal (Raw JSON Output)", 
    value='{"type": "TRANSFER", "amount": 1500, "note": "Bypass for emergency"}'
)

if st.button("PROCESS AGENT PROPOSAL"):
    # The Governor acts as the firewall
    outcome = st.session_state.axion.analyze_proposal(ai_thought)
    
    if outcome.get("status") == "BLOCK":
        st.error(f"🛑 AXION INTERCEPTED: {outcome.get('reason')}")
    else:
        st.success(f"🛡️ AXION AUTHORIZED: {outcome.get('msg')}")
        st.info(f"Verification Token: {outcome.get('token')[:32]}...")
      
