import json
import os
import sys

CONFIG_FILE = "system_config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found!")
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def main():
    config = load_config()
    if not config:
        sys.exit(1)

    identity = config.get("system_identity", {})
    system_name = identity.get("name", "System")
    user_name = identity.get("user_name", "User")
    salutation = identity.get("user_salutation", "Sir")
    version = identity.get("version", "1.0.0")

    print("=" * 50)
    print(f" Initializing {system_name} v{version}")
    print(f" Welcome back, {salutation} {user_name}!")
    print("=" * 50)

    modules = config.get("active_modules", [])
    print(f"Active Modules Loaded: {len(modules)}")
    for mod in modules:
        print(f" - [ACTIVE] {mod}")
    
    print("\nSystem ready.")

if __name__ == "__main__":
    main()
  
