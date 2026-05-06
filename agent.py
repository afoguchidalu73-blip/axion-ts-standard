# agent.py

class GeneralAutonomousAgent:
    def __init__(self, kernel, world_model, planner, memory, tools):
        self.tools = tools
        # ... other inits ...

    def execute_cycle(self, goal_balance):
        # 1. ANALYZE GOAL: Does the agent need more info?
        if self.world_model.objects["balance"].uncertainty > 0.5:
            # Planner will likely choose 'web_search' because it has highest utility 
            # for reducing the 'uncertainty penalty' we coded earlier.
            action = {"type": "TOOL", "name": "web_search", "params": "current balance rules"}
        else:
            action = self.planner.find_best_action(goal={"balance": goal_balance})

        # 2. VALIDATE & EXECUTE
        if self.kernel.validate(action):
            if action["type"] == "TOOL":
                # Real-world impact!
                result = self.tools.execute(action["name"], action.get("params"))
                st.info(f"🛠️ Tool Used: {action['name']} -> {result}")
            else:
                self.kernel.execute(action)
            
            # 3. LEARN (Store in Deep Memory)
            # The agent now remembers: "Searching helped me be certain before transferring."
            self.memory.store(...) 
