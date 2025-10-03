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
        
        # Get target information from user
        target_ip, target_port, target_uri = get_target_info(config_manager)
        
        # Set the target in configuration
        config_manager.set_target(target_ip, target_port, target_uri)
        
        # Initialize attack controller
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
║            CYBERSTRIKE PRO v4.0  ULTRA-AGGRESSIVE MODE             ║
║               MAXIMUM TRAFFIC & SERVER IMPACT                      ║
║                                                                    ║
║      Enhanced Features:                                            ║
║    • HYPER HTTP Flood (Ultra-high RPS)                             ║
║    • Mega Slowloris (Connection exhaustion++)                      ║
║    • Multi-vector simultaneous attacks                             ║
║    • Reduced delays & increased parallelism                        ║
║    • Advanced resource exhaustion                                  ║
║                                                                    ║
║      WARNING: EXTREMELY AGGRESSIVE - FOR LAB USE ONLY              ║
║      Made by: Nin Kanong(k4n0ng)                                   ║
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
    if consent.lower() != 'yes':
        print(" Tool execution canceled.")
        return False
    return True

def get_target_info(config_manager):
    """Get target information from user input"""
    print("\n TARGET CONFIGURATION")
    print("=" * 50)
    
    # Get target IP
    while True:
        target_ip = input("Enter target IP address: ").strip()
        if target_ip:
            break
        print(" IP address cannot be empty. Please enter a valid IP.")
    
    # Get target port
    target_port = input(f"Enter target port [80]: ").strip()
    if not target_port:
        target_port = 80
    else:
        try:
            target_port = int(target_port)
        except ValueError:
            print("  Invalid port. Using default port 80.")
            target_port = 80
    
    # Get target URI
    target_uri = input(f"Enter target URI [/]: ").strip()
    if not target_uri:
        target_uri = "/"
    
    # Display configuration
    print(f"\n Target configured:")
    print(f"   IP: {target_ip}")
    print(f"   Port: {target_port}")
    print(f"   URI: {target_uri}")
    print(f"   URL: http://{target_ip}:{target_port}{target_uri}")
    
    return target_ip, target_port, target_uri

if __name__ == "__main__":
    main()
