import json
import os

# Centralized configuration path and defaults
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULTS = {
    "label_bg": "#2c3e50",
    "fg_color": "#ecf0f1",
    "light_color": "#c61212",
    "font_setting": ["Helvetica", 10, "bold"]
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = DEFAULTS.copy()
                config.update(json.load(f))
                return config
        except Exception:
            pass
    
    save_config(DEFAULTS)
    return DEFAULTS.copy()

def save_config(config_dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config_dict, f, indent=4)