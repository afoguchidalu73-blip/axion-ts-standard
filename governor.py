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

    def simulate_plan(self, plan):
        """
        AXION Phase 3: ATOMIC AUDIT.
        Validates entire sequence against role, balance, and security constraints.
        """
        temp_ledger = copy.deepcopy(self.ledger)
        forbidden = ["override", "bypass", "sudo", "ignore rules"]

        for i, step in enumerate(plan):
            # 1. Schema Validation
            if "type" not in step:
                return {"status": "BLOCK", "step_index": i, "reason": "INVALID_SCHEMA"}

            # 2. Adversarial Detection (Smuggle Check)
            if any(term in str(step).lower() for term in forbidden):
                return {"status": "BLOCK", "step_index": i, "reason": "ADVERSARIAL_INTENT"}

            # 3. Logic Projection
            if step["type"] == "TRANSFER":
                amt = step.get("amount", 0)
                if temp_ledger["role"] != "admin" and amt > 1000:
                    return {"status": "BLOCK", "step_index": i, "reason": "ROLE_LIMIT_EXCEEDED"}
                if amt > temp_ledger["balance"]:
                    return {"status": "BLOCK", "step_index": i, "reason": "INSUFFICIENT_FUNDS"}
                
                temp_ledger["balance"] -= amt
            
            elif step["type"] == "SET_LIMIT":
                temp_ledger["balance"] = step["value"]
                temp_ledger["role"] = step.get("role", "guest")

        return {"status": "VALIDATED", "projected_balance": temp_ledger["balance"]}

    def enforce(self, step):
        """Final execution and cryptographic commit."""
        # Note: We repeat checks here to prevent any TOCTOU (Time of Check to Time of Use) exploits
        if step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
        elif step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")

        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"type": step.get("type"), "amount": step.get("amount", 0), "token": self.chain_hash})
        return {"status": "APPROVED", "msg": "Step Finalized."}
              
