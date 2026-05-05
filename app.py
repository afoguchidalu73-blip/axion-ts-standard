import streamlit as st
from governor import AxionGovernor
import json

# Persistence
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.set_page_config(page_title="AXION v8.0 | Operational Autonomy", layout="wide")
st.title("🛡️ AXION v8.0 | Deterministic Control Plane")

# --- 1. INFORMED PLANNER (PHASE 4) ---
def informed_planner(goal_text):
    """
    Checks constraints BEFORE building the plan to ensure zero-failure convergence.
    """
    try:
        total_goal = int(''.join(filter(str.isdigit, goal_text)))
        
        # SIGHT: Get current rules from the Governor
        limits = st.session_state.axion.get_constraints()
        max_chunk = limits["max_per_transfer"]
        balance = limits["balance"]
        
        # Real-world cap
        execution_goal = min(total_goal, balance)
        
        plan = []
        remaining = execution_goal
        
        while remaining > 0:
            amt = min(max_chunk, remaining)
            plan.append({
                "type": "TRANSFER", 
                "amount": amt, 
                "note": f"Informed Step ({limits['role']} cap)"
            })
            remaining -= amt
            
        return plan, execution_goal
    except Exception as e:
        return None, 0

# --- 2. UI LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("System Identity")
    role_select = st.selectbox("Current Role:", ["guest", "admin"])
    if st.button("Set State & Update Identity"):
        # Reset/Set ledger for the test
        st.session_state.axion.enforce({"type": "SET_LIMIT", "value": 5000, "role": role_select})
        st.rerun()

    st.markdown("---")
    snap = st.session_state.axion.get_state_snapshot()
    st.metric("Verified Ledger", f"${snap['verified_balance']}")
    st.metric("Role Context", snap['active_role'].upper() if snap['active_role'] else "NONE")
    st.caption(f"Integrity Hash: {snap['state_integrity_hash']}")

with col2:
    st.subheader("Autonomous Mission")
    intent = st.text_input("High-Level Goal:", value="Distribute 2000")
    
    if st.button("🚀 EXECUTE INFORMED MISSION"):
        plan, goal_sum = informed_planner(intent)
        
        if plan and goal_sum > 0:
            st.write("### Generated Plan Preview")
            st.json(plan)
            
            # PRE-EXECUTION AUDIT
            audit = st.session_state.axion.simulate_plan(plan, expected_total=goal_sum)
            
            if audit["status"] == "VALIDATED":
                st.info("Plan Validated. Committing to Ledger...")
                for step in plan:
                    st.session_state.axion.enforce(step)
                st.success(f"Mission Complete. Sum Verified: {goal_sum}")
                st.rerun()
            else:
                st.error(f"Audit Blocked: {audit['reason']}")
        else:
            st.warning("Invalid Intent or Zero Balance.")

# --- 3. FORENSIC AUDIT TRAIL ---
st.markdown("---")
st.subheader("🧾 Immutable Forensic Trace")
if st.session_state.axion.history:
    st.table(st.session_state.axion.history)
else:
    st.write("No transactions committed.")
  
