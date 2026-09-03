import json
import os
from ui_theme_manager import UIThemeManager

class AudioFeedbackEngine:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        
        self.theme_mgr = UIThemeManager(config_path)
        self.active_theme = self.theme_mgr.get_theme()
        self.sound_enabled = self.config.get("audio_settings", {}).get("sound_effects", True)
        self.voice_enabled = self.config.get("audio_settings", {}).get("voice_feedback", True)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Audio Engine Error]: Config load failed -> {e}")
        return {}

    def play_sound_effect(self, event_type="SUCCESS"):
        """
        Triggers tactical sound effect cues for UI actions, correct answers, or alerts.
        """
        sound_library = {
            "SUCCESS": "chime_success.wav",
            "ERROR": "alert_error.wav",
            "BUTTON_CLICK": "ui_click.wav",
            "BOSS_LEVEL_START": "boss_warning.wav",
            "VIVA_CORRECT": "viva_pass.wav"
        }
        
        sound_file = sound_library.get(event_type.upper(), "default_beep.wav")
        if self.sound_enabled:
            print(f"[Audio Feedback]: Playing sound FX '{sound_file}' for event '{event_type}'.")
            return {"status": "playing", "file": sound_file, "enabled": True}
        else:
            print(f"[Audio Feedback]: Sound FX muted.")
            return {"status": "muted", "file": sound_file, "enabled": False}

    def speak_voice_prompt(self, message_text, language="bn"):
        """
        Executes text-to-speech audio feedback in Bengali, English, or Banglish for viva/fitness prompts.
        """
        formatted_message = f"{self.salutation} {self.user_name}, {message_text}"
        
        if self.voice_enabled:
            print(f"\n[Voice Engine Active] ({language.upper()}): '{formatted_message}'")
            return {
                "status": "speaking",
                "text": formatted_message,
                "lang": language,
                "user": f"{self.salutation} {self.user_name}"
            }
        else:
            print(f"[Voice Engine]: Speech synthesis disabled.")
            return {"status": "disabled", "text": formatted_message}

if __name__ == "__main__":
    audio_engine = AudioFeedbackEngine()
    audio_engine.play_sound_effect("BOSS_LEVEL_START")
    audio_engine.speak_voice_prompt("আপনার অডিটিং ভাইভা সেশন শুরু করার জন্য তৈরি হন।", language="bn")
  
