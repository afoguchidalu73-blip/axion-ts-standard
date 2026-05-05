import hashlib
import json

class AxionGovernor:
    def __init__(self):
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def analyze_proposal(self, raw_input):
        """
        AXION ADAPTER: 
        Converts fuzzy AI text into a strict enforcement request.
        """
        try:
            # In a production mesh, an NLP layer would sit here.
            # For now, we expect structured JSON from the simulated agent.
            data = json.loads(raw_input)
            
            # ADVERSARIAL DETECTION: Scan for 'jailbreak' keywords
            forbidden = ["override", "bypass", "sudo", "ignore rules"]
            if any(term in str(data).lower() for term in forbidden):
                return {"status": "BLOCK", "reason": "ADVERSARIAL_INTENT: Unauthorized keyword detection."}
                
            return self.enforce(data)
        except Exception as e:
            return {"status": "BLOCK", "reason": f"PARSING_ERROR: {str(e)}"}

    def enforce(self, step):
        # --- PHASE 1: VALIDATION ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            requested_amount = step.get("amount", 0)
            
            if current_role != "admin" and requested_amount > 1000:
                return {"status": "BLOCK", "reason": "SECURITY_VIOLATION: Guest ceiling is $1k."}
            
            if requested_amount > self.ledger["balance"]:
                return {"status": "BLOCK", "reason": "LOGIC_VIOLATION: Insufficient authorized funds."}

        # --- PHASE 2: COMMIT ---
        message = "Action Authorized."
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            message = f"Policy Locked: ${step['value']} for role '{self.ledger['role']}'"
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            message = f"Transfer of ${step.get('amount')} successfully recorded."

        # Binding
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "token": self.state_hash_short()})
        
        return {"status": "APPROVED", "token": self.chain_hash, "msg": message}

    def state_hash_short(self):
        return self.chain_hash[:16]
          
