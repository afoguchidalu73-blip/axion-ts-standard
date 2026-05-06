# tools.py
import os

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "web_search": {
                "func": self._mock_search,
                "cost": 10,
                "description": "Gather external data to reduce uncertainty"
            },
            "file_write": {
                "func": self._mock_write,
                "cost": 5,
                "description": "Persist data to long-term storage"
            }
        }

    def _mock_search(self, query):
        # In reality, this would be a Serper/Google API call
        return f"Verified data for: {query}"

    def _mock_write(self, content):
        # In reality, this would be open('log.txt', 'a').write()
        return "Success: Record Persisted"

    def execute(self, tool_name, params):
        if tool_name in self.tools:
            return self.tools[tool_name]["func"](params)
        return "Error: Tool Not Found"
      
