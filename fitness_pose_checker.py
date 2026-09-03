import json
import os

class FitnessPoseChecker:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.target_angle = 45.0  # Default pose requirement
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

    def analyze_camera_pose(self, detected_angle):
        """
        Analyzes real-time camera pose angle for workouts.
        Ensures strict angle checking without physical strain.
        """
        print(f"[Pose Vision Active]: Monitoring posture for {self.salutation} {self.user_name}...")
        
        accuracy = round(100.0 - abs(self.target_angle - detected_angle), 2)
        if accuracy < 0:
            accuracy = 0.0

        is_correct = accuracy >= 85.0
        status = "PERFECT POSTURE" if is_correct else "INCORRECT ANGLE - ADJUST FORM"

        print(f"[Vision Feedback]: Angle = {detected_angle}° | Accuracy = {accuracy}% | Status: {status}")
        return {
            "detected_angle": detected_angle,
            "accuracy": accuracy,
            "is_correct": is_correct
        }

if __name__ == "__main__":
    checker = FitnessPoseChecker()
    checker.analyze_camera_pose(detected_angle=44.5)
  
