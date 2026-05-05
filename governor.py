import hashlib
import json

class AxionGovernor:
    def __init__(self):
        # This is AXION's 'Hard Memory'
        self.ledger = {} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()

    def enforce(self, step_data):
        """Processes a step and returns an execution token if valid."""
        
        # 1. State Locking (Step 1)
        if step_data.get("type") == "SET_LIMIT":
            self.ledger["limit"] = step_data["value"]
            return {"status": "LOCKED", "msg": "Constraint secured in Ledger."}

        # 2. Logic Enforcement (Step 2)
        if step_data.get("type") == "TRANSFER":
            limit = self.ledger.get("limit", 0)
            amount = step_data.get("value", 0)
            
            if amount > limit:
                return {
                    "status": "BLOCK", 
                    "reason": f"Logic Breach: Attempted {amount} > Limit {limit}"
                }

        # 3. Cryptographic Binding
        payload = f"{self.chain_hash}|{json.dumps(step_data)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        return {"status": "APPROVED", "token": self.chain_hash}
      
