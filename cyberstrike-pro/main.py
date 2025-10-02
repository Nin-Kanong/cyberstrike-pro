#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CyberStrike Pro v4.0 - Ultra Aggressive Mode
Professional penetration testing toolkit
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.attack_controller import AttackController
from config.config_manager import ConfigManager
from utils.logger import setup_logger

def main():
    """Main entry point for CyberStrike Pro"""
    
    # Print banner
    print_banner()
    
    # Legal disclaimer
    print_legal_disclaimer()
    
    # Get user consent
    if not get_user_consent():
        return
    
    try:
        # Initialize components
        config_manager = ConfigManager()
        logger = setup_logger()
        attack_controller = AttackController(config_manager, logger)
        
        # Start the attack controller
        attack_controller.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application interrupted by user.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

def print_banner():
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║            CYBERSTRIKE PRO v4.0  ULTRA-AGGRESSIVE MODE            ║
║               MAXIMUM TRAFFIC & SERVER IMPACT                     ║
║                                                                    ║
║      Enhanced Features:                                            ║
║    • HYPER HTTP Flood (Ultra-high RPS)                            ║
║    • Mega Slowloris (Connection exhaustion++)                     ║
║    • Multi-vector simultaneous attacks                            ║
║    • Reduced delays & increased parallelism                       ║
║    • Advanced resource exhaustion                                 ║
║                                                                    ║
║      WARNING: EXTREMELY AGGRESSIVE - FOR LAB USE ONLY             ║
║      Made by: Nin Kanong(k4n0ng)                                  ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_legal_disclaimer():
    disclaimer = """
⚠️  LEGAL DISCLAIMER:
This tool is for educational and authorized penetration testing only.
Unauthorized use against systems you don't own is ILLEGAL.
You are responsible for complying with all applicable laws.
    """
    print(disclaimer)

def get_user_consent():
    consent = input("\nDo you agree to use this tool responsibly? (yes/no): ")
    return consent.lower() == 'yes'

if __name__ == "__main__":
    main()