# planner.py (Upgraded)
import copy

class StrategicPlanner:
    def __init__(self, world_model, memory, kernel):
        self.world_model = world_model
        self.memory = memory
        self.kernel = kernel

    def find_plan(self, goal, depth=2):
        """Generates a multi-step sequence toward the goal."""
        best_sequence = []
        max_utility = float('-inf')

        # Simple 2-step lookahead
        for action1 in self._get_valid_actions():
            # Step 1: Simulate
            sim_state_1 = self.world_model.predict(action1)
            
            for action2 in self._get_valid_actions():
                # Step 2: Simulate from state 1
                # (Ideally we'd deepcopy the world model here)
                sim_state_2 = self._predict_from_sim(sim_state_1, action2)
                
                utility = self._score_state(sim_state_2, goal)
                if utility > max_utility:
                    max_utility = utility
                    best_sequence = [action1, action2]

        return best_sequence

    def _get_valid_actions(self):
        # Returns current tool options + transfer options
        return [{"type": "TOOL", "name": "web_search"}, {"type": "TRANSFER", "amount": 500}]
      
