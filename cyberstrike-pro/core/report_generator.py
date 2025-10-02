"""
Report generation for CyberStrike Pro
"""

from datetime import datetime
from utils.logger import log

class ReportGenerator:
    def generate(self, stats, target):
        """Generate final attack report"""
        duration = stats.attack_duration
        total_requests = stats.http_requests + stats.post_requests + stats.udp_packets
        rps = total_requests / max(duration, 1)

        # Impact assessment
        if rps > 2000:
            impact = "CRITICAL"
        elif rps > 1000:
            impact = "SEVERE" 
        elif rps > 500:
            impact = "HIGH"
        elif rps > 200:
            impact = "MODERATE"
        else:
            impact = "LOW"

        print("\n" + "="*80)
        print("💀 CYBERSTRIKE PRO v4.0 - ULTRA AGGRESSIVE ATTACK REPORT")
        print("="*80)
        print(f"🎯 Target: http://{target['ip']}:{target['port']}{target['uri']}")
        print(f"⏱️  Duration: {int(duration)} seconds")
        print(f"⚡ HTTP Requests: {stats.http_requests:,}")
        print(f"📨 POST Requests: {stats.post_requests:,}")
        print(f"📡 UDP Packets: {stats.udp_packets:,}")
        print(f"🚧 Peak Slowloris: {stats.slowloris_connections}")
        print(f"📊 Average RPS: {int(rps):,}")
        print(f"💀 IMPACT LEVEL: {impact}")
        print(f"💥 EXPECTED RESULT: Server should be UNRESPONSIVE or CRASHED")
        print("="*80)
        
        log(f"ULTRA AGGRESSIVE attack completed. Impact: {impact}", "REPORT")