from loganalyzer.reader import read_log_file
from loganalyzer.models import LogAnalyzer
from loganalyzer.reports import ReportGenerator


def show_menu():
    print("\n===== LOG ANALYZER MENU =====")
    print("1. Show first 5 ERROR entries")
    print("2. Show suspicious login warnings")
    print("3. Show summary by level")
    print("4. Show all ERROR messages")
    print("5. Show all WARNING entries")
    print("0. Exit")


def main():
    # Load and parse the log file
    entries, invalid = read_log_file("application.log")
    analyzer = LogAnalyzer(entries, invalid)
    report = ReportGenerator(analyzer)

    print(f"Loaded {analyzer.total_valid()} valid entries "
          f"({invalid} invalid lines skipped).")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            report.print_first_errors(5)
        elif choice == "2":
            report.print_suspicious_logins()
        elif choice == "3":
            report.print_summary()
        elif choice == "4":
            print("\nERROR messages:")
            for msg in analyzer.error_messages():
                print(f"  - {msg}")
        elif choice == "5":
            print("\nWARNING entries:")
            for entry in analyzer.filter_by_level("WARNING"):
                print(f"  {entry.to_string()}")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option — try again.")


if __name__ == "__main__":
    main()