from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

PERMITTED_LOG_TYPES_PREFIXES = ["INBOUND", "OUTG"]

@dataclass
class LogEntry:
    timestamp: datetime
    log_type: str
    user_ip: str
    cloud_ip: str
    user: str = None
    domain: str = None

    def is_valid(self) -> bool:
        return any([self.log_type.startswith(prefix) for prefix in PERMITTED_LOG_TYPES_PREFIXES])

    @classmethod
    def from_line(cls, line: str) -> LogEntry:
        try:
            parts = line.split(maxsplit=3)

            timestamp_str = " ".join(parts[:3])
            timestamp = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")

            remaining_parts = parts[-1].split(": ")

            log_type = remaining_parts[1]

            data = remaining_parts[-1].split()
            details = {}
            user, domain, user_ip, cloud_ip = [None for _ in range(4)]
            for detail in data:
                if '=' in detail:
                    key, value = detail.split('=', 1)
                    details[key] = value
                else:
                    details[detail] = None

            src = details.get("SRC")
            dst = details.get("DST")
            user = details.get("USER")
            domain = details.get("DOMAIN")

            if log_type.startswith("INBOUND"):
                user_ip, cloud_ip = dst, src
            elif log_type.startswith("OUTG"):
                user_ip, cloud_ip = src, dst

            return cls(timestamp, log_type, user_ip, cloud_ip, user, domain)
        except ValueError as e:
            raise ValueError(f"Invalid log line format: {line}\n{e}")

if __name__ == "__main__":
    print(LogEntry.from_line("Feb 17 06:25:53 bridge kernel: INBOUND TCP: IN=br0 PHYSIN=eth0 OUT=br0 PHYSOUT=eth1 SRC=65.80.51.138 DST=11.11.11.87 LEN=48 TOS=0x00 PREC=0x00 TTL=117 ID=46193 DF PROTO=TCP SPT=3421 DPT=445 WINDOW=16384 RES=0x00 SYN URGP=0"))