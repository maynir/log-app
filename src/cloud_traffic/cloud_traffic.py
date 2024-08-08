class CloudTraffic:
    def __init__(self,  cloud_name: str, cloud_domain: str, risk: str, country_of_origin: str, gdpr_compliant: str):
        self._cloud_name: str = cloud_name
        self._cloud_domain: str = cloud_domain
        self._risk: str = risk
        self._country_of_origin: str = country_of_origin
        self._gdpr_compliant: str = gdpr_compliant
        self._ips: set = set()

    def add_ip(self, ip):
        self._ips.add(ip)

    def get_ips(self) -> list:
        return list(self._ips)

    def get_cloud_name(self) -> str:
        return self._cloud_name
