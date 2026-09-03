import json
import os
import time

class SystemLogger:
    def __init__(self, log_file="system_activity.log", config_path="system_config.json"):
        self.log_file = log_file
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Logger Error]: Config load failed -> {e}")
        return {}

    def log_event(self, module_name, action, level="INFO"):
        """
        Logs system events, errors, and module operations with precise timestamps.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [{module_name}] User: {self.salutation} {self.user_name} -> {action}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"[System Logger]: Entry recorded -> [{module_name}] {action}")
            return True
        except Exception as e:
            print(f"[Logger Error]: Failed to write log -> {e}")
            return False

    def get_recent_logs(self, limit=10):
        """Retrieves the most recent log entries."""
        if not os.path.exists(self.log_file):
            return []
            
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return [line.strip() for line in lines[-limit:]]
        except Exception as e:
            print(f"[Logger Error]: Failed to read logs -> {e}")
            return []

if __name__ == "__main__":
    logger = SystemLogger()
    logger.log_event("SYSTEM_CORE", "23rd Module Integration Completed", level="SUCCESS")
    print(f"[Recent Logs]: {logger.get_recent_logs(2)}")
  
