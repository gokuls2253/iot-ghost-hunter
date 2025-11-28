import requests
import os
import re

class ThreatHunter:
    def __init__(self):
        self.api_key = os.getenv('VT_API_KEY')
        self.base_url = "https://www.virustotal.com/api/v3/ip_addresses/"

    def is_public_ip(self, ip):
        """
        Ignore Local IPs (192.168.x.x, 10.x.x.x, 127.0.0.1)
        """
        # Simple regex for private ranges
        private_re = re.compile(r'(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)')
        return not private_re.match(ip)

    def check_ip(self, ip_address):
        """
        Query VirusTotal API.
        Returns: (is_malicious: bool, score: int)
        """
        # === SIMULATION MODE: ON ===
        # Force a fake threat alert for testing purposes
        #return True, 99  # (is_malicious=True, score=99)
        
        # === ORIGINAL CODE BELOW (Commented out) ===
        if not self.api_key:
            print("Error: No VirusTotal API Key found.")
            return False, 0

        headers = {
            "x-apikey": self.api_key
        }

        try:
            print(f"[*] Querying VirusTotal for {ip_address}...")
            response = requests.get(self.base_url + ip_address, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                # Extract the "malicious" vote count
                stats = data['data']['attributes']['last_analysis_stats']
                malicious_count = stats['malicious']
                
                if malicious_count > 0:
                    return True, malicious_count
                return False, 0
            elif response.status_code == 429:
                print("[-] VirusTotal Quota Exceeded")
                return False, 0
            else:
                print(f"[-] VirusTotal Error: {response.status_code}")
                return False, 0

        except Exception as e:
            print(f"[-] API Request Failed: {e}")
            return False, 0