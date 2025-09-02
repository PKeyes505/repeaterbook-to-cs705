import csv

# Input/output CSV file paths
input_file = 'repeaterbook.csv'        # Update with your file path
output_file = 'ic705_formatted.csv'    # Output file

# User input
group_no = input("Enter Group Number: ")
group_name = input("Enter Group Name: ")

# Sets to track used call signs
used_repeater_calls = set()
used_gateway_calls = set()

def is_supported_band(frequency):
    # List of supported frequency bands in MHz
    supported_bands = [
        (1.8, 30),    # HF Band
        (50, 54),     # 6m Band
        (144, 148),   # 2m Band
        (430, 450)    # 70cm Band
    ]
    
    # Check if frequency is within any of the supported bands
    for band in supported_bands:
        if band[0] <= frequency <= band[1]:
            return True
    return False

# Helper function to count decimal places
def count_decimal_places(value):
    try:
        parts = str(value).split('.')
        if len(parts) > 1:
            return len(parts[1])
        return 0
    except ValueError:
        return 0

# Logic for determining position based on decimal places
def determine_position(lat, long):
    lat_decimals = count_decimal_places(lat)
    long_decimals = count_decimal_places(long)

    if lat_decimals > 3 and long_decimals > 3:
        return 'Exact'
    else:
        return 'Approximate'

# Mode mapping function
def map_mode(mode_str):
    mode_str = mode_str.upper()
    if mode_str in ['FM', 'ANALOG']:
        return 'FM'

    elif any(digital in mode_str for digital in ['DMR', 'D-STAR', 'C4FM', 'NXDN', 'YSF']):
        return 'DV'
    else:
        return 'FM'  # Default fallback

# Function to calculate offset and dup type
def calculate_offset_and_dup(output_freq, input_freq):
    try:
        # Calculate the offset
        offset = round(output_freq - input_freq, 5)
        
        # Determine the dup based on offset
        if offset > 0:
            dup = "+"
        elif offset < 0:
            dup = "-"
        else:
            dup = "0"
        
        return offset, dup
    except ValueError:
        return 0.0, "0"  # Default if invalid frequency values

# RPT1USE calculation helper
def calculate_rpt1use(offset):
    if offset > 0:
        return "DUP+"
    elif offset < 0:
        return "DUP-"
    else:
        return "DUP0"

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

            # Skip rows with unsupported frequencies
            if not is_supported_band(out_freq):
                continue  # Skip this row
            
            # Calculate offset and dup
            offset, dup = calculate_offset_and_dup(out_freq, in_freq)

            # Set default UTC Value if none supplied
            utc_offset = row.get('UTC Offset', '--:--')

        except ValueError:
            out_freq = in_freq = offset = 0.0
            dup = "0"



        lat = row.get('Lat', 0)
        long = row.get('Long', 0)
 
 
    tone = row.get('Uplink Tone', '')  # Set TONE to 'Tone' if uplink_tone is provided
    if tone:
        tone = "TONE"       
       
        # Get Repeater and Gateway Call Signs
        repeater_call = row.get('Call', '')
        gateway_call = row.get('Gateway Call', '')

        # Ensure Repeater Call Sign is unique
        if repeater_call in used_repeater_calls:
            # If it's a duplicate, append a number to make it unique
            suffix = 1
            while f"{repeater_call}_{suffix}" in used_repeater_calls:
                suffix += 1
            repeater_call = f"{repeater_call}_{suffix}"
        used_repeater_calls.add(repeater_call)

        # Allow duplicate Gateway Call Signs only if it's not empty
        if gateway_call and gateway_call in used_gateway_calls:
            # If it's a duplicate, append a number to make it unique
            suffix = 1
            while f"{gateway_call}_{suffix}" in used_gateway_calls:
                suffix += 1
            gateway_call = f"{gateway_call}_{suffix}"
        # Add non-empty Gateway Call Signs to the set for future checks
        if gateway_call:
            used_gateway_calls.add(gateway_call)
        
        new_row = {
            'Group No': group_no,
            'Group Name': group_name,
            'Name': row.get('Location', ''),
            'Sub Name': row.get('County', ''),
            #'Repeater Call Sign': row.get('Call', ''),
            #'Gateway Call Sign': '',
            'Repeater Call Sign': repeater_call,  # Unique Repeater Call Sign
            'Gateway Call Sign': gateway_call,  # Unique Gateway Call Sign
            'Frequency': row.get('Output Freq', ''),
            'Dup': dup,
            'Offset': abs(offset),
            'Mode': map_mode(row.get('Mode', 'FM')),
            'TONE': tone,
            'Repeater Tone': row.get('Downlink Tone', ''),
            'RPT1USE': "NO",  # Translates to the SKIP 
            'Position': determine_position(lat, long),
            'Latitude': lat,
            'Longitude': long,
            'UTC Offset': utc_offset
        }

        writer.writerow(new_row)

print(f"✅ Done. Output written to: {output_file}")

