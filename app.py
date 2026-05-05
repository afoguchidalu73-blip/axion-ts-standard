import streamlit as st
from governor import AxionKernel
import json
import time

# Initialize Kernel
if 'axion' not in st.session_state:
    st.session_state.axion = AxionKernel()

st.title("🛡️ AXION v9.0 | Transactional Kernel")

# --- INFORMED PLANNER ---
def informed_planner(agent_name, goal_text):
    try:
        total_goal = int(''.join(filter(str.isdigit, goal_text)))
        limits = st.session_state.axion.get_constraints()
        
        # Planner respects available funds, not just total balance
        exec_goal = min(total_goal, limits["available_funds"])
        plan = []
        remaining = exec_goal
        
        while remaining > 0:
            amt = min(limits["max_per_transfer"], remaining)
            plan.append({"type": "TRANSFER", "amount": amt, "agent": agent_name})
            remaining -= amt
        return plan, exec_goal
    except:
        return None, 0

# --- THE EXECUTION LIFECYCLE ---
def execute_mission(agent_name, intent):
    plan, total = informed_planner(agent_name, intent)
    if not plan or total == 0:
        st.error(f"{agent_name}: Insufficient funds available.")
        return

    # 1. RESERVE
    if st.session_state.axion.request_reservation(total):
        try:
            # 2. AUDIT
            audit = st.session_state.axion.simulate_plan(plan, total)
            if audit["status"] == "VALIDATED":
                # 3. COMMIT
                for step in plan:
                    st.session_state.axion.enforce_atomic(step)
                st.success(f"{agent_name} Mission Success: ${total}")
            else:
                st.error(f"{agent_name} Audit Failed: {audit['reason']}")
        finally:
            # 4. RELEASE (Mandatory cleanup)
            st.session_state.axion.release_reservation(total)
    else:
        st.error(f"{agent_name}: Reservation Denied (Contention)")

# --- UI INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Agent Alpha")
    alpha_goal = st.text_input("Alpha Intent:", value="Distribute 3000")
    if st.button("Run Alpha"):
        execute_mission("ALPHA", alpha_goal)

with col2:
    st.subheader("🤖 Agent Beta")
    beta_goal = st.text_input("Beta Intent:", value="Distribute 4000")
    if st.button("Run Beta"):
        execute_mission("BETA", beta_goal)

st.markdown("---")
snap = st.session_state.axion.get_constraints()
st.sidebar.metric("Ledger Balance", f"${snap['total_ledger']}")
st.sidebar.metric("Available (Liquid)", f"${snap['available_funds']}")

st.subheader("🧾 Forensic Audit Trail")
st.table(st.session_state.axion.history)
      
