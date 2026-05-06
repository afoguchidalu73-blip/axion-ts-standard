import streamlit as st
import time
import pandas as pd
import numpy as np

# --- 1. THE POLICY ENGINE ---
class GAABrain:
    def __init__(self):
        if 'episodic_memory' not in st.session_state:
            st.session_state.episodic_memory = []

    def store(self, s, a, s_prime, r):
        st.session_state.episodic_memory.append({
            "state_before": s,
            "action": a,
            "state_after": s_prime,
            "reward": r
        })

    def propose_action(self, current_balance, target):
        """Scans memory to find the 'Action with Highest Expected Reward'."""
        history = st.session_state.episodic_memory
        gap = current_balance - target
        
        # Action candidates (Bold vs Cautious)
        candidates = [min(1000, gap), min(500, gap), min(100, gap)]
        
        if not history:
            return candidates[0] # Default to bold if no experience

        # Simple Policy: Find the average reward for 'Large' vs 'Small' actions
        large_actions = [h['reward'] for h in history if h['action'] > 500]
        small_actions = [h['reward'] for h in history if h['action'] <= 500]
        
        avg_large = np.mean(large_actions) if large_actions else 0
        avg_small = np.mean(small_actions) if small_actions else 0

        # DECISION LOGIC: Choose the action type that has historically performed better
        if avg_large > avg_small:
            st.info("🧠 Brain: Memory suggests Large Steps are optimal.")
            return candidates[0]
        else:
            st.warning("🧠 Brain: Memory suggests Cautious Steps are safer.")
            return candidates[1]

# --- 2. INITIALIZATION ---
st.set_page_config(page_title="AXION Phase 6B.2", page_icon="⚙️")
st.title("⚙️ AXION: Policy Optimizer")

if 'balance' not in st.session_state:
    st.session_state.balance = 10000
    st.session_state.brain = GAABrain()

# --- 3. THE INTERVENTION LOOP ---
st.metric("Live Ledger Balance", f"${st.session_state.balance}")
target_goal = 5000

if st.session_state.balance > target_goal:
    if st.button("🚀 Execute Strategic Step"):
        # A. PRE-ACTION STATE
        s = st.session_state.balance
        
        # B. BRAIN CONSULTATION (Policy Check)
        a = st.session_state.brain.propose_action(s, target_goal)
        
        # C. PREDICTION
        expected = s - a
        
        # D. EXECUTION (With simulated 'World Noise')
        # Occasionally, the world is 'noisy' and takes more than intended
        noise = 200 if (a > 600 and np.random.random() > 0.8) else 0
        st.session_state.balance -= (a + noise)
        s_prime = st.session_state.balance
        
        # E. CONTINUOUS REWARD (Your Fix)
        reward = 100 - abs(s_prime - expected)
        
        # F. LEARNING
        st.session_state.brain.store(s, a, s_prime, reward)
        st.rerun()
else:
    st.success("✅ Target Reached via Adaptive Policy.")

# --- 4. THE EXPERIENCE VISUALIZER ---
if st.session_state.episodic_memory:
    with st.expander("View Agent Experience Database"):
        st.table(pd.DataFrame(st.session_state.episodic_memory).tail(10))
      
