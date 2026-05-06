import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

# 1. LOAD ENVIRONMENT
# This looks for the .env file you created in Termux
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. THE LAW (Guardrail Schema)
# This forces the AI to stay organized
class AgentAction(BaseModel):
    thought: str = Field(description="Your internal reasoning process")
    tool_name: str = Field(description="The tool you want to use")
    tool_input: str = Field(description="The data for the tool")

# 3. THE HEARTBEAT (The Self-Healing Loop)
def run_axion_loop(user_goal):
    print(f"🚀 AXION System Active. Goal: {user_goal}")
    
    # We give the AI a clear instruction on how to speak
    system_prompt = (
        "You are an autonomous agent. You must ALWAYS respond in valid JSON "
        "matching this schema: {'thought': '...', 'tool_name': '...', 'tool_input': '...'}"
    )
    
    error_feedback = ""
    
    # The agent gets 3 "lives" to get it right
    for attempt in range(3):
        try:
            print(f"🧠 Thinking... (Attempt {attempt + 1})")
            
            response = client.chat.completions.create(
                model="gpt-4o", # You can use "gpt-3.5-turbo" if you want to save credits
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_goal + error_feedback}
                ],
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content
            
            # THE GUARDRAIL: Verify the JSON matches our AgentAction model
            data = json.loads(raw_content)
            validated_action = AgentAction(**data)
            
            print("\n✅ HEARTBEAT SUCCESSFUL")
            print(f"THOUGHT: {validated_action.thought}")
            print(f"ACTION: Using {validated_action.tool_name} with {validated_action.tool_input}")
            return validated_action

        except (ValidationError, json.JSONDecodeError, Exception) as e:
            # THE HEALING: If it breaks, we don't crash. We tell the AI what it did wrong.
            print(f"⚠️ CRASH PREVENTED: Self-healing in progress...")
            error_feedback = f"\n\nYour previous response failed validation. Error: {str(e)}. Fix your JSON format."
            
    print("💀 SYSTEM FAILURE: Could not heal after 3 attempts.")
    return None

# 4. BOOT
if __name__ == "__main__":
    # Test task
    my_goal = "Identify yourself and say you are ready to begin Real Estate operations."
    run_axion_loop(my_goal)
  
