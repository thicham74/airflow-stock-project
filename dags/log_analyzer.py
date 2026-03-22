import sys
from pathlib import Path

def analyze_file(file_path):
    """Parses a single log file for ERROR messages."""
    error_count = 0
    error_messages = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if "ERROR" in line:
                    error_count += 1
                    error_messages.append(line.strip())
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        
    return error_count, error_messages

def main():
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_directory>")
        return

    log_dir = sys.argv[1]
    total_errors = 0
    all_error_details = []

    # 2.1. Iterate through the directory recursively for .log files
    file_list = Path(log_dir).rglob('*.log')

    for file in file_list:
        # 2.2. Call the parse method
        count, cur_list = analyze_file(file)
        total_errors += count
        all_error_details.extend(cur_list)

    # 2.3. Print cumulative information
    print(f"Total number of errors: {total_errors}")
    if total_errors > 0:
        print("Here are all the errors:")
        for msg in all_error_details:
            print(msg)

if __name__ == "__main__":
    main()