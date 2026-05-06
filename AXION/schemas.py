from pydantic import BaseModel, Field
from typing import List, Optional

class AgentAction(BaseModel):
    """The strict format for every action the agent takes."""
    thought: str = Field(description="The agent's internal reasoning.")
    tool_name: str = Field(description="Which tool to use (e.g., 'write_file').")
    tool_input: dict = Field(description="The parameters for the tool.")
    is_final: bool = Field(default=False, description="Set to True if task is finished.")
  
