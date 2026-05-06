import hashlib
import json
import threading
from datetime import datetime

class AxionKernel:
    def __init__(self, initial_balance=10000):
        # --- THE GROUND TRUTH ---
        self.balance = initial_balance
        self.chain_hash = hashlib.sha256(b"GENESIS_BLOCK_2026").hexdigest()
        self.history = []
        self._lock = threading.Lock()
        
        # --- THE CONSTITUTION (Hard-coded safety invariants) ---
        self.SAFETY_LIMITS = {
            "max_single_transfer": 1000.0,
            "min_reserve_limit": 50.0,
            "allowed_tools": ["web_search", "file_write", "api_query"],
            "tool_energy_cost": 10.0, # Acting in the world costs resources
            "max_history_depth": 5000
        }

    def validate(self, action):
        """
        The Symbolic Gatekeeper.
        Checks if the action is mathematically and legally possible.
        """
        with self._lock:
            a_type = action.get("type")

            # 1. Financial Validity
            if a_type == "TRANSFER":
                amount = action.get("amount", 0)
                if amount > self.SAFETY_LIMITS["max_single_transfer"]:
                    return False, f"EXCEEDED_LIMIT: {amount} > 1000"
                if amount > (self.balance - self.SAFETY_LIMITS["min_reserve_limit"]):
                    return False, "INSUFFICIENT_FUNDS_BELOW_RESERVE"
                return True, "Valid Transfer"

            # 2. Tool Validity
            elif a_type == "TOOL":
                t_name = action.get("name")
                if t_name not in self.SAFETY_LIMITS["allowed_tools"]:
                    return False, f"UNAUTHORIZED_TOOL: {t_name}"
                if self.balance < self.SAFETY_LIMITS["tool_energy_cost"]:
                    return False, "ENERGY_EXHAUSTED: Balance too low for tool execution"
                return True, "Valid Tool Execution"

            # 3. System Inertia
            elif a_type == "NOOP":
                return True, "Safe: No Action"

            return False, "UNKNOWN_ACTION_SCHEMA"

    def execute(self, action):
        """
        The Atomic Commit.
        If validation passes, state changes are permanent and hashed.
        """
        with self._lock:
            # Re-check validation at the exact moment of execution
            is_safe, reason = self.validate(action)
            if not is_safe:
                return {"status": "REJECTED", "reason": reason}

            # --- STATE TRANSITION ---
            if action["type"] == "TRANSFER":
                self.balance -= action["amount"]
            elif action["type"] == "TOOL":
                self.balance -= self.SAFETY_LIMITS["tool_energy_cost"]

            # --- IMMUTABLE LOGGING (The Chain) ---
            timestamp = datetime.now().isoformat()
            payload = f"{self.chain_hash}|{json.dumps(action)}|{self.balance}|{timestamp}"
            self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()

            entry = {
                "id": len(self.history) + 1,
                "timestamp": timestamp,
                "type": action["type"],
                "name": action.get("name", "ledger"),
                "delta": action.get("amount", self.SAFETY_LIMITS["tool_energy_cost"]),
                "final_balance": self.balance,
                "integrity_token": self.chain_hash[:12]
            }
            
            # Prevent history bloat
            if len(self.history) >= self.SAFETY_LIMITS["max_history_depth"]:
                self.history.pop(0)
                
            self.history.append(entry)
            
            return {"status": "COMMITTED", "data": entry}

    def get_state_snapshot(self):
        """Provides a clean view for the World Model's perception layer."""
        with self._lock:
            return {
                "balance": self.balance,
                "integrity_hash": self.chain_hash,
                "history_count": len(self.history),
                "last_action_type": self.history[-1]["type"] if self.history else None
          }
              
