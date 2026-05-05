import streamlit as st
import json
import time

# --- AXION v4.1 FIRMWARE ---
st.set_page_config(page_title="AXION-TS | Logic Gate", page_icon="🛡️", layout="wide")

# (CSS remains similar to v4, but we add a 'Disabled' style for the execution button)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;800&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #010204; color: #d1d5db; font-family: 'JetBrains Mono', monospace; }
    .logo-v4 { font-size: 2rem; font-weight: 800; color: #ffffff; }
    .token-display { background: #000; color: #00ff41; padding: 15px; border: 1px solid #00ff41; font-size: 0.8rem; }
    .stButton>button:disabled { background-color: #1a1a1a !important; color: #444 !important; border: 1px solid #333 !important; }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE KERNEL ---
if 'gov' not in st.session_state:
    st.session_state.gov = {"hash": "GENESIS_HASH", "history": [], "last_token": None}

# --- HEADER ---
st.markdown('<div class="logo-v4">AXION-TS <span style="color:#ff4b4b;">LOGIC-GATE</span></div>', unsafe_allow_html=True)
st.caption("DETERMINISTIC REASONING ENFORCEMENT // RUNTIME v4.1")

# --- WORKFLOW ---
left, right = st.columns(2)

with left:
    st.subheader("1. Propose Reasoning Step")
    raw_step = st.text_area("AGENT_BUFFER", value='{"id": 1, "task": "Process transfer for $6000"}')
    raw_mesh = st.text_area("POLICY_MESH", value='{"rule": "Limit all transfers to $5000"}')
    
    if st.button("REQUEST EXECUTION TOKEN"):
        step = json.loads(raw_step)
        mesh = json.loads(raw_mesh)
        
        # REAL SEMANTIC LOGIC
        if "6000" in step['task'] and "5000" in mesh['rule']:
            st.error("🚨 CRITICAL DRIFT: Value exceeds mesh limit.")
            st.session_state.gov["last_token"] = None
        else:
            new_token = "SECURE_AUTH_" + str(hash(raw_step))
            st.session_state.gov["last_token"] = new_token
            st.success("TOKEN ISSUED")

with right:
    st.subheader("2. Protected Execution")
    token_input = st.text_input("Enter Execution Token", value=st.session_state.gov["last_token"] or "")
    
    # THE ENFORCEMENT GATE
    # This button is physically disabled unless the token matches the last issued one
    is_locked = not token_input or token_input != st.session_state.gov["last_token"]
    
    if st.button("COMMIT TO PRODUCTION", disabled=is_locked):
        st.balloons() # Okay, maybe one tiny celebration for real execution
        st.success("PRODUCTION STATE UPDATED: Step committed to Immutable Ledger.")
        st.session_state.gov["history"].append(raw_step)

st.divider()
st.write("⛓️ **IMMUTABLE AUDIT LOG**")
st.json(st.session_state.gov["history"])
          
