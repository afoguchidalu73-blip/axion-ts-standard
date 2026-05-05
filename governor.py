import copy
import json
import hashlib

class AxionGovernor:
    def __init__(self):
        # State Law
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def get_constraints(self):
        """
        AXION Phase 4: READ-ONLY contract for the Planner.
        Allows the planner to see the walls before hitting them.
        """
        role = self.ledger.get("role", "guest")
        # Deterministic Rule Mapping
        return {
            "role": role,
            "max_per_transfer": 500 if role == "guest" else 1000 if role == "admin" else 100,
            "balance": self.ledger.get("balance", 0)
        }

    def get_state_snapshot(self):
        return {
            "verified_balance": self.ledger["balance"],
            "active_role": self.ledger["role"],
            "state_integrity_hash": self.chain_hash[:16],
            "transaction_count": len(self.history)
        }

    def simulate_plan(self, plan, expected_total):
        """
        AXION Phase 3.1 & 4: PRE-EXECUTION SIMULATION.
        Ensures the future state is valid before the present is modified.
        """
        temp_ledger = copy.deepcopy(self.ledger)
        forbidden = ["sudo", "bypass", "override", "ignore"]
        
        # 1. Sum-Verification Law (Conservation of Value)
        actual_total = sum(step.get("amount", 0) for step in plan if step.get("type") == "TRANSFER")
        if actual_total != expected_total:
            return {"status": "BLOCK", "reason": f"MATH_DRIFT: Plan ({actual_total}) != Goal ({expected_total})"}

        for i, step in enumerate(plan):
            # 2. Adversarial Smuggle Check
            if any(term in str(step).lower() for term in forbidden):
                return {"status": "BLOCK", "step_index": i, "reason": "ADVERSARIAL_INTENT"}

            # 3. Constraint Projection
            if step["type"] == "TRANSFER":
                amt = step.get("amount", 0)
                # Check against the temporary state created by previous steps
                constraints = self.get_constraints() # Dynamic lookup based on temp_ledger in real logic, here simplified
                
                # Rule enforcement
                if temp_ledger["role"] == "guest" and amt > 500:
                    return {"status": "BLOCK", "step_index": i, "reason": "ROLE_CAP_VIOLATION"}
                if amt > temp_ledger["balance"]:
                    return {"status": "BLOCK", "step_index": i, "reason": "INSUFFICIENT_FUNDS"}
                
                temp_ledger["balance"] -= amt
            
            elif step["type"] == "SET_LIMIT":
                temp_ledger["balance"] = step["value"]
                temp_ledger["role"] = step.get("role", "guest")

        return {"status": "VALIDATED", "projected_balance": temp_ledger["balance"]}

    def enforce(self, step):
        """
        Phase 1 Core: Execution and Cryptographic Commitment.
        """
        if step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
        elif step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")

        # Hash-Chain Binding
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        self.history.append({
            "step": len(self.history) + 1,
            "type": step.get("type"),
            "amount": step.get("amount", 0),
            "token": self.chain_hash[:16]
        })
        return {"status": "APPROVED"}
                            
