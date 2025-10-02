"""
Logging utilities for CyberStrike Pro
"""

import os
from datetime import datetime
from config.config_manager import ConfigManager

# Global logger instance
_logger_instance = None

def setup_logger():
    """Setup and return logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger()
    return _logger_instance

def log(msg, level="INFO"):
    """Global log function"""
    if _logger_instance:
        _logger_instance.log(msg, level)

class Logger:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.log_file = self.config_manager.config["logging"]["log_file"]
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log(self, msg, level="INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] {level.upper()}: {msg}"
        
        # Print to console
        print(formatted_msg)
        
        # Write to log file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted_msg + "\n")
        except Exception as e:
            print(f"❌ Logging error: {e}")