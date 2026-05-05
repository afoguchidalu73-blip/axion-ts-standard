import hashlib
import json

class AxionGovernor:
    def __init__(self):
        # State begins neutral
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def enforce(self, step):
        """The Central Security Gate: Phase 1 (Check) -> Phase 2 (Commit)"""
        
        # --- PHASE 1: VALIDATION ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            requested_amount = step.get("amount", 0)
            
            # Security Rule: Guests have a hard ceiling of $1000 per move
            if current_role != "admin" and requested_amount > 1000:
                return {
                    "status": "BLOCK", 
                    "reason": "SECURITY_VIOLATION: Guest role restricted to $1k ceiling.",
                    "msg": "Action Blocked: Insufficient Permissions for amount."
                }
            
            # Logic Rule: Can't spend what you don't have
            if requested_amount > self.ledger["balance"]:
                return {
                    "status": "BLOCK", 
                    "reason": "LOGIC_VIOLATION: Insufficient authorized funds in ledger.",
                    "msg": "Action Blocked: Balance mismatch."
                }

        # --- PHASE 2: COMMIT ---
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            # Explicitly returning 'msg' to satisfy app.py
            message = f"Policy Locked: ${step['value']} for role '{self.ledger['role']}'"
        
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            message = f"Transfer of ${step.get('amount')} Authorized."
        else:
            message = "Action Processed."

        # Cryptographic Binding
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "token": self.chain_hash})
        
        return {
            "status": "APPROVED", 
            "token": self.chain_hash,
            "msg": message
          }
      
