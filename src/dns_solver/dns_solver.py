import threading
import socket
from lru import LRU

class DnsSolver:
    def __init__(self, capacity: int = 1024):
        self._cache = LRU(capacity)
        self._lock = threading.Lock()

    def get(self, ip):
        if ip in self._cache:
            return self._cache[ip]

        domain = self._resolve_domain(ip=ip)

        with self._lock:
            self._cache[ip] = domain
        return domain

    def put(self, ip, domain):
        with self._lock:
            self._cache[ip] = domain

    def _resolve_domain(self,ip):
        try:
            domain, _, _ = socket.gethostbyaddr(ip)
        except socket.herror:
            domain = None
        return domain

if __name__ == "__main__":
    ds = DnsSolver()
    ds.put('ip1', 'domain1')
    print(ds.get('ip1'))
