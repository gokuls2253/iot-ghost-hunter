import requests
import json

class GeoMaster:
    def __init__(self):
        self.api_url = "http://ip-api.com/batch"

    def resolve_ips(self, ip_list):
        """
        Accepts a list of IPs and returns their Geo-Coordinates.
        Uses batch processing to be polite to the API.
        """
        if not ip_list:
            return []

        # Prepare payload (limit 100 per batch per API rules)
        # We perform a POST request for efficiency
        payload = [{"query": ip} for ip in ip_list[:100]] 
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=5)
            if response.status_code == 200:
                results = response.json()
                locations = []
                for res in results:
                    if res.get('status') == 'success':
                        locations.append({
                            'ip': res['query'],
                            'lat': res['lat'],
                            'lon': res['lon'],
                            'city': res['city'],
                            'country': res['countryCode']
                        })
                return locations
        except Exception as e:
            print(f"GeoIP Error: {e}")
        
        return []