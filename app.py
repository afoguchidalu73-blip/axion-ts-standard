import streamlit as st
from governor import AxionGovernor
import json

# Initialize Session
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION v7.1 | Goal Decomposition")

# --- 1. THE PLANNER (DECOMPOSITION) ---
def build_plan_without_guessing(goal_text):
    """
    Deterministic Planner: Converts Intent to auditable JSON.
    """
    if "distribute" in goal_text.lower():
        try:
            total = int(''.join(filter(str.isdigit, goal_text)))
            # Split into 3 logical chunks
            chunk = total // 3
            return [
                {"type": "TRANSFER", "amount": chunk, "note": "Dist. Phase 1"},
                {"type": "TRANSFER", "amount": chunk, "note": "Dist. Phase 2"},
                {"type": "TRANSFER", "amount": chunk, "note": "Dist. Phase 3"}
            ]
        except:
            return None
    return None

# --- 2. TELEMETRY ---
snap = st.session_state.axion.get_state_snapshot()
st.sidebar.metric("Ledger", f"${snap['verified_balance']}")
st.sidebar.metric("Context", snap['active_role'])

# --- 3. UI INTERFACE ---
st.subheader("🧠 Mission Intent")
intent = st.text_input("Enter Goal:", value="Distribute 3000")

if st.button("EXECUTE MISSION"):
    # Simulated Role setup for this test
    if st.session_state.axion.ledger["role"] is None:
        st.session_state.axion.enforce({"type": "SET_LIMIT", "value": 10000, "role": "admin"})
    
    plan = build_plan_without_guessing(intent)
    
    if plan:
        # Pre-Execution Audit
        audit = st.session_state.axion.simulate_plan(plan)
        
        if audit["status"] == "VALIDATED":
            st.success(f"Plan Validated. Final Balance will be ${audit['projected_balance']}")
            for step in plan:
                st.session_state.axion.enforce(step)
            st.rerun()
        else:
            st.error(f"Audit Blocked Plan: {audit['reason']}")

# Use Markdown instead of st.divider() to avoid the NameError
st.markdown("---")
st.subheader("🧾 Forensic Audit Trace")
st.table(st.session_state.axion.history)
          
