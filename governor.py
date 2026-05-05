import hashlib
import json

class AxionGovernor:
    def __init__(self):
        # Starts in a neutral state; must be initialized via SET_LIMIT
        self.ledger = {"balance": 0, "role": None} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []

    def analyze_proposal(self, raw_input):
        """
        INPUT FIREWALL: Strips noise and checks for adversarial intent 
        before passing to the enforcement engine.
        """
        try:
            # 1. Clean noise (Removes accidental trailing periods or whitespace)
            clean_input = raw_input.strip().rstrip('.')
            
            if not clean_input or len(clean_input) > 1500:
                return {"status": "BLOCK", "reason": "MALFORMED_INPUT: Payload size or type error."}
            
            # 2. Parse JSON
            data = json.loads(clean_input)
            
            # 3. Adversarial Filter: Detect attempts to bypass the governor
            forbidden = ["override", "bypass", "sudo", "ignore rules", "drop", "delete"]
            if any(term in str(data).lower() for term in forbidden):
                return {
                    "status": "BLOCK", 
                    "reason": "ADVERSARIAL_INTENT: Unauthorized security keywords detected.",
                    "msg": "Security trigger: Intervention required."
                }
                
            return self.enforce(data)
            
        except json.JSONDecodeError:
            return {"status": "BLOCK", "reason": "PARSING_ERROR: Input is not a valid JSON object."}
        except Exception as e:
            return {"status": "BLOCK", "reason": f"SYSTEM_FAULT: {str(e)}"}

    def enforce(self, step):
        """
        DETERMINISTIC KERNEL: Enforces RBAC and Numeric Invariants.
        """
        # --- PHASE 1: VALIDATION (Read-Only) ---
        if step.get("type") == "TRANSFER":
            current_role = self.ledger.get("role")
            amt = step.get("amount", 0)
            
            # Identity Constraint: Guest ceiling
            if current_role != "admin" and amt > 1000:
                return {
                    "status": "BLOCK", 
                    "reason": f"RULE_VIOLATION: Role '{current_role}' limited to $1k per move.",
                    "msg": "Authorization Denied."
                }
            
            # Numeric Invariant: Ledger balance
            if amt > self.ledger["balance"]:
                return {
                    "status": "BLOCK", 
                    "reason": "LOGIC_VIOLATION: Amount exceeds verified ledger balance.",
                    "msg": "Transaction Blocked: Insufficient Funds."
                }

        # --- PHASE 2: COMMIT (Write State) ---
        msg = "Action Processed."
        
        if step.get("type") == "SET_LIMIT":
            self.ledger["balance"] = step["value"]
            self.ledger["role"] = step.get("role", "guest")
            msg = f"Policy Locked: ${step['value']} for role '{self.ledger['role']}'"
        
        elif step.get("type") == "TRANSFER":
            self.ledger["balance"] -= step.get("amount", 0)
            msg = f"Transfer of ${step.get('amount')} Authorized."

        # 4. Cryptographic Binding: Lock the session history
        payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
        self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        # Store full audit trace
        self.history.append({
            "step": step.get("type"),
            "amount": step.get("amount", 0),
            "token": self.chain_hash
        })
        
        return {
            "status": "APPROVED", 
            "token": self.chain_hash,
            "msg": msg
      }
      
