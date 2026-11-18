from loganalyzer.reader import LogReader
from loganalyzer.models import LogAnalyzer, filter_by_level_generator, BatchIterator
from loganalyzer.reports import ReportGenerator

def main():
    log_file = "application.log"
    reader = LogReader()
    
    entries = list(reader.generate_entries(log_file))
    
    if not entries:
        return
        
    analyzer = LogAnalyzer(entries)
    reporter = ReportGenerator(analyzer, reader.invalid_count)

    while True:
        print("\n===== SECURITY LOG ANALYZER =====")
        print("1. Display valid entries and malformed count")
        print("2. Count entries by severity level")
        print("3. Filter by severity level")
        print("4. Filter by date range")
        print("5. Display Top 5 ERROR messages")
        print("6. Display daily counts")
        print("7. Export text report")
        print("8. Run batch processing demo (Size 128)")
        print("0. Exit")
        
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"\nValid entries: {len(entries)}")
            print(f"Malformed lines: {reader.invalid_count}")
            
        elif choice == "2":
            print("\n--- Severity Counts ---")
            for level, count in analyzer.count_by_level().items():
                print(f"{level}: {count}")
                
        elif choice == "3":
            level = input("Enter severity level (DEBUG, INFO, WARNING, ERROR): ").strip().upper()
            if level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
                print("[ERROR] Invalid level.")
                continue
            
            limit_input = input("Enter max number to display (or press Enter for all): ").strip()
            
            try:
                limit = int(limit_input) if limit_input else None
                if limit is not None and limit < 0:
                    raise ValueError
            except ValueError:
                print("[ERROR] Invalid limit. Showing all entries.")
                limit = None

            fresh_stream = reader.generate_entries(log_file)
            level_gen = filter_by_level_generator(fresh_stream, level)
            
            displayed = 0
            print()
            for entry in level_gen:
                print(entry.to_string())
                displayed += 1
                if limit and displayed >= limit:
                    break
            print(f"\nTotal displayed: {displayed}")

        elif choice == "4":
            start = input("Enter start date (YYYY-MM-DD): ").strip()
            end = input("Enter end date (YYYY-MM-DD): ").strip()
            
            import datetime
            try:
                datetime.datetime.strptime(start, "%Y-%m-%d")
                datetime.datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                print("[ERROR] Invalid date format. Please use YYYY-MM-DD.")
                continue
                
            filtered = analyzer.filter_by_date(start, end)
            print()
            for entry in filtered:
                print(entry.to_string())
            print(f"\nTotal entries between {start} and {end}: {len(filtered)}")

        elif choice == "5":
            print("\n--- Top 5 ERROR Messages ---")
            for msg, count in analyzer.get_top_errors(5):
                print(f"{count}: {msg}")
                
        elif choice == "6":
            print("\n--- Valid Entries By Date ---")
            for date, count in analyzer.get_daily_counts():
                print(f"{date}: {count}")

        elif choice == "7":
            reporter.export_text_report()

        elif choice == "8":
            print("\n--- Batch Processing Demo (Size: 128) ---")
            fresh_stream = reader.generate_entries(log_file)
            batch_iter = BatchIterator(fresh_stream, batch_size=128)
            
            batch_count = 0
            last_batch_size = 0
            
            for batch in batch_iter:
                batch_count += 1
                last_batch_size = len(batch)
            
            print(f"Total batches created: {batch_count}")
            print(f"Size of final batch: {last_batch_size}")

        elif choice == "0":
            print("Exiting the program")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()