from kernel import AxionKernel
from world_model import WorldModel
from planner import Planner
import time

# --- SETUP ---
kernel = AxionKernel(initial_balance=10000)
world = WorldModel(initial_val=10000)
planner = Planner(world)

TARGET_GOAL = 5000 
print(f"🚩 MISSION: Reach {TARGET_GOAL} with zero anomalies.\n")

# --- EXECUTION ---
for step in range(20):
    # 1. PERCEIVE (Sync world model with kernel reality)
    world.update(kernel.balance)
    
    # 2. THINK (Consult the strategist)
    action = planner.find_action(TARGET_GOAL)
    if action["type"] == "NOOP":
        print("\n✅ Goal Reached. System Idling.")
        break

    # 3. PREDICT (What should happen?)
    expected = world.predict(action)
    
    # 4. ACT (Validate and Execute via Kernel)
    is_valid, reason = kernel.validate(action) # FIX: Unpack tuple
    
    if is_valid:
        kernel.execute(action)
        
        # 5. VERIFY (The 'Aha!' Moment)
        actual = kernel.balance
        if actual != expected:
            # This is where we catch divergence
            print(f"⚠️ ANOMALY! Step {step}: Expected {expected}, got {actual}.")
        else:
            print(f"Step {step}: Action {action['type']} {action['amount']} | Balance: {actual}")
    else:
        print(f"🛡️ SAFETY BLOCK: {reason}")
        break
    
    time.sleep(0.1)
  
