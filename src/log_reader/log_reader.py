from typing import Generator, Optional
from src.log_entry.log_entry import LogEntry


class LogReader:

    def __init__(self, file_path: str, chunk_size: int = 1024):
        self.file_path = file_path
        self.chunk_size = chunk_size

    def read_logs(self) -> Generator[Optional[LogEntry], None, None]:
        with open(self.file_path, "r") as file:
            for line in file:
                try:
                    yield LogEntry.from_line(line.strip())
                except ValueError as e:
                    # print(f"Skipped bad form log entry: {e}")
                    continue

