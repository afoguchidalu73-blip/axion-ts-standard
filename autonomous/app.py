import streamlit as st
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AXION Autonomous Agent",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# 2. LOAD ENVIRONMENT
# ==========================================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# ==========================================
# 3. OPENROUTER CLIENT
# ==========================================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# ==========================================
# 4. AXION AGENT
# ==========================================
class AxionGAA:
    def __init__(self, goal):
        self.goal = goal
        self.memory = []
        self.model = "openrouter/auto:free"

    def execute_cycle(self):
        prompt = (
            f"You are AXION, an Autonomous Agent.\n\n"
            f"MISSION:\n{self.goal}\n\n"
            f"MEMORY:\n{self.memory}\n\n"
            "Provide:\n"
            "1. Analysis of the mission\n"
            "2. Step-by-step execution strategy\n"
            "3. Risks and constraints\n"
            "4. Recommended next action"
        )

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are AXION, a governed autonomous enterprise agent. "
                            "Be logical, structured, safe, and strategic."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "AXION Autonomous Agent",
                }
            )

            thought = response.choices[0].message.content

            self.memory.append(thought)

            return {
                "status": "success",
                "response": thought
            }

        except Exception as e:
            return {
                "status": "error",
                "response": str(e)
            }

# ==========================================
# 5. SESSION STATE
# ==========================================
if "logs" not in st.session_state:
    st.session_state.logs = []

if "memory" not in st.session_state:
    st.session_state.memory = []

# ==========================================
# 6. HEADER
# ==========================================
st.title("🤖 AXION Autonomous Agent")
st.caption("Governed General Autonomous Architecture")

# ==========================================
# 7. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ System Status")

    if api_key:
        st.success("API Key Loaded")
    else:
        st.error("OPENAI_API_KEY Missing")

    st.markdown("---")

    st.subheader("🧠 Memory Size")
    st.write(len(st.session_state.memory))

    st.subheader("📜 Logs")
    st.write(len(st.session_state.logs))

# ==========================================
# 8. MISSION INPUT
# ==========================================
mission = st.text_area(
    "📍 Enter Mission Goal",
    height=150,
    placeholder="Example: Research AI startup opportunities in healthcare..."
)

# ==========================================
# 9. CONTROL BUTTONS
# ==========================================
col1, col2, col3 = st.columns(3)

run_clicked = col1.button("🚀 Run AXION")
clear_clicked = col2.button("🧹 Clear Memory")
save_clicked = col3.button("💾 Save Logs")

# ==========================================
# 10. CLEAR MEMORY
# ==========================================
if clear_clicked:
    st.session_state.memory = []
    st.session_state.logs = []
    st.success("Memory Cleared")

# ==========================================
# 11. RUN AGENT
# ==========================================
if run_clicked:

    if not mission.strip():
        st.warning("Please enter a mission.")
    else:

        with st.spinner("AXION thinking..."):

            agent = AxionGAA(mission)

            # Restore previous memory
            agent.memory = st.session_state.memory

            result = agent.execute_cycle()

            if result["status"] == "success":

                st.session_state.memory = agent.memory

                log_entry = {
                    "time": time.strftime("%H:%M:%S"),
                    "mission": mission,
                    "result": result["response"]
                }

                st.session_state.logs.append(log_entry)

                st.success("Mission Executed")

                st.subheader("🧠 AXION Reasoning")

                st.markdown(result["response"])

            else:
                st.error(result["response"])

# ==========================================
# 12. MEMORY VIEW
# ==========================================
st.markdown("---")
st.subheader("🧠 Long-Term Memory")

if st.session_state.memory:
    for i, mem in enumerate(reversed(st.session_state.memory[-5:]), 1):
        with st.expander(f"Memory {i}"):
            st.write(mem)
else:
    st.info("No memory stored yet.")

# ==========================================
# 13. LOG VIEWER
# ==========================================
st.markdown("---")
st.subheader("📜 Execution Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):

        with st.container(border=True):

            st.markdown(f"### ⏰ {log['time']}")
            st.markdown(f"**Mission:** {log['mission']}")

            with st.expander("View Result"):
                st.write(log["result"])

else:
    st.info("No logs available.")

# ==========================================
# 14. SAVE LOGS
# ==========================================
if save_clicked:

    if st.session_state.logs:

        filename = f"axion_logs_{int(time.time())}.txt"

        with open(filename, "w", encoding="utf-8") as f:

            for log in st.session_state.logs:
                f.write(f"TIME: {log['time']}\n")
                f.write(f"MISSION: {log['mission']}\n")
                f.write(f"RESULT:\n{log['result']}\n")
                f.write("\n" + "="*80 + "\n\n")

        st.success(f"Logs saved as {filename}")

    else:
        st.warning("No logs to save.")

# ==========================================
# 15. FOOTER
# ==========================================
st.markdown("---")
st.caption("AXION GAA • Autonomous Enterprise Runtime")
