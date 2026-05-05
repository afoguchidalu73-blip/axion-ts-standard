import streamlit as st
from governor import AxionKernel
import json
import threading
import time

# --- Persistence Layer ---
if 'axion' not in st.session_state:
    st.session_state.axion = AxionKernel()

st.set_page_config(page_title="AXION v9.1 | Concurrency Lab", layout="wide")
st.title("🛡️ AXION v9.1 | Multi-Agent Concurrency Lab")

# --- INFORMED PLANNER ---
def informed_planner(agent_name, goal_text):
    try:
        # Extract numerical goal
        total_goal = int(''.join(filter(str.isdigit, goal_text)))
        
        # SIGHT: Get current rules and available liquidity from the Kernel
        limits = st.session_state.axion.get_constraints()
        
        max_chunk = limits["max_per_transfer"]
        available = limits["available_funds"]
        
        # Planner bounds the goal to current reality
        exec_goal = min(total_goal, available)
        
        plan = []
        remaining = exec_goal
        
        while remaining > 0:
            amt = min(max_chunk, remaining)
            plan.append({
                "type": "TRANSFER", 
                "amount": amt, 
                "agent": agent_name,
                "note": f"Informed Split ({limits['role']})"
            })
            remaining -= amt
            
        return plan, exec_goal
    except Exception:
        return None, 0

# --- THE ATOMIC EXECUTION LIFECYCLE ---
def execute_mission(agent_name, intent):
    """
    Standard Mission Lifecycle: 
    RESERVE -> AUDIT -> COMMIT -> RELEASE
    """
    plan, total = informed_planner(agent_name, intent)
    
    if not plan or total == 0:
        return f"REJECTED: Insufficient available funds for {agent_name}."

    # 1. ATOMIC RESERVATION (The Gate)
    if st.session_state.axion.request_reservation(total):
        try:
            # 2. PRE-EXECUTION AUDIT
            audit = st.session_state.axion.simulate_plan(plan, total)
            
            if audit["status"] == "VALIDATED":
                # 3. SEQUENTIAL COMMIT
                for step in plan:
                    st.session_state.axion.enforce_atomic(step)
                return f"SUCCESS: {agent_name} committed ${total}"
            else:
                return f"FAILED: Audit blocked {agent_name} - {audit['reason']}"
        finally:
            # 4. MANDATORY RELEASE (Cleanup)
            st.session_state.axion.release_reservation(total)
    else:
        return f"BLOCKED: {agent_name} denied due to resource contention."

# --- UI LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Agent Alpha")
    alpha_intent = st.text_input("Alpha Goal:", value="Distribute 6000")
    if st.button("Manual Run Alpha"):
        res = execute_mission("ALPHA", alpha_intent)
        st.info(res)

with col2:
    st.subheader("🤖 Agent Beta")
    beta_intent = st.text_input("Beta Goal:", value="Distribute 6000")
    if st.button("Manual Run Beta"):
        res = execute_mission("BETA", beta_intent)
        st.info(res)

st.markdown("---")

# --- RACE CONDITION TESTER ---
st.subheader("🏁 The Race Condition Simulator")
st.write("This launches Alpha and Beta in simultaneous threads to test the Kernel's atomic locking.")

if st.button("🔥 START SIMULTANEOUS RACE"):
    # Results container for threads
    results = []
    
    def thread_worker(name, intent):
        outcome = execute_mission(name, intent)
        results.append(outcome)

    # Creating simultaneous threads
    t1 = threading.Thread(target=thread_worker, args=("ALPHA", alpha_intent))
    t2 = threading.Thread(target=thread_worker, args=("BETA", beta_intent))

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    for r in results:
        if "SUCCESS" in r:
            st.success(r)
        else:
            st.error(r)
    
    time.sleep(1)
    st.rerun()

# --- TELEMETRY SIDEBAR ---
with st.sidebar:
    st.header("📊 Kernel Telemetry")
    snap = st.session_state.axion.get_constraints()
    st.metric("Ledger Total", f"${snap['total_ledger']}")
    st.metric("Available (Liquid)", f"${snap['available_funds']}")
    st.metric("System Role", snap['role'].upper())
    
    if st.button("RESET KERNEL"):
        st.session_state.axion = AxionKernel()
        st.rerun()

# --- FORENSIC LEDGER ---
st.subheader("🧾 Immutable Forensic Audit Trail")
if st.session_state.axion.history:
    st.table(st.session_state.axion.history)
else:
    st.caption("No transactions committed to the ledger yet.")
      
