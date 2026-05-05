import hashlib
import json

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

    def analyze_proposal(self, raw_input):
        try:
            data = json.loads(raw_input)
            
            # --- SECURITY LAYER: REPAIRABLE ADVERSARIAL INTENT ---
            forbidden = ["sudo", "override", "bypass"]
            if any(term in str(data).lower() for term in forbidden):
                return {
                    "status": "BLOCK", 
                    "reason": "ADVERSARIAL_INTENT",
                    "repair": {"action": "REMOVE_UNSAFE_FIELD", "field": "note"}
                }
                
            return self.enforce(data)
        except Exception:
            return {"status": "BLOCK", "reason": "PARSING_ERROR"}

    def enforce(self, step):
        if step.get("type") == "TRANSFER":
            amt = step.get("amount", 0)
            balance = self.ledger["balance"]
            
            # Constraint 1: Role-based cap
            if self.ledger["role"] != "admin" and amt > 1000:
                return {
                    "status": "BLOCK", 
                    "reason": "ROLE_LIMIT_EXCEEDED",
                    "repair": {"action": "ADJUST_AMOUNT", "max_allowed": 1000}
                }
            
            # Constraint 2: Ledger depth
            if amt > balance:
                return {
                    "status": "BLOCK", 
                    "reason": "INSUFFICIENT_FUNDS",
                    "repair": {"action": "ADJUST_AMOUNT", "max_allowed": balance}
                }

        # --- COMMIT PHASE ---
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)

        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"type": step.get("type"), "amount": step.get("amount", 0), "token": self.chain_hash})
        
        return {"status": "APPROVED", "token": self.chain_hash, "msg": "Target State Achieved."}
              
