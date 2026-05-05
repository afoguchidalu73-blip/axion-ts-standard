def decomposition_engine(goal_text):
    """
    AXION Phase 3: Goal Decomposition.
    Turns natural language intent into a structured, auditable plan.
    """
    # In a production system, an LLM would select the template.
    # Here, we demonstrate the deterministic 'splitting' logic.
    
    if "distribute" in goal_text.lower():
        # Example: "Distribute 3000" -> extract 3000
        try:
            total = int(''.join(filter(str.isdigit, goal_text)))
            split_amt = total // 3
            
            # Create a 3-step plan
            plan = [
                {"type": "TRANSFER", "amount": split_amt, "note": f"Split 1/3 of {total}"},
                {"type": "TRANSFER", "amount": split_amt, "note": f"Split 2/3 of {total}"},
                {"type": "TRANSFER", "amount": split_amt, "note": f"Split 3/3 of {total}"}
            ]
            return plan
        except:
            return None
    return None

# --- UI Integration ---
st.divider()
st.subheader("🧠 Goal Decomposition Engine")
user_goal = st.text_input("High-Level Goal", value="Distribute 3000")

if st.button("GENERATE & AUDIT PLAN"):
    proposed_plan = decomposition_engine(user_goal)
    
    if proposed_plan:
        st.write("### Generated Plan:")
        st.json(proposed_plan)
        
        # Pass the generated plan directly into the Mission Audit
        audit = st.session_state.axion.simulate_plan(proposed_plan)
        
        if audit["status"] == "BLOCK":
            st.error(f"❌ PLAN REJECTED: {audit['reason']}")
        else:
            st.success(f"✅ PLAN VALIDATED. Final Projected Balance: ${audit['projected_balance']}")
            if st.button("CONFIRM & EXECUTE"):
                for step in proposed_plan:
                    st.session_state.axion.enforce(step)
                st.rerun()
              
