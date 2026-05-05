import streamlit as st
from governor import AxionGovernor
import json

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION v7.0 | Mission Control")

# --- MISSION TELEMETRY ---
snapshot = st.session_state.axion.get_state_snapshot()
with st.sidebar:
    st.metric("Ledger Balance", f"${snapshot['verified_balance']}")
    st.metric("System Role", str(snapshot['active_role']).upper())
    if st.button("RESET SYSTEM"):
        st.session_state.axion = AxionGovernor()
        st.rerun()

# --- MISSION INPUT ---
st.subheader("📋 Proposed Mission Plan")
default_plan = [
    {"type": "SET_LIMIT", "value": 5000, "role": "admin"},
    {"type": "TRANSFER", "amount": 2000, "note": "Safe transfer"},
    {"type": "TRANSFER", "amount": 4000, "note": "This should fail the audit"}
]
plan_input = st.text_area("Input Sequence (JSON List)", value=json.dumps(default_plan, indent=2), height=200)

if st.button("🚀 AUDIT & EXECUTE MISSION"):
    plan = json.loads(plan_input)
    
    # 1. ATOMIC AUDIT
    audit_result = st.session_state.axion.simulate_plan(plan)
    
    if audit_result["status"] == "BLOCK":
        st.error(f"❌ MISSION REJECTED at Step {audit_result['step_index']}: {audit_result['reason']}")
    else:
        st.success(f"✅ MISSION VALIDATED. Projected Balance: ${audit_result['projected_balance']}")
        
        # 2. SEQUENTIAL EXECUTION
        st.info("Executing confirmed mission...")
        for step in plan:
            st.session_state.axion.enforce(step)
        
        st.rerun()

# --- AUDIT TRAIL ---
if st.session_state.axion.history:
    st.divider()
    st.write("### 🧾 Confirmed Forensic History")
    st.table(st.session_state.axion.history)
  
