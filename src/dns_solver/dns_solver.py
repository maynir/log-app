from collections import OrderedDict
from typing import Optional


class DnsSolver:
    def __init__(self, _capacity: int = 1024):
        self._cache = OrderedDict()
        self._capacity = _capacity

    def get(self, key: str) -> Optional[str]:
        if key not in self._cache:
            return None
        else:
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(self, key: str, value: str) -> None:
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > self._capacity:
            self._cache.popitem(last = False)


if __name__ == "__main__":
    ds = DnsSolver()
    ds.put('ip1','domain1')
    print(ds.get('ip1'))
