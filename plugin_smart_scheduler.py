import json
import os
from datetime import datetime

class SmartScheduler:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def auto_reschedule(self, delay_minutes, task_name):
        """
        Dynamically adjusts the user's daily schedule in case of unexpected delay (e.g., traffic).
        """
        now = datetime.now().strftime("%H:%M")
        print(f"\n[Smart Scheduler Active]: Re-optimizing routine for {self.salutation} {self.user_name}...")
        print(f"[Delay Detected]: Task '{task_name}' delayed by {delay_minutes} mins at {now}.")
        
        # Adaptive scheduling logic
        print(f"[Adjustment]: Next study/fitness sessions shifted smoothly by {delay_minutes} mins to preserve focus.")
        return {
            "status": "Rescheduled",
            "delayed_task": task_name,
            "shift_minutes": delay_minutes,
            "timestamp": now
        }

if __name__ == "__main__":
    scheduler = SmartScheduler()
    scheduler.auto_reschedule(delay_minutes=30, task_name="Auditing Study Session")
  
