import streamlit as st
import time

# --- STABLE CORE LOGIC (Self-Contained) ---
class RecoveryKernel:
    def __init__(self): self.balance = 10000
    def validate(self, action):
        if action['amount'] > 1000: return False, "Limit Exceeded"
        return True, "Valid"
    def execute(self, action): self.balance -= action['amount']

class RecoveryWorld:
    def __init__(self): self.state = 10000
    def predict(self, action): return self.state - action['amount']
    def update(self, val): self.state = val

# --- UI LAYER ---
st.set_page_config(page_title="AXION Recovery", page_icon="⚡")
st.title("⚡ AXION Emergency Recovery")

if 'k' not in st.session_state:
    st.session_state.k = RecoveryKernel()
    st.session_state.w = RecoveryWorld()
    st.session_state.logs = []

st.metric("Kernel Balance", f"${st.session_state.k.balance}")

# TARGET ACTION
target = 5000
gap = st.session_state.k.balance - target

if gap > 0:
    if st.button("Execute Recovery Step"):
        action = {'type': 'TRANSFER', 'amount': min(1000, gap)}
        
        # OODA Logic
        pred = st.session_state.w.predict(action)
        is_valid, _ = st.session_state.k.validate(action)
        
        if is_valid:
            st.session_state.k.execute(action)
            st.session_state.w.update(st.session_state.k.balance)
            st.session_state.logs.append(f"Moved {action['amount']} | New: {st.session_state.k.balance}")
            st.rerun()
else:
    st.success("✅ Stability Reached.")

# LOGS
for l in reversed(st.session_state.logs):
    st.text(l)
  
