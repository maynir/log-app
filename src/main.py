from log_analyzer.log_analyzer import LogAnalyzer
from pathlib import Path

def run():
    print('run')
    log_file = str(Path("../logs/firewall.log"))
    csv_file_path = str(Path("../databases/ServiceDBv1.csv"))
    log_analyzer = LogAnalyzer(log_file=log_file, csv_file_path=csv_file_path)
    clouds_dict = log_analyzer.analyze()
    print(clouds_dict)

if __name__ == "__main__":
    run()
