"""
Helper functions for CyberStrike Pro
"""

import random
import string

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

def get_random_headers(min_headers=1, max_headers=5):
    """Generate random headers"""
    headers = {}
    num_headers = random.randint(min_headers, max_headers)
    
    for _ in range(num_headers):
        header = random.choice(SPOOF_HEADERS)
        try:
            key, value = header.split(": ", 1)
            headers[key] = value
        except ValueError:
            continue
    
    return headers

def generate_random_string(length=10):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_rps(total_requests, duration):
    """Calculate requests per second"""
    return total_requests / max(duration, 1)

def format_number(number):
    """Format number with commas"""
    return f"{number:,}"

def get_impact_level(rps):
    """Determine impact level based on RPS"""
    if rps > 2000:
        return "CRITICAL"
    elif rps > 1000:
        return "SEVERE" 
    elif rps > 500:
        return "HIGH"
    elif rps > 200:
        return "MODERATE"
    else:
        return "LOW"