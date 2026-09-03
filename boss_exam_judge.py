import json
import os
from system_logger import SystemLogger

class BossExamJudge:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.logger = SystemLogger(config_path=config_path)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Judge Error]: Config load failed -> {e}")
        return {}

    def evaluate_boss_level(self, viva_score, fitness_score, level=10):
        """
        Evaluates dual-criteria (Study Viva + Fitness Pose) for Boss Level progression.
        Triggers rank promotion if threshold (85%+) is met.
        """
        print(f"\n[AI Boss Judge]: Evaluating Boss Level {level} for {self.salutation} {self.user_name}...")
        
        overall_score = round((viva_score * 0.6) + (fitness_score * 0.4), 2)
        passed = overall_score >= 85.0
        
        result = {
            "user": f"{self.salutation} {self.user_name}",
            "boss_level": level,
            "viva_score": viva_score,
            "fitness_score": fitness_score,
            "overall_score": overall_score,
            "status": "PASSED" if passed else "FAILED",
            "rank_unlocked": "S-Class Commander" if passed else "E-Rank Novice"
        }

        log_msg = f"Boss Exam Lvl {level} -> Score: {overall_score}% | Status: {result['status']}"
        self.logger.log_event("BOSS_EXAM_JUDGE", log_msg, level="SUCCESS" if passed else "WARNING")
        
        print(f"[Judge Decision]: {result['status']} ({overall_score}%) -> Rank: {result['rank_unlocked']}")
        return result

if __name__ == "__main__":
    judge = BossExamJudge()
    judge.evaluate_boss_level(viva_score=92.0, fitness_score=88.5, level=10)
  
