import copy
import json
import hashlib
import threading

class AxionKernel:
    def __init__(self):
        # Current State
        self.ledger = {"balance": 10000, "role": "admin"} 
        self.chain_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self.history = []
        
        # 🔒 Concurrency Control
        self._lock = threading.Lock()
        self.pending_reservations = 0

    def get_constraints(self):
        """Phase 4 Sight: Returns read-only rules and available liquidity."""
        with self._lock:
            available = self.ledger["balance"] - self.pending_reservations
            return {
                "role": self.ledger["role"],
                "max_per_transfer": 1000 if self.ledger["role"] == "admin" else 500,
                "available_funds": max(0, available),
                "total_ledger": self.ledger["balance"]
            }

    def request_reservation(self, amount):
        """Phase 5 Atomic Gate: Checks and locks funds in one operation."""
        with self._lock:
            available = self.ledger["balance"] - self.pending_reservations
            if amount > available:
                return False
            self.pending_reservations += amount
            return True

    def release_reservation(self, amount):
        """Lifecycle Cleanup: Ensures money doesn't 'evaporate' if an agent fails."""
        with self._lock:
            self.pending_reservations = max(0, self.pending_reservations - amount)

    def simulate_plan(self, plan, expected_total):
        """Audit logic (Simplified for this version - verify sum and constraints)."""
        actual_total = sum(s.get("amount", 0) for s in plan if s.get("type") == "TRANSFER")
        if actual_total != expected_total:
            return {"status": "BLOCK", "reason": "SUM_MISMATCH"}
        return {"status": "VALIDATED"}

    def enforce_atomic(self, step):
        """Phase 1 Commit: Writes to the permanent ledger."""
        with self._lock:
            if step.get("type") == "TRANSFER":
                self.ledger["balance"] -= step.get("amount", 0)
            elif step.get("type") == "SET_LIMIT":
                self.ledger["balance"] = step["value"]
                self.ledger["role"] = step.get("role", "guest")

            # Cryptographic Fingerprint
            payload = f"{self.chain_hash}|{json.dumps(step)}|{json.dumps(self.ledger)}"
            self.chain_hash = hashlib.sha256(payload.encode()).hexdigest()
            
            self.history.append({
                "agent": step.get("agent", "unknown"),
                "type": step.get("type"),
                "amount": step.get("amount", 0),
                "token": self.chain_hash[:12]
            })
              
