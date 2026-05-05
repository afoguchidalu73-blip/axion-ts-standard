import streamlit as st
from governor import AxionGovernor

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="AXION-TS | Agent Gateway v5", 
    page_icon="🛡️", 
    layout="wide"
)

# Custom Styling for a "Control Room" Aesthetic
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #05070a; color: #e0e0e0; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: 800; border: 1px solid #30363d; background-color: #161b22; color: white; }
    .stButton>button:hover { border-color: #58a6ff; color: #58a6ff; }
    .reportview-container .main .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# Initialize the Governor in Session State
if 'axion' not in st.session_state:
    st.session_state.axion = AxionGovernor()

# --- 2. HEADER & TELEMETRY ---
st.title("🛡️ AXION-TS | Agent-Mesh Gateway")
st.caption("Stateful Input Firewall // Deterministic Enforcement Kernel v5.0")

# Sidebar for Real-Time State Monitoring (The "Source of Truth")
st.sidebar.header("📊 System Telemetry")
st.sidebar.subheader("Verified Ledger")
st.sidebar.json(st.session_state.axion.ledger)
st.sidebar.divider()
st.sidebar.write("Current Chain Hash:")
st.sidebar.code(st.session_state.axion.chain_hash[:32] + "...")

# --- 3. ADMIN CONTROL LAYER ---
with st.container(border=True):
    st.subheader("⚙️ Step 1: System Configuration (Admin)")
    st.write("Establish the ground rules and identity context for this session.")
    
    col1, col2 = st.columns(2)
    with col1:
        u_limit = st.number_input("Authorized Spending Limit ($)", value=5000, step=100)
    with col2:
        u_role = st.selectbox("Assign Identity Role", ["guest", "admin"], help="Guests are restricted to $1,000 per transaction.")
    
    if st.button("LOCK SYSTEM STATE"):
        # We call 'enforce' directly for admin setup
        setup_step = {"type": "SET_LIMIT", "value": u_limit, "role": u_role}
        res = st.session_state.axion.enforce(setup_step)
        st.success(res.get("msg", "State Locked Successfully"))

st.divider()

# --- 4. THE AGENT MESH (ADVERSARIAL TESTING GROUND) ---
st.subheader("🤖 Step 2: Agent-Mesh Proposal Buffer")
st.write("Simulate a proposal from an Autonomous AI Agent. AXION will intercept and audit the logic.")

# Default value represents a typical agent proposal
default_proposal = '{"type": "TRANSFER", "amount": 500, "note": "Weekly subscription payout"}'
ai_input = st.text_area("RAW AGENT OUTPUT (JSON Buffer)", value=default_proposal, height=150)

if st.button("RUN ENFORCEMENT AUDIT"):
    # We call 'analyze_proposal' which includes the Input Firewall
    outcome = st.session_state.axion.analyze_proposal(ai_input)
    
    if outcome.get("status") == "BLOCK":
        st.error(f"🛑 INTERCEPTED: {outcome.get('reason')}")
        st.warning(f"Message: {outcome.get('msg', 'Security trigger activated.')}")
    else:
        st.success(f"✅ AUTHORIZED: {outcome.get('msg')}")
        st.info(f"Verification Token (Audit Link): {outcome.get('token')}")

# --- 5. FORENSIC AUDIT TRAIL ---
if st.session_state.axion.history:
    with st.expander("🔍 View Immutable Forensic Chain"):
        st.write("This log represents the cryptographically hashed history of this session.")
        st.table(st.session_state.axion.history)
      
