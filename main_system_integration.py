import json
import os
import sys

# Import core modules
from database_manager import DatabaseManager
from security_guard import SecurityGuard
from ui_theme_manager import UIThemeManager
from ui_dashboard import UIDashboard
from flet_app_wrapper import FletAppWrapper
from audio_feedback_engine import AudioFeedbackEngine
from system_logger import SystemLogger
from boss_exam_judge import BossExamJudge
from system_pdf import SystemPDFGenerator
from tutorial_manager import TutorialManager

class MainSystemIntegration:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        # Initialize Subsystems
        self.logger = SystemLogger(config_path=config_path)
        self.db = DatabaseManager(config_path=config_path)
        self.security = SecurityGuard(config_path=config_path)
        self.theme_mgr = UIThemeManager(config_path=config_path)
        self.dashboard = UIDashboard(config_path=config_path)
        self.app_wrapper = FletAppWrapper(config_path=config_path)
        self.audio = AudioFeedbackEngine(config_path=config_path)
        self.boss_judge = BossExamJudge(config_path=config_path)
        self.pdf_gen = SystemPDFGenerator(config_path=config_path)
        self.tutorial = TutorialManager(config_path=config_path)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Core Integration Error]: Config load failed -> {e}")
        return {}

    def boot_system(self, input_pin="1234"):
        """
        Executes full system startup sequence and authenticates user.
        """
        print(f"\n==================================================")
        print(f"   LAUNCHING S-CLASS ASSISTANT - {self.salutation} {self.user_name}")
        print(f"==================================================")
        
        self.logger.log_event("MAIN_SYSTEM", "System Boot Sequence Initiated", level="INFO")
        
        # Security Authentication
        if not self.security.verify_pin(input_pin):
            self.logger.log_event("MAIN_SYSTEM", "Boot Failed: Invalid PIN", level="ERROR")
            self.audio.play_sound_effect("ERROR")
            print("[System Core]: Authentication Failed. Shutting down.")
            return False

        self.app_wrapper.authenticate_user(input_pin)
        self.audio.play_sound_effect("SUCCESS")
        self.audio.speak_voice_prompt("সিস্টেম সফলভাবে চালু হয়েছে। আপনাকে স্বাগতম।", language="bn")
        
        # Load User Stats from Database Vault
        stats = self.db.get_user_stats()
        if stats:
            level = stats.get("level", 1)
            xp = stats.get("xp", 0)
            rank = stats.get("rank", "Novice")
        else:
            level, xp, rank = 1, 0, "Novice"

        # Render Main GUI Dashboard Overview
        self.dashboard.render_dashboard(level=level, xp=xp, rank=rank)
        self.logger.log_event("MAIN_SYSTEM", "System Boot Completed Successfully", level="SUCCESS")
        return True

    def execute_boss_exam_workflow(self, subject="Auditing", viva_score=90.0, fitness_score=85.0):
        """
        Runs complete Boss Exam pipeline: Evaluation -> Database Log -> PDF Report -> Voice Feedback.
        """
        print(f"\n[Pipeline]: Triggering Boss Exam Evaluation...")
        
        # 1. AI Boss Level Evaluation
        result = self.boss_judge.evaluate_boss_level(viva_score, fitness_score)
        
        # 2. Database Recording
        self.db.log_viva(subject=subject, topic="Boss Assessment", accuracy=viva_score, xp_gained=500)
        self.db.log_fitness(exercise_type="Posture Check", accuracy=fitness_score, status="PASSED")
        
        # 3. PDF Report Generation
        self.pdf_gen.generate_study_summary(
            subject=subject,
            viva_score=viva_score,
            fitness_score=fitness_score,
            rank=result["rank_unlocked"]
        )
        
        # 4. Audio Cue
        self.audio.play_sound_effect("BOSS_LEVEL_START")
        self.audio.speak_voice_prompt("বস লেভেল মূল্যায়ন সম্পন্ন হয়েছে। ফলাফল রিপোর্ট তৈরি করা হয়েছে।", language="bn")
        
        return result

if __name__ == "__main__":
    system = MainSystemIntegration()
    if system.boot_system("1234"):
        system.execute_boss_exam_workflow(subject="Auditing & Vouching", viva_score=95.0, fitness_score=89.0)
      
