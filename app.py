import streamlit as st
from governor import AxionGovernor

# --- PRO UI CONFIG ---
st.set_page_config(page_title="AXION-TS Governor", page_icon="🛡️")

# Initialize the Governor in the background
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Logic Governor")
st.caption("Deterministic Runtime Enforcement Engine")

# --- AREA 1: CONSTRAINT SETTING ---
with st.container(border=True):
    st.subheader("Step 1: Set Deterministic Policy")
    user_limit = st.number_input("Maximum Authorized Spending ($)", value=1000)
    
    if st.button("LOCK POLICY"):
        policy_step = {"type": "SET_LIMIT", "value": user_limit}
        result = st.session_state.axion.enforce(policy_step)
        st.success(result["msg"])

st.divider()

# --- AREA 2: EXECUTION ---
with st.container(border=True):
    st.subheader("Step 2: Propose Autonomous Action")
    transfer_val = st.number_input("AI Proposed Transfer ($)", value=0)
    
    if st.button("EXECUTE ENFORCEMENT AUDIT"):
        action_step = {"type": "TRANSFER", "value": transfer_val}
        
        # The Governor Decides
        outcome = st.session_state.axion.enforce(action_step)
        
        if outcome["status"] == "BLOCK":
            st.error(f"🚨 {outcome['reason']}")
        else:
            st.success(f"✅ ACTION AUTHORIZED. Token: {outcome['token'][:16]}...")
            st.balloons()

# --- SIDEBAR: SYSTEM INTEGRITY ---
st.sidebar.header("System Telemetry")
st.sidebar.write("Current State Hash:")
st.sidebar.code(st.session_state.axion.chain_hash[:20] + "...")
st.sidebar.write("Verified Ledger:", st.session_state.axion.ledger)
      
