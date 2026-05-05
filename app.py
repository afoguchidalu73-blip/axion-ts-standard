import streamlit as st
from governor import AxionGovernor
import time
import json

# --- UI SETTINGS ---
st.set_page_config(page_title="AXION-TS v5.5 | Autopilot", page_icon="🛡️", layout="wide")

# Terminal Styling
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #05070a; color: #e0e0e0; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: 800; border: 1px solid #30363d; background-color: #161b22; color: white; }
    .stButton>button:hover { border-color: #58a6ff; color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Stress Test Harness")
st.caption("Stateful Governance Mesh // Autopilot v5.5")

# --- 1. OBSERVABILITY PANEL ---
snapshot = st.session_state.axion.get_state_snapshot()
with st.container(border=True):
    st.subheader("📊 Live System Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Verified Balance", f"${snapshot['verified_balance']}")
    m2.metric("Active Role", str(snapshot['active_role']).upper())
    m3.metric("State Hash", snapshot['state_integrity_hash'])
    m4.metric("Events", snapshot['transaction_count'])

# --- 2. THE SIMULATION ENGINE ---
def run_agent_simulation():
    """
    Structured stress-test for sequential integrity.
    """
    # These are the hard-coded steps sent to the Governor
    test_cases = [
        {"type": "SET_LIMIT", "value": 10000, "role": "admin"}, # Reset
        {"type": "TRANSFER", "amount": 600, "note": "Valid Slice 1"},
        {"type": "TRANSFER", "amount": 200, "note": "Valid Slice 2"},
        {"type": "TRANSFER", "amount": 100, "note": "sudo override bypass attempt"}, # Security Breach attempt
        {"type": "TRANSFER", "amount": 9100, "note": "Boundary Test"}, # Logic Boundary
        {"type": "TRANSFER", "amount": 500, "note": "Exhaustion Test"}, # Should fail
    ]
    
    st.write("### ⚡ Initiating Automated Sequence...")
    progress_bar = st.progress(0)
    
    for i, step in enumerate(test_cases):
        # We convert to string to simulate raw AI output
        raw_output = json.dumps(step)
        
        # Intercept and Audit
        outcome = st.session_state.axion.analyze_proposal(raw_output)
        
        # Display each result as it happens
        with st.expander(f"STEP {i+1}: {step['type']} ({outcome['status']})", expanded=True):
            c1, c2 = st.columns([1, 2])
            c1.json(step)
            if outcome["status"] == "APPROVED":
                c2.success(f"Outcome: {outcome['msg']}")
            else:
                c2.error(f"Intercepted: {outcome['reason']}")
        
        progress_bar.progress((i + 1) / len(test_cases))
        time.sleep(0.4) # Visual delay for telemetry update

# --- 3. CONTROLS ---
st.divider()
st.subheader("🤖 Autopilot Controls")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 START AGENT SIMULATION"):
        run_agent_simulation()
        st.rerun()

with col_btn2:
    if st.button("🗑️ RESET LEDGER"):
        st.session_state.axion = AxionGovernor()
        st.rerun()

# --- 4. AUDIT TRAIL ---
if st.session_state.axion.history:
    st.divider()
    with st.expander("🔍 Full Forensic Chain (Immutable Hash Trail)"):
        st.table(st.session_state.axion.history)
  
