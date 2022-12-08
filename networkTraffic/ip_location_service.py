import requests
from networkTraffic import Location


class IPLocationService:
    cache: dict = {}

    def get_ip_location(self, ip: str):
        found = self.cache.get(ip)
        if found:
            return found
        else:
            location = self._get_for_ip(ip)
            self.cache[ip] = location
            return location

    @staticmethod
    def _get_for_ip(ip_addr: str):
        response = requests.get(f'https://ipapi.co/{ip_addr}/json/').json()
        return Location(
            city=response.get("city"),
            country=response.get("country_name")
        )
