import time
import os
import json
import random
from datetime import datetime

# --- 1. THE EMBODIED ENVIRONMENT ---
STATE_FILE = "axion_state.json"  # The agent's "Vitals"
WORLD_DIR = "./axion_env/"
LOG_FILE = "axion_autonomy.log"

if not os.path.exists(WORLD_DIR):
    os.makedirs(WORLD_DIR)

class AxionStateEngine:
    def __init__(self):
        self.boot_time = datetime.now()
        self.load_or_init_state()

    def load_or_init_state(self):
        """Persistent Vitals: Energy and Structural Integrity."""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"energy": 100.0, "integrity": 100.0, "status": "ALIVE"}
        self.save_state()

    def save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f)

    def sense_environment(self):
        """The agent looks at the world and its own body."""
        files = os.listdir(WORLD_DIR)
        return len(files)

    def apply_entropy(self):
        """Real Autonomy Requirement: The world decays over time."""
        # Living costs energy; time damages integrity
        self.state["energy"] -= 1.5 
        self.state["integrity"] -= 0.5
        
        if self.state["energy"] <= 0 or self.state["integrity"] <= 0:
            self.state["status"] = "DEAD"

    def decide_and_act(self, resource_count):
        """Homeostatic Intelligence: Action based on survival need."""
        energy = self.state["energy"]
        
        # PRIORITY 1: Survival (Recharge)
        if energy < 40:
            self.log("CRITICAL: Low Energy. Initiating Recharge (Simulated External Fetch).")
            self.state["energy"] += 20
            return "RECHARGE"

        # PRIORITY 2: Growth (Resource Creation)
        if resource_count < 10:
            filename = f"res_{int(time.time())}.dat"
            with open(os.path.join(WORLD_DIR, filename), "w") as f:
                f.write("Structural Resource")
            self.state["energy"] -= 5 # Work costs energy
            self.state["integrity"] += 2 # Building improves integrity
            return f"BUILD_RESOURCE ({filename})"

        return "STASIS"

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {msg} | E: {self.state['energy']:.1f} | I: {self.state['integrity']:.1f}"
        print(entry)
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

    def run_forever(self):
        self.log("AXION State Autonomy Online.")
        try:
            while self.state["status"] == "ALIVE":
                # 1. Entropy (The clock is ticking)
                self.apply_entropy()
                
                # 2. Perceive
                resources = self.sense_environment()
                
                # 3. Decide & Act
                action = self.decide_and_act(resources)
                
                # 4. Save
                self.save_state()
                
                # 5. Heartbeat pacing
                time.sleep(3)
                
            self.log("FATAL: Agent has reached terminal state (System Death).")
        except KeyboardInterrupt:
            self.log("Suspended by User.")

if __name__ == "__main__":
    agent = AxionStateEngine()
    agent.run_forever()
          
