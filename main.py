import csv

# User input
group_no = input("Enter Group Number: ")
group_name = input("Enter Group Name: ")

# Input/output CSV file paths
input_file = 'repeaterbook.csv'        # Update with your file path
output_file = 'ic705_formatted.csv'    # Output file

# RPT1USE calculation helper
def calculate_rpt1use(offset):
    if offset > 0:
        return "DUP+"
    elif offset < 0:
        return "DUP-"
    else:
        return "DUP0"

# Dup string value based on offset
def get_dup_type(offset):
    if offset > 0:
        return "+"
    elif offset < 0:
        return "-"
    else:
        return "0"

# Load and transform CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = [
        'Group No', 'Group Name', 'Name', 'Sub Name', 'Repeater Call Sign',
        'Gateway Call Sign', 'Frequency', 'Dup', 'Offset', 'Mode', 'TONE',
        'Repeater Tone', 'RPT1USE', 'Position', 'Latitude', 'Longitude', 'UTC Offset'
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            out_freq = float(row.get('Output Freq', 0))
            in_freq = float(row.get('Input Freq', 0))
            offset = round(out_freq - in_freq, 5)
        except ValueError:
            offset = 0.0

        new_row = {
            'Group No': group_no,
            'Group Name': group_name,
            'Name': row.get('Location', ''),
            'Sub Name': row.get('County', ''),
            'Repeater Call Sign': row.get('Call', ''),
            'Gateway Call Sign': '',  # Empty unless you have data
            'Frequency': row.get('Output Freq', ''),
            'Dup': get_dup_type(offset),
            'Offset': abs(offset),
            'Mode': row.get('Mode', ''),
            'TONE': '',  # Can be filled if known
            'Repeater Tone': row.get('Downlink Tone', ''),
            'RPT1USE': calculate_rpt1use(offset),
            'Position': row.get('Location', ''),
            'Latitude': row.get('Lat', ''),
            'Longitude': row.get('Long', ''),
            'UTC Offset': ''  # Optional, if available
        }

        writer.writerow(new_row)

print(f"✅ Done. Output written to: {output_file}")
