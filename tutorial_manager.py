import json
import os

class TutorialManager:
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

    def get_tutorial(self, feature_name):
        """
        Provides short 5-15 second visual/text guidance for system modules.
        """
        tutorials = {
            "viva": "Speak clearly for 2 minutes explaining the core theory (e.g., Auditing/Vouching). The AI Judge will score your accuracy.",
            "pose": "Position camera at a 45-degree angle. Maintain form during workouts for posture validation.",
            "boss_exam": "Boss Levels trigger every 10 levels. Complete both study viva and fitness tests to unlock the next rank."
        }
        
        guide = tutorials.get(feature_name.lower(), "No specific tutorial found. Follow standard instructions.")
        print(f"\n[Tutorial Manager]: Loading guide for {self.salutation} {self.user_name} -> Task: {feature_name}")
        print(f"[Instruction]: {guide}\n")
        return guide

if __name__ == "__main__":
    manager = TutorialManager()
    manager.get_tutorial("viva")
  
