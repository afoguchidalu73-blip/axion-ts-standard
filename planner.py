class Planner:
    def __init__(self, world_model):
        self.world_model = world_model

    def find_action(self, target_goal):
        """Calculates the necessary intervention to reach the goal."""
        current_val = self.world_model.state
        gap = current_val - target_goal

        if gap <= 0:
            return {"type": "NOOP"}

        # Stride control: take the largest step allowed by AXION (1000)
        step = min(1000, gap)
        return {"type": "TRANSFER", "amount": step}
      
