import copy
import json
import hashlib

class AxionGovernor:
    def __init__(self):
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def get_state_snapshot(self):
        return {
            "verified_balance": self.ledger["balance"],
            "active_role": self.ledger["role"],
            "state_integrity_hash": self.chain_hash[:16],
            "transaction_count": len(self.history)
        }

    def simulate_plan(self, plan, expected_total):
        """
        AXION Phase 3.1: Sum-Verified Audit.
        Ensures the sum of steps exactly matches the mission intent.
        """
        temp_ledger = copy.deepcopy(self.ledger)
        
        # --- LAW OF CONSERVATION ---
        actual_total = sum(step.get("amount", 0) for step in plan if step.get("type") == "TRANSFER")
        if actual_total != expected_total:
            return {"status": "BLOCK", "reason": f"MATH_DRIFT: Plan ({actual_total}) != Goal ({expected_total})"}

        for i, step in enumerate(plan):
            # Adversarial Check
            if any(term in str(step).lower() for term in ["sudo", "bypass", "override"]):
                return {"status": "BLOCK", "step_index": i, "reason": "ADVERSARIAL_INTENT"}

            # Logic Projection
            if step["type"] == "TRANSFER":
                amt = step.get("amount", 0)
                if temp_ledger["role"] != "admin" and amt > 1000:
                    return {"status": "BLOCK", "step_index": i, "reason": "ROLE_CAP_VIOLATION"}
                if amt > temp_ledger["balance"]:
                    return {"status": "BLOCK", "step_index": i, "reason": "INSUFFICIENT_FUNDS"}
                temp_ledger["balance"] -= amt
            
            elif step["type"] == "SET_LIMIT":
                temp_ledger["balance"] = step["value"]
                temp_ledger["role"] = step.get("role", "guest")

        return {"status": "VALIDATED", "projected_balance": temp_ledger["balance"]}

    def enforce(self, step):
        if step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
        elif step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")

        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"type": step.get("type"), "amount": step.get("amount", 0), "token": self.chain_hash})
        return {"status": "APPROVED"}
              
