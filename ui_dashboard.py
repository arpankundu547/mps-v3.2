import json
import os
from ui_theme_manager import UIThemeManager

class UIDashboard:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.theme_mgr = UIThemeManager(config_path)
        self.theme = self.theme_mgr.get_theme()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def render_dashboard(self, level=1, xp=0, rank="Novice"):
        """
        Renders the main dashboard structure and stats overview.
        """
        print(f"\n==================================================")
        print(f"       SYSTEM COMMAND CENTER - {self.salutation} {self.user_name}")
        print(f"==================================================")
        print(f" Theme Active : {self.config.get('ui_preferences', {}).get('theme', 'Cyberpunk')}")
        print(f" User Status  : {rank} (Level {level} | XP: {xp})")
        print(f" Primary Color: {self.theme['primary']} | Text: {self.theme['text']}")
        print(f"--------------------------------------------------")
        print(f" [1] Voice Viva Mode (Study)")
        print(f" [2] Fitness Pose Monitor (Vision)")
        print(f" [3] System Vault & Analytics")
        print(f" [4] Custom Settings Panel")
        print(f"==================================================\n")
        
        return {
            "status": "rendered",
            "active_user": f"{self.salutation} {self.user_name}",
            "theme": self.theme
        }

if __name__ == "__main__":
    dashboard = UIDashboard()
    dashboard.render_dashboard(level=10, xp=4500, rank="S-Class Supreme")
  
