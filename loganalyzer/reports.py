class ReportGenerator:
    """Generates formatted reports from a LogAnalyzer."""

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def print_summary(self):
        print("===== SUMMARY =====")
        print(f"Total valid entries: {self.analyzer.total_valid()}")
        print(f"Invalid lines skipped: {self.analyzer.invalid_count}")
        print(f"INFO:    {self.analyzer.count_by_level('INFO')}")
        print(f"DEBUG:   {self.analyzer.count_by_level('DEBUG')}")
        print(f"WARNING: {self.analyzer.count_by_level('WARNING')}")
        print(f"ERROR:   {self.analyzer.count_by_level('ERROR')}")

    def print_first_errors(self, n=5):
        print(f"First {n} ERROR entries:")
        count = 0
        for entry in self.analyzer.entries:
            if entry.is_error():
                print(entry.to_string())
                count += 1
                if count == n:
                    break
        if count == 0:
            print("  (no ERROR entries found)")

    def print_suspicious_logins(self):
        suspicious = self.analyzer.suspicious_logins()
        print(f"\nSuspicious login warnings: {len(suspicious)}")
        for entry in suspicious[:5]:
            print(f"  {entry.to_string()}")