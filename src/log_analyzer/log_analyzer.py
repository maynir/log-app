from typing import Optional

from src.dns_solver.dns_solver import DnsSolver
from src.log_entry.log_entry import LogEntry
from src.log_reader.log_reader import LogReader
import queue
import concurrent.futures
import threading
from src.traffic.traffic import Traffic


class LogAnalyzer:
    def __init__(self, log_file: str, csv_file_path: str, thread_num: int = 4) -> None:
        self.log_reader: LogReader = LogReader(log_file)
        self._thread_num: int = thread_num
        self._log_queue: queue.Queue = queue.Queue()
        self._result_queue: queue.Queue = queue.Queue()
        self._counter = 0
        self._lock = threading.Lock()
        self._traffic = Traffic.read_csv_file(csv_file_path=csv_file_path)
        self._logs_counter = 0
        self._dns_solver = DnsSolver()


    def _is_valid_log(self, log_entry: LogEntry) -> bool:
        return log_entry.is_valid()


    def _proccess_log_with_domain(self, log_line: LogEntry):
        with self._lock:
            self._dns_solver.put(key=log_line.cloud_ip, value=log_line.domain)
            self._logs_counter += 1
            self._traffic.add_ip_to_cloud(cloud_domain=log_line.domain, ip=log_line.user_ip)

    def _proccess_log_without_domain(self, log_line: LogEntry):
        with self._lock:
            domain = self._dns_solver.get(key=log_line.cloud_ip)
            if domain is not None:
                self._logs_counter += 1
                self._traffic.add_ip_to_cloud(domain, log_line.user_ip)

    def _process_logs(self) -> None:
        while True:
            log_line: Optional[LogEntry] = self._log_queue.get()
            if log_line is None:
                break
            if not self._is_valid_log(log_line):
                continue
            if log_line.domain:
                self._proccess_log_with_domain(log_line)
            else:
                self._proccess_log_without_domain(log_line)

    def analyze(self) -> dict:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._thread_num) as executer:
            futures = [executer.submit(self._process_logs) for _ in range(self._thread_num)]

            for log_entry in self.log_reader.read_logs():
                if log_entry is None:
                    break
                self._log_queue.put(log_entry)

            for _ in range(self._thread_num):
                self._log_queue.put(None)

            [future.result() for future in futures] # wait for threads to finish
            print(f"analyzed {self._logs_counter} logs") # TODO: remove
            return self._traffic.get_clouds_ips()



