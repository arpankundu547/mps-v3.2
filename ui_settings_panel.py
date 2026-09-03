import json
import os
from security_guard import SecurityGuard

class UISettingsPanel:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.security = SecurityGuard(config_path)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def update_theme_preference(self, pin_input, new_theme):
        """
        Updates system theme (Scientific/Cyberpunk) after PIN verification.
        """
        print(f"\n[Settings Panel]: Change Theme Request Initiated...")
        if not self.security.verify_pin(pin_input):
            print("[Settings Error]: Access Denied. Cannot modify preferences.")
            return False

        if new_theme not in ["Scientific", "Cyberpunk"]:
            print(f"[Settings Error]: Invalid theme '{new_theme}'. Choose 'Scientific' or 'Cyberpunk'.")
            return False

        if "ui_preferences" not in self.config:
            self.config["ui_preferences"] = {}

        self.config["ui_preferences"]["theme"] = new_theme

        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            print(f"[Settings Updated]: Theme changed to '{new_theme}' for {self.salutation} {self.user_name}.")
            return True
        except Exception as e:
            print(f"[Settings Save Error]: {e}")
            return False

if __name__ == "__main__":
    settings = UISettingsPanel()
    # Test updating theme with correct PIN
    settings.update_theme_preference(pin_input="1234", new_theme="Scientific")
  
