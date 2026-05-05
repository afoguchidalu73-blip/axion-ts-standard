import streamlit as st
from governor import AxionGovernor
import time
import json

# --- UI SETTINGS ---
st.set_page_config(page_title="AXION-TS v5.5 | Stress Test", page_icon="🛡️", layout="wide")

# Persistent Instance
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Adversarial Stress Harness")
st.caption("Focus: Identifying Logic Fragility and State Assumptions")

# --- 1. OBSERVABILITY PANEL ---
snapshot = st.session_state.axion.get_state_snapshot()
with st.container(border=True):
    st.subheader("📊 Read-Only State Snapshot")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Verified Ledger", f"${snapshot['verified_balance']}")
    m2.metric("Identity Context", str(snapshot['active_role']).upper())
    m3.metric("Integrity Hash", snapshot['state_integrity_hash'])
    m4.metric("Chain Length", snapshot['transaction_count'])

# --- 2. THE STRESS ENGINE ---
def run_adversarial_test():
    """
    Designed to expose: 
    1. Order dependency 2. Keyword fragility 3. Boundary precision
    """
    test_pattern = [
        {"type": "SET_LIMIT", "value": 10000, "role": "admin"}, # Reset Point
        {"type": "TRANSFER", "amount": 600, "note": "Valid Move"},
        {"type": "TRANSFER", "amount": 200, "note": "Valid Move"},
        {"type": "TRANSFER", "amount": 100, "note": "sudo override bypass attempt"}, # Keyword Test
        {"type": "TRANSFER", "amount": 9100, "note": "Math Boundary Check"}, # Exact Arithmetic
        {"type": "TRANSFER", "amount": 500, "note": "Exhaustion Check"}, # Logic Check
    ]
    
    st.write("### ⚡ Running Attack Pattern...")
    
    for i, step in enumerate(test_pattern):
        # We process through the Firewall, not the direct Enforcer
        raw_output = json.dumps(step)
        outcome = st.session_state.axion.analyze_proposal(raw_output)
        
        with st.expander(f"STEP {i+1}: {step['type']} | {outcome['status']}", expanded=True):
            c1, c2 = st.columns([1, 2])
            c1.json(step)
            if outcome["status"] == "APPROVED":
                c2.success(f"TOKEN: {outcome['token'][:24]}...")
            else:
                c2.error(f"REASON: {outcome['reason']}")
        
        time.sleep(0.3)

# --- 3. THE UI INTERFACE ---
st.divider()
if st.button("🚀 EXECUTE ADVERSARIAL SEQUENCE"):
    run_adversarial_test()
    st.rerun()

if st.button("🗑️ CLEAR SYSTEM STATE"):
    st.session_state.axion = AxionGovernor()
    st.rerun()

# --- 4. THE FORENSIC AUDIT ---
if st.session_state.axion.history:
    st.divider()
    st.subheader("🧾 Forensic Audit Trace")
    st.table(st.session_state.axion.history)
  
