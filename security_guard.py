import json
import os
import hashlib

class SecurityGuard:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        # Default stored PIN hash (1234 by default if not set in config)
        self.stored_pin_hash = self.config.get("security", {}).get("pin_hash", self._hash_pin("1234"))

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _hash_pin(self, pin_str):
        """Hashes the input PIN for secure storage and comparison."""
        return hashlib.sha256(pin_str.encode("utf-8")).hexdigest()

    def verify_pin(self, input_pin):
        """
        Validates user PIN authentication before allowing access to sensitive panels.
        """
        hashed_input = self._hash_pin(str(input_pin))
        if hashed_input == self.stored_pin_hash:
            print(f"[Security Guard]: Access GRANTED to {self.salutation} {self.user_name}.")
            return True
        else:
            print(f"[Security Guard]: Access DENIED. Invalid PIN input.")
            return False

if __name__ == "__main__":
    guard = SecurityGuard()
    # Test PIN authentication
    guard.verify_pin("1234")
  
