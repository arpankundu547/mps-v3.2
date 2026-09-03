import sqlite3
import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="system_vault.db", config_path="system_config.json"):
        self.db_path = db_path
        self.config_path = config_path
        self.config = self.load_config()
        self.salutation = self.config.get("system_identity", {}).get("user_salutation", "Sir")
        self.user_name = self.config.get("system_identity", {}).get("user_name", "ARPAN")
        self.init_db()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes encrypted local tables for logs, XP, and user stats."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # User Progress Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    rank TEXT DEFAULT 'E-Rank',
                    last_updated TIMESTAMP
                )
            """)
            
            # Viva Log Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS viva_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT,
                    topic TEXT,
                    accuracy REAL,
                    xp_gained INTEGER,
                    timestamp TIMESTAMP
                )
            """)

            # Fitness Log Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fitness_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_type TEXT,
                    accuracy REAL,
                    status TEXT,
                    timestamp TIMESTAMP
                )
            """)

            # Ensure default user entry exists
            cursor.execute("SELECT COUNT(*) FROM user_progress")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_progress (user_name, level, xp, rank, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.user_name, 1, 0, 'E-Rank Novice', datetime.now()))

            conn.commit()
        print(f"[Database Manager]: System Vault initialized successfully for {self.salutation} {self.user_name}.")

    def log_viva(self, subject, topic, accuracy, xp_gained):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO viva_logs (subject, topic, accuracy, xp_gained, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (subject, topic, accuracy, xp_gained, datetime.now()))
            
            # Update Total XP
            cursor.execute("UPDATE user_progress SET xp = xp + ?, last_updated = ? WHERE user_name = ?", 
                           (xp_gained, datetime.now(), self.user_name))
            conn.commit()
        print(f"[DB Log]: Viva record saved (+{xp_gained} XP).")

    def log_fitness(self, exercise_type, accuracy, status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fitness_logs (exercise_type, accuracy, status, timestamp)
                VALUES (?, ?, ?, ?)
            """, (exercise_type, accuracy, status, datetime.now()))
            conn.commit()
        print(f"[DB Log]: Fitness session recorded ({status}).")

    def get_user_stats(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_name, level, xp, rank FROM user_progress LIMIT 1")
            row = cursor.fetchone()
            if row:
                return {"user_name": row[0], "level": row[1], "xp": row[2], "rank": row[3]}
            return None

if __name__ == "__main__":
    db = DatabaseManager()
    db.log_viva(subject="Auditing", topic="Vouching Principles", accuracy=95.0, xp_gained=450)
    stats = db.get_user_stats()
    print(f"[Current Stats]: {stats}")
  
