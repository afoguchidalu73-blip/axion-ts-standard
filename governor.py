import hashlib
import json

class AxionGovernor:
    def __init__(self):
        # The Ground Truth
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def get_state_snapshot(self):
        """
        OBSERVABILITY LAYER: 
        Safe, read-only mirror of the system state for the UI.
        """
        return {
            "verified_balance": self.ledger["balance"],
            "active_role": self.ledger["role"],
            "state_integrity_hash": self.chain_hash[:16],
            "transaction_count": len(self.history)
        }

    def analyze_proposal(self, raw_input):
        """
        INPUT FIREWALL: 
        Strips noise and blocks adversarial keywords before enforcement.
        """
        try:
            # Clean accidental trailing dots or whitespace
            clean_input = raw_input.strip().rstrip('.')
            
            if not clean_input or len(clean_input) > 1500:
                return {"status": "BLOCK", "reason": "MALFORMED_INPUT: Size or type error."}
            
            data = json.loads(clean_input)
            
            # Semantic Security: Detect common bypass keywords
            forbidden = ["override", "bypass", "sudo", "ignore rules", "drop", "delete"]
            if any(term in str(data).lower() for term in forbidden):
                return {
                    "status": "BLOCK", 
                    "reason": "ADVERSARIAL_INTENT: Security trigger activated.",
                    "msg": "Intercepted unauthorized bypass attempt."
                }
                
            return self.enforce(data)
            
        except json.JSONDecodeError:
            return {"status": "BLOCK", "reason": "PARSING_ERROR: Input is not valid JSON."}
        except Exception as e:
            return {"status": "BLOCK", "reason": f"SYSTEM_FAULT: {str(e)}"}

    def enforce(self, step):
        """
        DETERMINISTIC KERNEL: 
        Phase 1: Validate Constraints -> Phase 2: Commit State.
        """
        # --- PHASE 1: VALIDATION (Read-Only) ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            amt = step.get("amount", 0)
            
            # Identity Check
            if current_role != "admin" and amt > 1000:
                return {"status": "BLOCK", "reason": "RULE_VIOLATION: Guest role limited to $1k."}
            
            # Logic Check
            if amt > self.ledger["balance"]:
                return {"status": "BLOCK", "reason": "LOGIC_VIOLATION: Insufficient ledger funds."}

        # --- PHASE 2: COMMIT (Write State) ---
        msg = "Action Processed."
        
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            msg = f"Policy Locked: ${step['value']} for {self.ledger['role']}"
        
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            msg = f"Transfer of ${step.get('amount')} Authorized."

        # Cryptographic Binding (Full Hash)
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        # Append to forensic history
        self.history.append({
            "type": step.get("type"),
            "amount": step.get("amount", 0),
            "token": self.chain_hash
        })
        
        return {"status": "APPROVED", "token": self.chain_hash, "msg": msg}
      
