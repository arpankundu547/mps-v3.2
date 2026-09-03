import json
import os
from ui_theme_manager import UIThemeManager

class UICustomSlider:
    def __init__(self, min_val=0, max_val=100, default_val=50, label="Custom Slider", config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.current_val = float(default_val)
        self.label = label
        
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Slider Error]: Config load failed -> {e}")
        return {}

    def set_value(self, new_val):
        """Sets slider value within valid range limits."""
        if new_val < self.min_val:
            self.current_val = self.min_val
        elif new_val > self.max_val:
            self.current_val = self.max_val
        else:
            self.current_val = float(new_val)
            
        percentage = round(((self.current_val - self.min_val) / (self.max_val - self.min_val)) * 100, 2)
        print(f"[UI Custom Slider]: '{self.label}' adjusted to {self.current_val} ({percentage}%) for {self.salutation} {self.user_name}.")
        return self.current_val

    def render_slider_properties(self):
        """Returns visual configuration properties for Flet GUI rendering."""
        percentage = round(((self.current_val - self.min_val) / (self.max_val - self.min_val)) * 100, 2)
        return {
            "label": self.label,
            "min": self.min_val,
            "max": self.max_val,
            "value": self.current_val,
            "percentage": percentage,
            "track_color": self.active_theme.get("border", "#334155"),
            "fill_color": self.active_theme.get("primary", "#00FF66"),
            "thumb_color": self.active_theme.get("accent", "#FF007F")
        }

if __name__ == "__main__":
    slider = UICustomSlider(min_val=0, max_val=100, default_val=75, label="Voice Recognition Sensitivity")
    slider.set_value(85)
    properties = slider.render_slider_properties()
    print(f"[Slider Layout Properties]: {properties}")
  
