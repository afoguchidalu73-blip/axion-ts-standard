import streamlit as st
import time
# Assuming your other files are named: kernel.py, world_model.py, planner.py
from kernel import AxionKernel
from world_model import WorldModel
from planner import Planner

st.set_page_config(page_title="AXION Core v6A", page_icon="🛡️")
st.title("🛡️ AXION: Stable Core v6A")
st.caption("Baseline Stability Test: 10k → 5k Reduction")

# --- 1. PERSISTENT STATE (Crucial for Streamlit) ---
if 'kernel' not in st.session_state:
    st.session_state.kernel = AxionKernel(initial_balance=10000)
    st.session_state.world = WorldModel(initial_val=10000)
    st.session_state.planner = Planner(st.session_state.world)
    st.session_state.history = []

# --- 2. UI CONTROLS ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Current Balance", f"${st.session_state.kernel.balance}")
with col2:
    target = st.number_input("Target Goal", value=5000, step=100)

if st.button("🚀 Start Autonomous Mission"):
    status = st.empty()
    progress = st.progress(0)
    
    # --- 3. THE OODA LOOP ---
    for step in range(15):
        # A. PERCEIVE
        st.session_state.world.update(st.session_state.kernel.balance)
        
        # B. THINK
        action = st.session_state.planner.find_action(target)
        
        if action["type"] == "NOOP":
            status.success("✅ Mission AccomplISHED: Target Reached.")
            break
            
        # C. PREDICT
        expected = st.session_state.world.predict(action)
        
        # D. ACT
        is_valid, reason = st.session_state.kernel.validate(action)
        
        if is_valid:
            st.session_state.kernel.execute(action)
            actual = st.session_state.kernel.balance
            
            # E. VERIFY
            if actual != expected:
                st.error(f"⚠️ ANOMALY! Expected {expected}, got {actual}")
                break
            
            st.session_state.history.append(f"Step {step}: Transferred {action['amount']} | Balance: {actual}")
            status.info(f"Step {step}: Executing...")
        else:
            st.warning(f"🛡️ Kernel Block: {reason}")
            break
        
        progress.progress((step + 1) / 10 if step < 10 else 1.0)
        time.sleep(0.4) # Give UI time to breathe
        st.rerun() # Refresh UI to show new balance

# --- 4. LOGS ---
if st.session_state.history:
    with st.expander("View Execution Logs"):
        for log in reversed(st.session_state.history):
            st.text(log)
      
