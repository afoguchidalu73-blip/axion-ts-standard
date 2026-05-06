import json
from schemas import AgentAction
from pydantic import ValidationError

def heal_output(raw_output: str, error_msg: str = None):
    """
    This is the self-healing loop logic. 
    It validates output or returns the error to the LLM.
    """
    try:
        # 1. Try to parse the JSON
        data = json.loads(raw_output)
        # 2. Force it through the Pydantic filter
        validated = AgentAction(**data)
        return validated, None
    except (json.JSONDecodeError, ValidationError) as e:
        # 3. Return the error trace instead of crashing
        return None, str(e)
      
