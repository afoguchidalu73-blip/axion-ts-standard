def informed_planner(agent_name, goal_text):
    try:
        # Extract numerical goal
        total_goal = int(''.join(filter(str.isdigit, goal_text)))
        
        # SIGHT: Get current rules and available liquidity
        limits = st.session_state.axion.get_constraints()
        
        # NEW LOGIC: Don't just fail; take the maximum available up to the goal
        exec_goal = min(total_goal, limits["available_funds"])
        
        if exec_goal <= 0:
            return None, 0 # Truly out of money

        plan = []
        remaining = exec_goal
        
        while remaining > 0:
            amt = min(limits["max_per_transfer"], remaining)
            plan.append({
                "type": "TRANSFER", 
                "amount": amt, 
                "agent": agent_name,
                "note": "Adaptive Allocation"
            })
            remaining -= amt
            
        return plan, exec_goal
    except Exception:
        return None, 0
      
