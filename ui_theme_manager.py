import json
import os

class UIThemeManager:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        # Color Palettes for Scientific & Cyberpunk themes
        self.themes = {
            "Scientific": {
                "background": "#0F172A",
                "card_bg": "#1E293B",
                "primary": "#38BDF8",
                "accent": "#818CF8",
                "text": "#F8FAFC",
                "border": "#334155"
            },
            "Cyberpunk": {
                "background": "#050505",
                "card_bg": "#12091B",
                "primary": "#00FF66",
                "accent": "#FF007F",
                "text": "#00F0FF",
                "border": "#2A085C"
            }
        }

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_theme(self, theme_name=None):
        """
        Retrieves color codes for selected theme (Scientific or Cyberpunk).
        """
        if not theme_name:
            theme_name = self.config.get("ui_preferences", {}).get("theme", "Cyberpunk")

        selected = self.themes.get(theme_name, self.themes["Cyberpunk"])
        print(f"[Theme Manager]: Loaded '{theme_name}' Theme for {self.salutation} {self.user_name}.")
        return selected

if __name__ == "__main__":
    theme_mgr = UIThemeManager()
    active_theme = theme_mgr.get_theme("Cyberpunk")
    print(f"[Active Palette]: {active_theme}")
  
