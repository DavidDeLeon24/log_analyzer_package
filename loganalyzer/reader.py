from .models import LogEntry


def read_log_file(filename):
    """
    Reads a log file and returns:
      - entries: list of LogEntry objects (valid lines only)
      - invalid_count: number of skipped malformed lines
    """
    entries = []
    invalid_count = 0

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 3)

            if len(parts) != 4:
                invalid_count += 1
                continue

            date, time, level, message = parts
            timestamp = f"{date} {time}"
            entries.append(LogEntry(timestamp, level, message))

    return entries, invalid_count