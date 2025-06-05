#!/usr/bin/env python3
"""
CSV Updater

This script updates the forza_cars.csv file by:
1. Adding an ID column at the beginning
2. Wrapping string values in quotation marks
3. Incrementing the ID by 1 for each row

Usage:
    python update_csv.py [input_file] [output_file]

If no input or output file is specified, it will use the default paths.
"""

import csv
import sys
import os

def update_csv(input_file, output_file):
    """
    Update the CSV file by adding an ID column and wrapping strings in quotes.

    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file
    """
    # Read the input CSV file
    rows = []
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Get the header row
        rows = list(reader)    # Get all data rows

    # Add the ID column to the header
    new_header = ['id'] + header

    # Create the new rows with ID
    new_rows = []
    for i, row in enumerate(rows, 1):
        # Add ID to the beginning of each row
        new_row = [i] + row
        new_rows.append(new_row)

    # Write the updated data to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        # Use quoting=csv.QUOTE_NONNUMERIC to automatically quote non-numeric fields
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(new_header)
        writer.writerows(new_rows)

    print(f"Updated CSV file saved to {output_file}")
    print(f"Added ID column and wrapped strings in quotes for {len(new_rows)} rows")

if __name__ == "__main__":
    # Get input and output file paths from command line arguments or use defaults
    input_file = sys.argv[1] if len(sys.argv) > 1 else "../forza_cars.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "../forza_cars.csv"

    # Make sure the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    try:
        # Update the CSV file
        update_csv(input_file, output_file)
    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_file}'")
        print("Try running the script with sudo or specify a different output file")
        sys.exit(1)
