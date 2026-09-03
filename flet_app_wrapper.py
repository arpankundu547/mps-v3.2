import json
import os
import sys
from ui_theme_manager import UIThemeManager
from security_guard import SecurityGuard

class FletAppWrapper:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        # Load theme and security services
        self.theme_mgr = UIThemeManager(config_path)
        self.security = SecurityGuard(config_path)
        self.active_theme = self.theme_mgr.get_theme()
        
        self.app_state = {
            "authenticated": False,
            "current_screen": "LOCK_SCREEN",
            "active_user": f"{self.salutation} {self.user_name}"
        }

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Wrapper Error]: Failed to load config -> {e}")
        return {}

    def authenticate_user(self, pin):
        """Validates PIN entry and updates app UI state."""
        print(f"\n[Flet App UI]: PIN Authentication requested by {self.user_name}...")
        if self.security.verify_pin(pin):
            self.app_state["authenticated"] = True
            self.app_state["current_screen"] = "MAIN_DASHBOARD"
            print(f"[Flet App UI]: Access Granted -> Navigating to {self.app_state['current_screen']}")
            return True
        else:
            self.app_state["authenticated"] = False
            print(f"[Flet App UI]: Authentication Failed -> Remaining on {self.app_state['current_screen']}")
            return False

    def get_ui_layout_config(self):
        """
        Provides complete layout JSON specs for Flet framework rendering.
        """
        if not self.app_state["authenticated"]:
            return {
                "screen": "LockScreen",
                "bg_color": self.active_theme["background"],
                "card_color": self.active_theme["card_bg"],
                "accent_color": self.active_theme["accent"],
                "elements": ["PIN_Input_Field", "Unlock_Button", "Status_Message"]
            }
        
        return {
            "screen": "DashboardScreen",
            "bg_color": self.active_theme["background"],
            "primary_color": self.active_theme["primary"],
            "text_color": self.active_theme["text"],
            "elements": [
                "Header_User_Banner",
                "Voice_Viva_Section",
                "Pose_Check_Section",
                "Settings_Access_Button",
                "System_Vault_Analytics"
            ]
        }

if __name__ == "__main__":
    app_wrapper = FletAppWrapper()
    # Test authentication flow
    if app_wrapper.authenticate_user("1234"):
        layout = app_wrapper.get_ui_layout_config()
        print(f"[UI Layout Config Loaded]: Screen = {layout['screen']}")
      
