import time

class GeneralAutonomousAgent:
    def __init__(self, kernel, world_model, planner, memory, tools):
        self.kernel = kernel
        self.world_model = world_model
        self.planner = planner
        self.memory = memory
        self.tools = tools
        self.is_running = False

    def run_cycle(self, goal_state):
        """A single OODA (Observe-Orient-Decide-Act) Loop."""
        
        # 1. OBSERVE: Get ground truth from the Kernel
        kernel_data = self.kernel.get_state_snapshot()
        observation = {
            "balance": kernel_data["balance"],
            "system_stability": 1.0 # In a real env, this would be a telemetry sensor
        }
        self.world_model.update(observation)

        # 2. DECIDE: Ask the Planner for the best causal path
        # The planner uses the World Model to simulate 'TRANSFER' vs 'TOOL'
        action = self.planner.find_best_action(goal_state)
        
        if not action or action["type"] == "NOOP":
            return "IDLE: Goal reached or no safe path."

        # 3. VALIDATE: Run the action through the AXION Safety Reflex
        is_safe, reason = self.kernel.validate(action)
        
        if not is_safe:
            # Memory records the failure so the Planner avoids this path next time
            self.memory.store(observation, action, observation, reward=-50)
            return f"HALTED: Safety Violation - {reason}"

        # 4. ACT: Execute via Ledger or Tool Registry
        if action["type"] == "TOOL":
            result = self.tools.execute(action["name"], action.get("params", "default"))
            execution_data = result
        else:
            execution_data = self.kernel.execute(action)

        # 5. LEARN: Evaluate the delta between Prediction and Reality
        new_kernel_state = self.kernel.get_state_snapshot()
        new_obs = {"balance": new_kernel_state["balance"]}
        
        # Calculate Reward (Success = Getting closer to goal + Low Uncertainty)
        reward = self._calculate_reward(goal_state, new_obs["balance"])
        self.memory.store(observation, action, new_obs, reward)

        return f"SUCCESS: Executued {action.get('type')} - {action.get('name', 'ledger')}"

    def _calculate_reward(self, goal, actual):
        gap = abs(goal["balance"] - actual)
        return 100 - (gap / 100) # Simple linear reward
          
