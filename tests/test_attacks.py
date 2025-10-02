"""
Unit tests for attack modules
"""

import unittest
from unittest.mock import Mock, patch
from attacks.http_flood import HTTPFlood
from attacks.slowloris import SlowlorisAttack

class TestAttackModules(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.target_config = {
            "ip": "127.0.0.1",
            "port": 8080,
            "uri": "/"
        }
        self.config_manager = Mock()
        self.stats_manager = Mock()
        
        # Mock configuration
        self.config_manager.get_attack_config.return_value = {
            "threads": 2,
            "delay": 0.1,
            "enabled": True
        }
    
    @patch('http.client.HTTPConnection')
    def test_http_flood_initialization(self, mock_http):
        """Test HTTP flood initialization"""
        attack = HTTPFlood(self.target_config, self.config_manager, self.stats_manager)
        self.assertEqual(attack.target_ip, "127.0.0.1")
        self.assertEqual(attack.target_port, 8080)
    
    @patch('socket.socket')
    def test_slowloris_initialization(self, mock_socket):
        """Test Slowloris initialization"""
        attack = SlowlorisAttack(self.target_config, self.config_manager, self.stats_manager)
        self.assertEqual(attack.target_ip, "127.0.0.1")
        self.assertEqual(attack.target_port, 8080)

if __name__ == '__main__':
    unittest.main()