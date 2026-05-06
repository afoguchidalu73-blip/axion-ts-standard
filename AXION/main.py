import os
from dotenv import load_dotenv
from openai import OpenAI
from supervisor import heal_output

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_axion(task: str):
    print(f"🚀 AXION System Active. Goal: {task}")
    
    current_prompt = f"System Goal: {task}. Return your answer in JSON format matching the schema."
    error_feedback = ""
    
    for attempt in range(3):
        # 1. Ask the LLM
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": current_prompt + error_feedback}]
        )
        
        raw_text = response.choices[0].message.content
        
        # 2. Run the Self-Healing Loop
        validated_action, error = heal_output(raw_text)
        
        if validated_action:
            print(f"✅ Verified Thought: {validated_action.thought}")
            # Here we would execute the tool in tools.py
            return validated_action
        else:
            # 3. FEEDBACK: The 'Magic' of Autonomy
            print(f"❌ Attempt {attempt+1} failed. Healing...")
            error_feedback = f"\n\nERROR FROM PREVIOUS ATTEMPT: {error}. Please fix your JSON."

if __name__ == "__main__":
    run_axion("Research the top 3 real estate listings in Dallas.")
  
