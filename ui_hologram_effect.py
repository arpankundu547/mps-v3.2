import json
import os
import math
from ui_theme_manager import UIThemeManager

class UIHologramEffect:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()
        self.hologram_active = True

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Hologram Engine Error]: Config load failed -> {e}")
        return {}

    def generate_hologram_projection(self, target_widget="HUD_DISPLAY", pulse_phase=0.0):
        """
        Generates flickering hologram projection vectors and glow matrix for Cyberpunk HUD.
        """
        flicker_intensity = round(0.85 + (0.15 * math.sin(pulse_phase * 3.1415)), 3)
        glow_radius = int(12 + (5 * math.cos(pulse_phase)))
        
        projection_data = {
            "target": target_widget,
            "flicker_alpha": flicker_intensity,
            "glow_radius_px": glow_radius,
            "scan_line_frequency": 120,
            "chromatic_aberration_offset": 2.5,
            "colors": {
                "core_glow": self.active_theme.get("primary", "#00FF66"),
                "flicker_edge": self.active_theme.get("accent", "#FF007F"),
                "projection_beam": self.active_theme.get("border", "#2A085C")
            }
        }
        
        print(f"\n[Hologram Engine]: Projection active for {self.salutation} {self.user_name} on {target_widget}.")
        print(f"[Projection Metrics]: Alpha = {flicker_intensity} | Glow Radius = {glow_radius}px")
        return projection_data

if __name__ == "__main__":
    hologram = UIHologramEffect()
    effect = hologram.generate_hologram_projection("AI_AVATAR_CARD", pulse_phase=1.57)
    print(f"[Hologram Projection Config]: {effect}")
  
