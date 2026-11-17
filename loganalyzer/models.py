from dataclasses import dataclass


@dataclass
class LogEntry:
    """Represents a single valid line of the log file."""
    timestamp: str
    level: str
    message: str

    def is_error(self):
        return self.level == "ERROR"

    def is_warning(self):
        return self.level == "WARNING"

    def to_string(self):
        return f"{self.timestamp} {self.level} {self.message}"


class LogAnalyzer:
    """Analyzes a list of LogEntry objects."""

    def __init__(self, entries, invalid_count):
        self.entries = entries
        self.invalid_count = invalid_count

    def count_by_level(self, level):
        # Declarative: list comprehension
        return len([e for e in self.entries if e.level == level])

    def error_messages(self):
        # Declarative: list comprehension
        return [e.message for e in self.entries if e.is_error()]

    def filter_by_level(self, level):
        # Declarative: list comprehension
        return [e for e in self.entries if e.level == level]

    def total_valid(self):
        return len(self.entries)

    def suspicious_logins(self):
        return [
            e for e in self.entries
            if e.level == "WARNING" and "login" in e.message.lower()
        ]