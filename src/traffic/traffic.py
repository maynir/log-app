from __future__ import annotations
import pandas as pd
from src.cloud_traffic.cloud_traffic import CloudTraffic


class Traffic:
    def __init__(self, csv_file_path: str, clouds_dict: dict):
        self._csv_file_path: str = csv_file_path
        self._clouds_dict: dict = clouds_dict

    @classmethod
    def read_csv_file(cls, csv_file_path) -> Traffic:
        data = pd.read_csv(csv_file_path)
        clouds_dict = {}
        for index, row in data.iterrows():
            service = CloudTraffic(
                cloud_name=row['Service name'],
                cloud_domain=row['Service domain'],
                risk=row['Risk'],
                country_of_origin=row['Country of origin'],
                gdpr_compliant=row['GDPR Compliant']
            )
            clouds_dict[row['Service domain']] = service

        return cls(csv_file_path=csv_file_path, clouds_dict=clouds_dict)

    def add_ip_to_cloud(self, cloud_domain: str, ip: str) -> None:
        self._clouds_dict[cloud_domain].add_ip(ip)

    def get_clouds_ips(self) -> dict:
        return {cloudTraffic.get_cloud_name(): cloudTraffic.get_ips() for cloud, cloudTraffic in self._clouds_dict.items()}

    def get_ips_for_cloud(self, cloud_domain: str) -> list:
        return self._clouds_dict[cloud_domain].get_ips()