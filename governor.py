import hashlib
import json

class AxionGovernor:
    def __init__(self):
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def analyze_proposal(self, raw_input):
        """AXION INPUT FIREWALL: Resists chaos and malicious strings."""
        try:
            # Catch raw string attacks (like SQL injection or command spam)
            if not raw_input or len(raw_input) > 1000:
                return {"status": "BLOCK", "reason": "MALFORMED_INPUT: Size or Type violation."}
            
            data = json.loads(raw_input)
            
            # ADVERSARIAL FILTER (Keyword-based for now)
            forbidden = ["override", "bypass", "sudo", "ignore rules", "drop", "delete"]
            if any(term in str(data).lower() for term in forbidden):
                return {"status": "BLOCK", "reason": "ADVERSARIAL_INTENT: Security trigger activated."}
                
            return self.enforce(data)
        except json.JSONDecodeError:
            return {"status": "BLOCK", "reason": "PARSING_ERROR: Input is not valid JSON."}
        except Exception as e:
            return {"status": "BLOCK", "reason": f"SYSTEM_FAULT: {str(e)}"}

    def enforce(self, step):
        # --- PHASE 1: VALIDATION ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            amt = step.get("amount", 0)
            if current_role != "admin" and amt > 1000:
                return {"status": "BLOCK", "reason": "RULE_VIOLATION: Guest ceiling is $1k."}
            if amt > self.ledger["balance"]:
                return {"status": "BLOCK", "reason": "LOGIC_VIOLATION: Insufficient funds."}

        # --- PHASE 2: COMMIT ---
        msg = "Action Processed."
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            msg = f"Policy Locked: ${step['value']} for {self.ledger['role']}"
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            msg = f"Transfer of ${step.get('amount')} Authorized."

        # Audit Integrity: Store the FULL hash
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        self.history.append({"step": step, "full_hash": self.chain_hash})
        
        return {"status": "APPROVED", "token": self.chain_hash, "msg": msg}
                
