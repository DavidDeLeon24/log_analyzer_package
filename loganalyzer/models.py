from dataclasses import dataclass
from collections import Counter

@dataclass
class LogEntry:
    """Part A.1: Dataclass representing a single valid log entry."""
    timestamp: str
    level: str
    message: str
    date_str: str

    def to_string(self):
        return f"{self.timestamp} {self.level} {self.message}"


class LogAnalyzer:
    """Part A.2: Additional class for data analysis."""
    def __init__(self, entries):
        self.entries = entries

    def count_by_level(self):
        counts = Counter(entry.level for entry in self.entries)
        return {level: counts.get(level, 0) for level in ["DEBUG", "INFO", "WARNING", "ERROR"]}

    def get_top_errors(self, limit=5):
        error_msgs = [e.message for e in self.entries if e.level == "ERROR"]
        counts = Counter(error_msgs)
        sorted_errors = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return sorted_errors[:limit]

    def get_daily_counts(self):
        counts = Counter(entry.date_str for entry in self.entries)
        return sorted(counts.items())

    def filter_by_date(self, start_date, end_date):
        return [e for e in self.entries if start_date <= e.date_str <= end_date]


def filter_by_level_generator(entries, target_level):
    """Part B.3: Generator that accepts an iterable and yields matching levels."""
    for entry in entries:
        if entry.level == target_level:
            yield entry


class BatchIterator:
    """Part B.4: Custom iterator returning log entries in configurable batches."""
    def __init__(self, entries, batch_size):
        self.entries = list(entries) 
        self.batch_size = batch_size
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.entries):
            raise StopIteration
        
        end = self.current_index + self.batch_size
        batch = self.entries[self.current_index:end]
        self.current_index = end
        return batch