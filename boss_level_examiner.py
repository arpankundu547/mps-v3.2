import json
import os

class BossLevelExaminer:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.milestones = self.config.get("progression_parameters", {}).get("boss_level_milestones", [10, 20, 30, 50, 100])

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def is_boss_level(self, current_level):
        """Checks if the current level triggers a Boss Exam."""
        return current_level in self.milestones

    def execute_boss_exam(self, level, viva_accuracy, fitness_accuracy):
        """
        Executes comprehensive Boss Level Exam combining study viva performance and fitness standard.
        """
        print(f"\n[BOSS EXAM ACTIVATED]: Level {level} Challenge for {self.salutation} {self.user_name}!")
        
        combined_score = round((viva_accuracy + fitness_accuracy) / 2.0, 2)
        passed = combined_score >= 80.0

        result_status = "PASSED - LEVEL UP GRANTED!" if passed else "FAILED - RETRY REQUIRED"
        
        print(f"[Exam Score]: Viva: {viva_accuracy}% | Fitness: {fitness_accuracy}%")
        print(f"[Final Evaluation]: Score = {combined_score}% | Result: {result_status}\n")

        return {
            "level": level,
            "combined_score": combined_score,
            "passed": passed
        }

if __name__ == "__main__":
    examiner = BossLevelExaminer()
    if examiner.is_boss_level(10):
        examiner.execute_boss_exam(level=10, viva_accuracy=92.0, fitness_accuracy=88.0)
      
