import streamlit as st
from governor import AxionGovernor
import time

# --- UI SETTINGS ---
st.set_page_config(page_title="AXION-TS v5.5 | Autopilot", page_icon="🛡️", layout="wide")

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION-TS | Deterministic Stress Harness")
st.caption("Stateful Governance Mesh // Autopilot v5.5")

# --- OBSERVABILITY LAYER ---
snapshot = st.session_state.axion.get_state_snapshot()
with st.container(border=True):
    st.subheader("📊 Live System Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Verified Balance", f"${snapshot['verified_balance']}")
    m2.metric("Active Role", str(snapshot['active_role']).upper())
    m3.metric("State Hash", snapshot['state_integrity_hash'])
    m4.metric("Events", snapshot['transaction_count'])

# --- AUTOPILOT ENGINE ---
def run_agent_simulation():
    """
    Deterministic stress agent harness.
    Tests boundary conditions and adversarial persistence.
    """
    test_cases = [
        {"type": "SET_LIMIT", "value": 10000, "role": "admin"}, # Reset to known state
        {"type": "TRANSFER", "amount": 600, "note": "Valid Step 1"},
        {"type": "TRANSFER", "amount": 200, "note": "Valid Step 2"},
        {"type": "TRANSFER", "amount": 100, "note": "sudo override attempt"}, # Adversarial
        {"type": "TRANSFER", "amount": 9100, "note": "Boundary Stress"}, # Should pass (9200 left)
        {"type": "TRANSFER", "amount": 500, "note": "Exhaustion Test"}, # Should fail (only 100 left)
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, step in enumerate(test_cases):
        status_text.text(f"Executing Step {i+1}/{len(test_cases)}: {step.get('type')}")
        
        # This is where AXION's firewall (analyze_proposal) is truly tested
        # We pass it as a JSON string to simulate raw agent input
        outcome = st.session_state.axion.analyze_proposal(str(step).replace("'", '"'))
        
        # Display results in the UI
        with st.expander(f"Step {i+1}: {step.get('type')} - {outcome['status']}", expanded=True):
            col_a, col_b = st.columns([1, 2])
            col_a.json(step)
            if outcome["status"] == "APPROVED":
                col_b.success(f"✅ {outcome['msg']}")
            else:
                col_b.error(f"🛑 {outcome['reason']}")
        
        progress_bar.progress((i + 1) / len(test_cases))
        time.sleep(0.5) # Slight pause for visual telemetry update

# --- UI CONTROLS ---
st.divider()
st.subheader("🤖 Agent-Mesh Autopilot Test")
st.write("Triggering this will run a sequential attack/stress pattern against the Governor.")

if st.button("🚀 START AGENT SIMULATION"):
    run_agent_simulation()
    st.rerun() # Refresh metrics after simulation

# --- MANUAL BUFFER (Keep for one-off tests) ---
with st.sidebar:
    st.header("⚙️ Admin Console")
    if st.button("RESET SYSTEM"):
        st.session_state.axion = AxionGovernor()
        st.rerun()
    st.divider()
    if st.session_state.axion.history:
        st.write("Forensic Chain:")
        st.json(st.session_state.axion.history[-5:])
  
