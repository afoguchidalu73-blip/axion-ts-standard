import numpy as np

class ObjectState:
    def __init__(self, name, value, uncertainty=0.1):
        self.name = name
        self.mean = value
        self.uncertainty = uncertainty 

class StructuredWorldModel:
    def __init__(self):
        # The agent's belief about the current reality
        self.objects = {
            "balance": ObjectState("balance", 10000.0, 0.0),
            "system_stability": ObjectState("system_stability", 1.0, 0.05),
            "data_verified": ObjectState("data_verified", 0.0, 1.0) # 0 to 1 scale
        }

    def predict(self, action):
        """Mental Simulation: Predicts the next state without changing reality."""
        future_state = {k: ObjectState(v.name, v.mean, v.uncertainty) for k, v in self.objects.items()}
        
        # Causal Logic for Transfers
        if action["type"] == "TRANSFER":
            amt = action.get("amount", 0)
            future_state["balance"].mean -= amt
            future_state["balance"].uncertainty += (amt * 0.01) # Large moves increase entropy
            future_state["system_stability"].mean -= (amt * 0.0001)

        # Causal Logic for Tools
        elif action["type"] == "TOOL":
            if action["name"] == "web_search":
                # Prediction: Search increases verification and lowers uncertainty
                future_state["data_verified"].mean = min(1.0, future_state["data_verified"].mean + 0.4)
                future_state["balance"].uncertainty *= 0.5 
            
            elif action["name"] == "file_write":
                future_state["system_stability"].mean = min(1.0, future_state["system_stability"].mean + 0.05)

        return future_state

    def update(self, observation):
        """Bayesian-lite update: Corrects internal beliefs based on Kernel reality."""
        for key, val in observation.items():
            if key in self.objects:
                error = abs(self.objects[key].mean - val)
                # Weighted update
                self.objects[key].mean = (self.objects[key].mean * 0.7) + (val * 0.3)
                # Adjust uncertainty based on prediction error
                self.objects[key].uncertainty = (self.objects[key].uncertainty * 0.9) + (error * 0.1)
                
