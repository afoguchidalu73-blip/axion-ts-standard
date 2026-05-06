import os, json, time

class AxionPolicy:
    def __init__(self):
        # The agent's "Values". These will evolve over time.
        self.weights = {"energy": 1.0, "integrity": 1.0}

    def score_action(self, e_delta, i_delta):
        """Higher score = Action is more 'valuable' to the agent."""
        return (self.weights["energy"] * e_delta) + (self.weights["integrity"] * i_delta)

    def learn(self, e_delta, i_delta, reward):
        """Self-Modification: Adjust weights based on the outcome."""
        learning_rate = 0.05
        # If reward was good, strengthen the weights that led here
        self.weights["energy"] += learning_rate * reward * e_delta
        self.weights["integrity"] += learning_rate * reward * i_delta

class AxionHomeostasis:
    def __init__(self):
        self.state = {"energy": 80.0, "integrity": 80.0, "status": "ALIVE"}
        self.policy = AxionPolicy()

    def run_cycle(self):
        # 1. Simulate Outcomes (Imagination)
        # Option A: Recharge (+20 Energy, -5 Integrity)
        # Option B: Repair (-10 Energy, +15 Integrity)
        
        score_recharge = self.policy.score_action(20, -5)
        score_repair = self.policy.score_action(-10, 15)

        # 2. Decision (Choose highest utility)
        if score_recharge > score_repair:
            action = "RECHARGE"
            e_d, i_d = 20, -5
        else:
            action = "REPAIR"
            e_d, i_d = -10, 15

        # 3. Apply and Calculate Reward
        self.state["energy"] += e_d
        self.state["integrity"] += i_d
        
        # Simple Reward: Are we moving toward 100/100 or 0/0?
        reward = (self.state["energy"] + self.state["integrity"]) / 200
        
        # 4. Self-Modify Policy
        self.policy.learn(e_d, i_d, reward)
        
        return action

# --- BOOT ---
if __name__ == "__main__":
    agent = AxionHomeostasis()
    print(f"🚀 {agent.__class__.__name__} Deployed to GitHub.")
    for i in range(5):
        act = agent.run_cycle()
        print(f"Cycle {i}: Action {act} | Vitals: {agent.state['energy']}/{agent.state['integrity']}")
      
