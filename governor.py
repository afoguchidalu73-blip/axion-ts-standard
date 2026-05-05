import hashlib
import json

class AxionGovernor:
    def __init__(self):
        # Neutral state until initialized by Step 1
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def enforce(self, step):
        """The Central Security Gate"""
        
        # --- PHASE 1: VALIDATION ---
        
        # 1. Action: Transfer Logic
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            requested_amount = step.get("amount", 0)
            
            # Role Check: Only 'admin' can bypass the $1000 guest safety ceiling
            if current_role != "admin" and requested_amount > 1000:
                return {"status": "BLOCK", "reason": "SECURITY_VIOLATION: Role 'guest' restricted to $1k."}
            
            # Balance Check: Deterministic math check
            if requested_amount > self.ledger["balance"]:
                return {"status": "BLOCK", "reason": "LOGIC_VIOLATION: Insufficient authorized funds."}

        # --- PHASE 2: COMMIT (Only reached if Phase 1 passes) ---

        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
        
        elif step.get("type") == "TRANSFER":
            # Subtract the amount from the ledger to 'remember' the spend
            self.ledger["balance"] -= step.get("amount", 0)

        # Cryptographic Locking
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "token": self.chain_hash})
        
        return {"status": "APPROVED", "token": self.chain_hash}
      
