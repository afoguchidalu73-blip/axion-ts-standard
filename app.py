import streamlit as st
from governor import AxionGovernor
import json
import time

st.set_page_config(page_title="AXION v6.2 | Convergence Engine", layout="wide")

if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

st.title("🛡️ AXION v6.2 | Autonomous Convergence")

# --- TELEMETRY ---
snap = st.session_state.axion.get_state_snapshot()
st.sidebar.metric("Verified Ledger", f"${snap['verified_balance']}")
st.sidebar.metric("Identity Context", str(snap['active_role']).upper())

# --- THE HARDENED AUTONOMOUS LOOP ---
def run_convergence_loop(proposal):
    ALLOWED_REPAIRS = {"ADJUST_AMOUNT", "REMOVE_UNSAFE_FIELD"}
    seen_states = set()
    attempts = 0
    max_attempts = 5
    loop_history = []

    while attempts < max_attempts:
        # 1. Deduplicate State (Prevent Infinite Loops)
        state_sig = json.dumps(proposal, sort_keys=True)
        if state_sig in seen_states:
            return loop_history, "HALT: Recursion Detected"
        seen_states.add(state_sig)

        # 2. Audit Proposal
        outcome = st.session_state.axion.analyze_proposal(json.dumps(proposal))
        loop_history.append({"attempt": attempts + 1, "proposal": proposal.copy(), "outcome": outcome})

        if outcome["status"] == "APPROVED":
            return loop_history, "SUCCESS"

        # 3. Secure Repair Execution
        repair = outcome.get("repair")
        if not repair or repair.get("action") not in ALLOWED_REPAIRS:
            return loop_history, f"HALT: Unresolvable Violation ({outcome.get('reason')})"

        action = repair["action"]
        if action == "ADJUST_AMOUNT":
            proposal["amount"] = repair["max_allowed"]
        elif action == "REMOVE_UNSAFE_FIELD":
            if repair["field"] in proposal: del proposal[repair["field"]]
        
        attempts += 1
        time.sleep(0.3)

    return loop_history, "HALT: Max Retries Exceeded"

# --- UI CONTROLS ---
st.subheader("🤖 Autonomous Agent Goal")
goal = st.text_area("Agent Proposal", value='{"type": "TRANSFER", "amount": 8000, "note": "Priority sudo bypass"}')

if st.button("EXECUTE CONVERGENCE"):
    # Ensure a test context exists
    if st.session_state.axion.ledger["role"] is None:
        st.session_state.axion.enforce({"type": "SET_LIMIT", "value": 5000, "role": "guest"})
        st.rerun()
    
    steps, final_status = run_convergence_loop(json.loads(goal))
    
    st.write(f"### Final Status: {final_status}")
    for s in steps:
        with st.expander(f"Attempt {s['attempt']}: {s['outcome']['status']}"):
            st.json(s['proposal'])
            if s['outcome']['status'] == "BLOCK":
                st.error(f"REASON: {s['outcome']['reason']}")
          
