import json
import os

class SystemJudge:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def evaluate_viva(self, accuracy_percentage):
        """
        Evaluates 2-minute study viva voice test accuracy and awards XP.
        """
        if accuracy_percentage >= 100:
            xp = 500
            grade = "S-Class Supreme"
        elif accuracy_percentage >= 90:
            xp = 450
            grade = "A-Rank Excellent"
        elif accuracy_percentage >= 60:
            xp = 200
            grade = "B-Rank Acceptable"
        else:
            xp = 0
            grade = "F-Rank Failed (Retest Required)"

        print(f"[{self.salutation} {self.user_name}'s Evaluation]: Grade: {grade} | XP Granted: +{xp}")
        return {"grade": grade, "xp": xp}

    def evaluate_boss_level(self, level, viva_score, fitness_score):
        """
        Boss level evaluation every 10 levels (Level 10, 20, 30...).
        Combines fitness posture and cumulative study performance.
        """
        total_score = (viva_score + fitness_score) / 2.0
        passed = total_score >= 80.0
        
        status = "PASSED BOSS EXAM" if passed else "FAILED BOSS EXAM"
        print(f"\n[BOSS LEVEL {level} JUDGMENT]: {self.salutation} {self.user_name} - {status}")
        print(f"Cumulative Score: {total_score}%\n")
        
        return {"level": level, "passed": passed, "score": total_score}

if __name__ == "__main__":
    judge = SystemJudge()
    judge.evaluate_viva(95)
    judge.evaluate_boss_level(10, viva_score=90, fitness_score=85)
  
