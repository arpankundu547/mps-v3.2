import json
import os
from ui_theme_manager import UIThemeManager

class UIGlassMorphism:
    def __init__(self, blur_radius=15, opacity=0.6, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.blur_radius = blur_radius
        self.opacity = opacity
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Glassmorphism Error]: Config load failed -> {e}")
        return {}

    def get_glass_card_style(self, border_width=1.5):
        """
        Generates dynamic backdrop-filter and translucency specs for Flet UI components.
        """
        card_color = self.active_theme.get("card_bg", "#12091B")
        border_color = self.active_theme.get("border", "#2A085C")
        
        style = {
            "backdrop_blur": f"{self.blur_radius}px",
            "background_color": card_color,
            "opacity": self.opacity,
            "border_color": border_color,
            "border_width": f"{border_width}px",
            "border_radius": "16px",
            "box_shadow": f"0 8px 32px 0 rgba(0, 0, 0, 0.37)"
        }
        
        print(f"[Glassmorphism Engine]: Rendered blur filter ({self.blur_radius}px) for {self.salutation} {self.user_name}.")
        return style

if __name__ == "__main__":
    glass_engine = UIGlassMorphism(blur_radius=20, opacity=0.7)
    style_specs = glass_engine.get_glass_card_style()
    print(f"[Glass UI Style Specs]: {style_specs}")
  
