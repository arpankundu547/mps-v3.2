import json
import os
import math
from ui_theme_manager import UIThemeManager

class UIBackgroundPattern:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()
        self.canvas_width = 1920
        self.canvas_height = 1080

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Pattern Generator Error]: Config load failed -> {e}")
        return {}

    def generate_cyberpunk_grid(self, grid_spacing=40, scanline_offset=0):
        """
        Calculates dynamic canvas grid matrix and scanning lines for Cyberpunk HUD overlay.
        """
        grid_lines = []
        # Vertical grid coordinates
        for x in range(0, self.canvas_width, grid_spacing):
            grid_lines.append({"type": "vertical", "x1": x, "y1": 0, "x2": x, "y2": self.canvas_height})

        # Horizontal grid coordinates
        for y in range(0, self.canvas_height, grid_spacing):
            grid_lines.append({"type": "horizontal", "x1": 0, "y1": y, "x2": self.canvas_width, "y2": y})

        # Dynamic glowing scanline coordinate
        scanline_y = (scanline_offset * 12) % self.canvas_height
        
        return {
            "theme": "Cyberpunk",
            "stroke_color": self.active_theme.get("border", "#2A085C"),
            "glow_color": self.active_theme.get("accent", "#FF007F"),
            "grid_count": len(grid_lines),
            "active_scanline_y": scanline_y,
            "grid_matrix": grid_lines[:10]  # First 10 nodes for preview rendering
        }

    def generate_scientific_nodes(self, node_count=15, time_step=1.0):
        """
        Generates floating orbital nodes and interconnected particle pathways for Scientific HUD theme.
        """
        nodes = []
        for i in range(node_count):
            angle = (time_step * 0.1) + (i * (2 * math.pi / node_count))
            radius = 150 + (i * 10)
            cx = int((self.canvas_width / 2) + radius * math.cos(angle))
            cy = int((self.canvas_height / 2) + radius * math.sin(angle))
            nodes.append({"node_id": i, "x": cx, "y": cy, "radius": 4})

        return {
            "theme": "Scientific",
            "primary_color": self.active_theme.get("primary", "#38BDF8"),
            "background_color": self.active_theme.get("background", "#0F172A"),
            "total_nodes": len(nodes),
            "center_orbit": {"x": self.canvas_width // 2, "y": self.canvas_height // 2},
            "nodes_preview": nodes[:5]
        }

    def render_background_layout(self, frame_index=0):
        """
        Master renderer function selecting appropriate dynamic background pattern based on theme.
        """
        theme_type = self.config.get("ui_preferences", {}).get("theme", "Cyberpunk")
        print(f"\n[UI Background Pattern]: Rendering frame {frame_index} for {self.salutation} {self.user_name} ({theme_type} Mode)...")

        if theme_type == "Cyberpunk":
            pattern_data = self.generate_cyberpunk_grid(scanline_offset=frame_index)
        else:
            pattern_data = self.generate_scientific_nodes(time_step=float(frame_index))

        print(f"[Pattern Engine]: Background successfully rendered with active theme palette.")
        return pattern_data

if __name__ == "__main__":
    pattern_engine = UIBackgroundPattern()
    # Test rendering background frame
    frame_output = pattern_engine.render_background_layout(frame_index=5)
    print(f"[Output Summary]: Mode = {frame_output['theme']} | Configured Node/Grid Elements = {frame_output.get('grid_count') or frame_output.get('total_nodes')}")
  
