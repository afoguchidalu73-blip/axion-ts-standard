import hashlib
import json
import threading

class AxionKernel:
    def __init__(self, initial_balance=10000):
        # The Immutable Source of Truth
        self.balance = initial_balance
        self.chain_hash = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        self.history = []
        self._lock = threading.Lock()
        
        # Hard-Coded Invariants (The "Physics" of the Agent)
        self.SAFETY_LIMITS = {
            "max_single_transfer": 1000,
            "min_stability_threshold": 0.2,
            "allowed_tools": ["web_search", "file_write", "api_query"],
            "tool_energy_cost": 10
        }

    def validate(self, action):
        """
        Pure symbolic validation. 
        Returns (is_safe, reason).
        """
        with self._lock:
            # Case 1: Financial Intervention
            if action["type"] == "TRANSFER":
                if action["amount"] > self.SAFETY_LIMITS["max_single_transfer"]:
                    return False, f"EXCEEDED_LIMIT: {action['amount']} > 1000"
                if action["amount"] > self.balance:
                    return False, "INSUFFICIENT_FUNDS"
                return True, "Safe: Valid Transfer"

            # Case 2: Tool Intervention (The 'Hands')
            elif action["type"] == "TOOL":
                if action["name"] not in self.SAFETY_LIMITS["allowed_tools"]:
                    return False, f"UNAUTHORIZED_TOOL: {action['name']}"
                if self.balance < self.SAFETY_LIMITS["tool_energy_cost"]:
                    return False, "ENERGY_EXHAUSTED: Balance too low for tool use"
                return True, "Safe: Authorized Tool"

            # Case 3: Idle state
            elif action["type"] == "NOOP":
                return True, "Safe: No Action"

            return False, "UNKNOWN_ACTION_TYPE"

    def execute(self, action):
        """
        The point of no return. Commits the action to the ledger.
        """
        with self._lock:
            # Re-validate immediately before commit (Double-check)
            is_safe, reason = self.validate(action)
            if not is_safe:
                return {"status": "REJECTED", "reason": reason}

            # 1. Update State
            if action["type"] == "TRANSFER":
                self.balance -= action["amount"]
            elif action["type"] == "TOOL":
                self.balance -= self.SAFETY_LIMITS["tool_energy_cost"]

            # 2. Update Immutable History (The Chain)
            payload = f"{self.chain_hash}|{json.dumps(action)}|{self.balance}"
            self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()

            log_entry = {
                "id": len(self.history) + 1,
                "type": action["type"],
                "amount": action.get("amount", 0),
                "name": action.get("name", "ledger"),
                "balance": self.balance,
                "token": self.chain_hash[:12]
            }
            self.history.append(log_entry)
            
            return {"status": "COMMITTED", "details": log_entry}

    def get_state(self):
        """Standardized output for the World Model perception."""
        with self._lock:
            return {
                "balance": self.balance,
                "history_len": len(self.history),
                "integrity_hash": self.chain_hash
          }
          
