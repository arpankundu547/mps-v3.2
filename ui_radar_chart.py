import json
import os
import math
from ui_theme_manager import UIThemeManager

class UIRadarChart:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()
        self.center_x = 200
        self.center_y = 200
        self.radius = 150

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Radar Chart Error]: Config load failed -> {e}")
        return {}

    def calculate_polygon_points(self, metrics):
        """
        Calculates geometric coordinates for Radar Chart rendering based on performance scores.
        Expected metrics input format: {'Auditing': 90, 'Fitness': 85, 'Consistency': 95, 'Focus': 80, 'Speed': 88}
        """
        num_axes = len(metrics)
        if num_axes < 3:
            print("[Radar Chart Warning]: Minimum 3 axes required for a valid polygon radar chart.")
            return []

        points = []
        angle_slice = (2 * math.pi) / num_axes
        
        for i, (key, value) in enumerate(metrics.items()):
            # Normalize value to scale between 0 and 1
            score = min(max(value, 0), 100) / 100.0
            angle = (i * angle_slice) - (math.pi / 2)  # Start from top axis
            
            x = self.center_x + (self.radius * score * math.cos(angle))
            y = self.center_y + (self.radius * score * math.sin(angle))
            
            points.append({
                "axis_label": key,
                "score_percent": value,
                "x": round(x, 2),
                "y": round(y, 2)
            })

        return points

    def generate_chart_config(self, metrics=None):
        """
        Generates full vector chart render specifications for Flet Canvas UI.
        """
        if not metrics:
            metrics = {
                "Audit Theory": 92,
                "Viva Expression": 88,
                "Posture Form": 85,
                "Consistency": 95,
                "Boss Level Accuracy": 90
            }

        polygon_points = self.calculate_polygon_points(metrics)
        print(f"\n[UI Radar Chart Engine]: Radar geometry mapped for {self.salutation} {self.user_name}.")
        print(f"[Metrics Analyzed]: {len(metrics)} Attributes Processed.")

        return {
            "chart_type": "Radar_Spider_Chart",
            "theme_colors": {
                "line_color": self.active_theme.get("primary", "#00FF66"),
                "fill_color": self.active_theme.get("accent", "#FF007F"),
                "grid_color": self.active_theme.get("border", "#2A085C")
            },
            "center": {"x": self.center_x, "y": self.center_y},
            "radius": self.radius,
            "axes_nodes": polygon_points
        }

if __name__ == "__main__":
    radar_engine = UIRadarChart()
    chart_specs = radar_engine.generate_chart_config()
    print(f"[Chart Render Config Preview]: Center = {chart_specs['center']} | Nodes = {chart_specs['axes_nodes'][:2]}")
              
