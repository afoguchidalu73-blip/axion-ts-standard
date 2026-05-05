import hashlib
import json

class AxionGovernor:
    def __init__(self):
        self.ledger = {"balance": 0, "role": "guest"} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def enforce(self, step):
        """The Central Security Gate"""
        
        # 1. Permission Check: Can this role even perform this action?
        if step.get("type") == "TRANSFER":
            if self.ledger["role"] != "admin" and step.get("amount", 0) > 1000:
                return {"status": "BLOCK", "reason": "UNAUTHORIZED: Only Admins can exceed $1k."}
            
            # 2. Logic Check: Does the math work based on the PAST steps?
            if step.get("amount", 0) > self.ledger["balance"]:
                return {"status": "BLOCK", "reason": "INSUFFICIENT_FUNDS: Logic breach."}

        # 3. State Locking: Update the ledger if approved
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            
        # 4. Cryptographic Binding: Lock the new state to the old one
        payload = f"{self.chain_hash}|{json.dumps(step)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "token": self.chain_hash})
        
        return {"status": "APPROVED", "token": self.chain_hash}
      
