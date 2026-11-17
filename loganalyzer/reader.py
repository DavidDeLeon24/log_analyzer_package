import datetime
from .models import LogEntry

class LogReader:
    def __init__(self):
        self.invalid_count = 0

    def generate_entries(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(" ", 3)
                    
                    if len(parts) != 4:
                        self.invalid_count += 1
                        continue
                    
                    date, time, level, message = parts
                    
                    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
                    if level not in valid_levels or not message.strip():
                        self.invalid_count += 1
                        continue
                    
                    try:
                        datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        self.invalid_count += 1
                        continue

                    timestamp = f"{date} {time}"
                    yield LogEntry(timestamp, level, message, date)
                    
        except FileNotFoundError:
            print(f"\n[ERROR] File '{filename}' not found. Please ensure it is in the same folder.")