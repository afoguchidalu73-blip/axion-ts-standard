import hashlib
import json

class AxionGovernor:
    def __init__(self):
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def enforce(self, step):
        # --- PHASE 1: VALIDATION ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            requested_amount = step.get("amount", 0)
            
            if current_role != "admin" and requested_amount > 1000:
                return {
                    "status": "BLOCK", 
                    "reason": "SECURITY_VIOLATION: Guest role restricted to $1k ceiling.",
                    "msg": "Action Blocked: Insufficient Permissions."
                }
            
            if requested_amount > self.ledger["balance"]:
                return {
                    "status": "BLOCK", 
                    "reason": "LOGIC_VIOLATION: Insufficient authorized funds.",
                    "msg": "Action Blocked: Balance mismatch."
                }

        # --- PHASE 2: COMMIT ---
        message = "Action Processed." # Default message
        
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            message = f"Policy Locked: ${step['value']} for role '{self.ledger['role']}'"
        
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            message = f"Transfer of ${step.get('amount')} Authorized."

        # Cryptographic Binding
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "token": self.chain_hash})
        
        return {
            "status": "APPROVED", 
            "token": self.chain_hash,
            "msg": message
          }
      
