import streamlit as st
import json
from axion.kernel import analyze_drift
from graphviz import Digraph

# --- PAGE CONFIG ---
st.set_page_config(page_title="AXION Firewall", page_icon="🛡️", layout="wide")

# --- PRO CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;800&family=JetBrains+Mono&display=swap');
html, body, [class*="css"] { background-color: #0e1117; color: #e6edf3; font-family: 'Inter', sans-serif; }
.title { font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #00f5a0, #00d9f5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; }
.sub { color: #8b949e; font-size: 1rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; }
.card { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.pass-text { color: #3fb950; font-size: 1.8rem; font-weight: 800; }
.fail-text { color: #f85149; font-size: 1.8rem; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# --- GRAPH ENGINE ---
def build_graph(trace, highlight_edges=None):
    dot = Digraph()
    dot.attr(bgcolor='transparent', fontcolor='white')
    dot.attr('node', shape='circle', color='#00d9f5', fontcolor='white', style='filled', fillcolor='#161b22')
    dot.attr('edge', color='#8b949e', fontcolor='white')
    
    highlight_edges = highlight_edges or []
    for event in trace:
        node_id = str(event.get("id"))
        dot.node(node_id)
        parents = event.get("parents", [])
        if not isinstance(parents, list): parents = [parents]
        for p in parents:
            edge = (str(p), node_id)
            if edge in highlight_edges:
                dot.edge(str(p), node_id, color="#f85149", penwidth="4", label="⚠️ BREACH")
            else:
                dot.edge(str(p), node_id)
    return dot

# --- HEADER ---
st.markdown('<div class="title">AXION</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Visual Causal Integrity Firewall</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
mode = st.sidebar.radio("Input Mode", ["📁 Upload Files", "📝 Paste Text"])
st.sidebar.divider()

current_data, baseline_data = None, None

if mode == "📁 Upload Files":
    c1, c2 = st.columns(2)
    with c1:
        f1 = st.file_uploader("Current Trace", type="json")
        if f1: current_data = json.load(f1)
    with c2:
        f2 = st.file_uploader("Baseline Trace", type="json")
        if f2: baseline_data = json.load(f2)
else:
    c1, c2 = st.columns(2)
    with c1:
        t1 = st.text_area("Paste Current JSON", height=150)
        if t1: current_data = json.loads(t1)
    with c2:
        t2 = st.text_area("Paste Baseline JSON", height=150)
        if t2: baseline_data = json.loads(t2)

# --- ANALYSIS ---
if current_data and baseline_data:
    if st.button("EXECUTE SYSTEM AUDIT"):
        result = analyze_drift(current_data, baseline_data)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        if result["status"] == "PASSED":
            st.markdown('<div class="pass-text">✅ SYSTEM SECURE</div>', unsafe_allow_html=True)
            st.write("Causal graph matches baseline perfectly. No unauthorized path detected.")
            st.graphviz_chart(build_graph(current_data))
        else:
            st.markdown('<div class="fail-text">❌ BREACH DETECTED</div>', unsafe_allow_html=True)
            
            # Threat Translation
            st.warning(f"**Threat Report:** Unauthorized process flow detected. A step was inserted/altered between critical operations.")
            
            # Visual Graph
            st.subheader("🗺️ Forensics Map")
            extra_edges = result.get("details", {}).get("extra", [])
            highlight = [(str(a), str(b)) for a, b in extra_edges]
            st.graphviz_chart(build_graph(current_data, highlight))
            
            with st.expander("Technical Root Cause"):
                st.code(result.get("cause"))
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("AXION v1.2 • Causal Integrity Protocol")
  
