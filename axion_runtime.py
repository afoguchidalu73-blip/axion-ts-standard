import time
import os
import json
from datetime import datetime

# --- 1. THE PERSISTENT ENVIRONMENT (The "Real" World) ---
GOAL_FILE = "agent_goal.json"
ENV_DIR = "./axion_world/"
LOG_FILE = "axion_lifecycle.log"

if not os.path.exists(ENV_DIR):
    os.makedirs(ENV_DIR)

# --- 2. THE AUTONOMOUS BRAIN (The Heartbeat) ---
class AxionRuntime:
    def __init__(self):
        self.active = True
        self.iteration = 0
        self.ensure_goal_exists()

    def ensure_goal_exists(self):
        """Goal persistence: The agent's reason for existing."""
        if not os.path.exists(GOAL_FILE):
            initial_goal = {"target_files": 5, "status": "active"}
            with open(GOAL_FILE, 'w') as f:
                json.dump(initial_goal, f)

    def perceive(self):
        """Sense the real external world."""
        files = os.listdir(ENV_DIR)
        with open(GOAL_FILE, 'r') as f:
            goal = json.load(f)
        return len(files), goal

    def decide(self, current_count, goal):
        """Determine if action is needed based on persistent intent."""
        if current_count < goal["target_files"]:
            return "CREATE_RESOURCE"
        return "IDLE"

    def act(self, decision):
        """Execute a real-world change."""
        timestamp = datetime.now().strftime("%H%M%S")
        if decision == "CREATE_RESOURCE":
            filename = f"data_{timestamp}.txt"
            with open(os.path.join(ENV_DIR, filename), "w") as f:
                f.write(f"Resource created by AXION at {timestamp}")
            return f"Created {filename}"
        return "No action required."

    def log(self, message):
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
        print(f"🤖 AXION: {message}")

    def run(self):
        """The Continuous Autonomous Loop."""
        self.log("System Awakened. Entering Autonomous Loop.")
        try:
            while self.active:
                self.iteration += 1
                
                # 1. Sense
                count, goal = self.perceive()
                
                # 2. Decide
                decision = self.decide(count, goal)
                
                # 3. Act
                result = self.act(decision)
                
                # 4. Record
                self.log(f"Iteration {self.iteration} | Files: {count}/{goal['target_files']} | {result}")
                
                # 5. Sleep (Pacing for safety)
                time.sleep(5) 
                
        except KeyboardInterrupt:
            self.log("Manual Shutdown Detected. Hibernating.")

# --- 3. THE EXECUTION ---
if __name__ == "__main__":
    agent = AxionRuntime()
    agent.run()
          
