class ReportGenerator:
    def __init__(self, analyzer, invalid_count):
        self.analyzer = analyzer
        self.invalid_count = invalid_count

    def export_text_report(self, filename="summary_report.txt"):
        """Part D.1: Export a plain-text summary report."""
        counts = self.analyzer.count_by_level()
        top_errors = self.analyzer.get_top_errors()
        daily_counts = self.analyzer.get_daily_counts()

        with open(filename, "w") as file:
            file.write("=== SECURITY LOG ANALYZER REPORT ===\n\n")
            file.write(f"Total Valid Entries: {len(self.analyzer.entries)}\n")
            file.write(f"Total Malformed Lines: {self.invalid_count}\n\n")
            
            file.write("--- Severity Counts ---\n")
            for level, count in counts.items():
                file.write(f"{level}: {count}\n")
            
            file.write("\n--- Top 5 ERROR Messages ---\n")
            for msg, count in top_errors:
                file.write(f"{count}: {msg}\n")
                
            file.write("\n--- Valid Entries By Date ---\n")
            for date, count in daily_counts:
                file.write(f"{date}: {count}\n")
                
        print(f"\n[SUCCESS] Report successfully saved to '{filename}'")