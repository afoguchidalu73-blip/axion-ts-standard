import os
import json
import datetime

class ToolRegistry:
    def __init__(self):
        # The 'Menu' for the Planner
        self.registry = {
            "web_search": {
                "func": self._web_search_logic,
                "impact": "reduces_uncertainty",
                "energy_cost": 10,
                "description": "Searches the internet for real-time data."
            },
            "file_write": {
                "func": self._file_write_logic,
                "impact": "persists_data",
                "energy_cost": 5,
                "description": "Saves agent logs or findings to a local file."
            },
            "api_query": {
                "func": self._api_query_logic,
                "impact": "external_interaction",
                "energy_cost": 15,
                "description": "Queries a specific external JSON endpoint."
            }
        }

    def execute(self, tool_name, params=None):
        """
        The entry point for the Agent.
        """
        if tool_name not in self.registry:
            return {"status": "error", "message": f"Tool {tool_name} not found."}

        tool = self.registry[tool_name]
        try:
            result = tool["func"](params)
            return {
                "status": "success",
                "tool": tool_name,
                "output": result,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- INDIVIDUAL TOOL LOGIC ---

    def _web_search_logic(self, query):
        """
        SWAP: Replace return with a real Serper/Google API call.
        """
        if not query: return "Error: No search query provided."
        # Simulating external data retrieval
        return f"SEARCH_RESULT: The current market rate/rule for '{query}' is verified at 1.05x variance."

    def _file_write_logic(self, content):
        """
        Writes data to the agent's persistent memory log.
        """
        filename = "agent_knowledge_base.txt"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {content}\n")
        return f"Successfully wrote to {filename}"

    def _api_query_logic(self, endpoint):
        """
        Standardized external API requester.
        """
        # Mocking a JSON response
        return {"status": 200, "data": "External system heartbeat: OK"}

    def get_tool_metadata(self):
        """Helper for the World Model to understand its hands."""
        return {name: info["description"] for name, info in self.registry.items()}
      
