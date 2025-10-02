"""
Configuration management for CyberStrike Pro
"""

import json
import os
from . import settings

class ConfigManager:
    def __init__(self):
        self.config_file = settings.CONFIG_FILE
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}. Using defaults.")
        
        # Save default config
        self.save_config(settings.DEFAULT_CONFIG)
        return settings.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def update_config(self, new_settings):
        """Update configuration with new settings"""
        self.config.update(new_settings)
        self.save_config()
    
    def get_target(self):
        """Get target configuration"""
        return self.config["target"]
    
    def get_attack_config(self, attack_name):
        """Get configuration for specific attack"""
        return self.config["attacks"].get(attack_name, {})
    
    def is_attack_enabled(self, attack_name):
        """Check if an attack is enabled"""
        attack_config = self.get_attack_config(attack_name)
        return attack_config.get("enabled", False)