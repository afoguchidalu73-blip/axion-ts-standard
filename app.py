import streamlit as st
from governor import AxionGovernor
import json

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION v7.2 | Hardened Autonomy")

# --- DETERMINISTIC PLANNER ---
def deterministic_planner(goal_text):
    try:
        # Extract numerical goal
        total_goal = int(''.join(filter(str.isdigit, goal_text)))
        plan = []
        remaining = total_goal
        chunk_size = 1000 
        
        while remaining > 0:
            amt = min(chunk_size, remaining)
            plan.append({"type": "TRANSFER", "amount": amt, "note": f"Atomic Step {len(plan)+1}"})
            remaining -= amt
        return plan, total_goal
    except:
        return None, 0

# --- UI CONTROLS ---
intent = st.text_input("Mission Goal:", value="Distribute 7000")

if st.button("🚀 EXECUTE MISSION"):
    # Ensure System context
    if st.session_state.axion.ledger["role"] is None:
        st.session_state.axion.enforce({"type": "SET_LIMIT", "value": 10000, "role": "admin"})
    
    plan, total_goal = deterministic_planner(intent)
    
    if plan:
        # Pass total_goal for strict sum-verification
        audit = st.session_state.axion.simulate_plan(plan, expected_total=total_goal)
        
        if audit["status"] == "VALIDATED":
            for step in plan:
                st.session_state.axion.enforce(step)
            st.success(f"✅ Mission Complete. Sum Verified: {total_goal}")
            st.rerun()
        else:
            st.error(f"❌ Audit Blocked Plan: {audit['reason']}")

st.markdown("---")
st.subheader("🧾 Immutable Forensic Ledger")
st.table(st.session_state.axion.history)
