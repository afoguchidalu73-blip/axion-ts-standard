# motivation.py

class IntrinsicDrives:
    def __init__(self):
        # Drives scale from 0 to 1.0 (1.0 = satisfied)
        self.drives = {
            "resource_security": 0.8, # Fear of low balance
            "curiosity": 0.5,         # Desire to reduce world model uncertainty
            "integrity": 1.0          # Desire to keep stability high
        }

    def update_drives(self, world_state):
        """Drives decay over time or respond to environment changes."""
        # Curiosity increases as World Model uncertainty grows
        avg_uncertainty = sum(o.uncertainty for o in world_state.values()) / len(world_state)
        self.drives["curiosity"] = max(0, 1.0 - avg_uncertainty)

        # Resource security drops if balance is low
        self.drives["resource_security"] = min(1.0, world_state["balance"].mean / 10000)

    def generate_top_priority_goal(self):
        """The 'Self' chooses what to care about next."""
        neediest_drive = min(self.drives, key=self.drives.get)
        
        if neediest_drive == "curiosity":
            return {"type": "EXPLORE", "target": "reduce_uncertainty"}
        elif neediest_drive == "resource_security":
            return {"type": "OPTIMIZE", "target": "increase_balance"}
        
        return {"type": "STABILIZE", "target": "maintain_status_quo"}
      
