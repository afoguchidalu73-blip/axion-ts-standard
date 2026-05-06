# world_model.py (add this logic to your predict function)
def predict(self, action):
    # ... existing balance/stability logic ...
    
    if action["type"] == "TOOL":
        if action["name"] == "web_search":
            # Predictions: Search doesn't change balance, but kills uncertainty
            new_state["balance"].uncertainty *= 0.5 
            new_state["system_stability"].mean -= 0.01 # minor 'effort' cost
            
    return new_state
  
