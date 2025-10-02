"""
Statistics management for CyberStrike Pro
"""

import time
from dataclasses import dataclass
from threading import Lock

@dataclass
class AttackStats:
    http_requests: int = 0
    slowloris_connections: int = 0
    udp_packets: int = 0
    post_requests: int = 0
    start_time: float = 0
    attack_duration: float = 0

class StatsManager:
    def __init__(self):
        self.stats = AttackStats()
        self.lock = Lock()
    
    def start_timer(self):
        """Start the attack timer"""
        self.stats.start_time = time.time()
    
    def update_duration(self):
        """Update attack duration"""
        if self.stats.start_time > 0:
            self.stats.attack_duration = time.time() - self.stats.start_time
    
    def increment_http_requests(self, count=1):
        """Increment HTTP request counter"""
        with self.lock:
            self.stats.http_requests += count
    
    def increment_post_requests(self, count=1):
        """Increment POST request counter"""
        with self.lock:
            self.stats.post_requests += count
    
    def increment_udp_packets(self, count=1):
        """Increment UDP packet counter"""
        with self.lock:
            self.stats.udp_packets += count
    
    def update_slowloris_connections(self, count):
        """Update Slowloris connection count"""
        with self.lock:
            self.stats.slowloris_connections = count
    
    def get_stats(self):
        """Get current statistics"""
        self.update_duration()
        return self.stats