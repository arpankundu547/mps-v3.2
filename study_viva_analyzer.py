import json
import os

class StudyVivaAnalyzer:
    def __init__(self, config_path="system_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
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

    def analyze_spoken_theory(self, subject, topic, spoken_text, target_keywords):
        """
        Analyzes 2-minute voice explanations in Bengali, Banglish, or English.
        Matches explanation accuracy against topic keywords (e.g., Auditing: Vouching/Verification).
        """
        print(f"\n[Viva Analyzer Active]: Listening to {self.salutation} {self.user_name} on Subject: {subject} ({topic})...")
        print(f"[Transcript Received]: \"{spoken_text}\"")

        # Check key concept coverage
        matched_keywords = [kw for kw in target_keywords if kw.lower() in spoken_text.lower()]
        coverage_ratio = len(matched_keywords) / len(target_keywords) if target_keywords else 1.0
        accuracy_percentage = round(coverage_ratio * 100, 2)

        print(f"[Concept Match]: {accuracy_percentage}% Accuracy against Standard Knowledge Base.")
        return {
            "subject": subject,
            "topic": topic,
            "accuracy": accuracy_percentage,
            "matched_concepts": matched_keywords
        }

if __name__ == "__main__":
    analyzer = StudyVivaAnalyzer()
    
    # Audit Viva Test Simulation
    sample_text = "অডিটিং এ Vouching এর মানে হলো documentary evidence দিয়ে transaction verify করা।"
    audit_keywords = ["Vouching", "documentary evidence", "verify"]
    
    analyzer.analyze_spoken_theory(
        subject="Auditing",
        topic="Vouching & Verification",
        spoken_text=sample_text,
        target_keywords=audit_keywords
    )
  
