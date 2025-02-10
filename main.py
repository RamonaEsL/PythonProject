import csv
import sys
import json
from datetime import datetime

# It will read the input CSV file and return the data as a list of dictionaries
def read_input_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

# It will perform calculations on the input data
# Calculates (total revenue = number of items x price) write it to the output file
def perform_calculations(data):
    try:
        for row in data:
            row['Revenue'] = float(row['Units Sold']) * float(row['Price'])
        return data
    except KeyError as e:
        print(f"Error: Missing column {e}. Please ensure the input file has 'Units Sold' and 'Price' columns.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during calculation: {e}")
        sys.exit(1)

#  Writing the processed data to an output CSV file
def write_output_file(data, output_path):
    try:
        fieldnames = list(data[0].keys())
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {output_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

# For text report generation
def generate_report(data, report_path):
    try:
        total_revenue = sum(row['Revenue'] for row in data)
        report = {
            "Processing Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Records Processed": len(data),
            "Total Revenue": total_revenue,
        }
        with open(report_path, mode='w') as file:
            json.dump(report, file, indent=4)
        print(f"Report successfully written to {report_path}")
    except Exception as e:
        print(f"Error writing report: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python data_processing.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = "output.csv"
    report_file = "report.txt"

    # Processing Workflow
    data = read_input_file(input_file)
    processed_data = perform_calculations(data)
    write_output_file(processed_data, output_file)
    generate_report(processed_data, report_file)

if __name__ == "__main__":
    main()
