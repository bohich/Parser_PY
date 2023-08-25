"""
Program for parsing header file and save register to csv file
"""
import re
import csv
import time

# Define the regular expression patterns
REGISTER_PATTERN1 = r"#define\s+(\w+)\s+(?:\(\((\w+)_Type\*\)\s+(&\w+->\w+\[\d+\])\)|([^\s]+))\s+/\*\s+(0x[0-9A-Fa-f]+)\s+\*/"
REGISTER_PATTERN2 = r'#define\s+(\w+_BASE)\s+(0x[0-9A-Fa-fLlUu]+)'
REGISTER_PATTERN3 = r'^\s*#define\s+(\w+)\s+\(\((\w+)\*\)\s*(\w+)\)\s+/\*\s*(0x[0-9A-Fa-f]+)\s+\*/$'
REGISTER_PATTERN4 = r'#define\s+(\w+)\s+\(\(([\w\s\->\*\(\).]*)\)\s+&([\w\->\.]+)\)\s+/\*\s+(0x[0-9a-fA-F]+)\s+\*/'
# List for all registers and values
data_list = []
#Path & name to CSV file
CSV_FILE = "Register.csv"
# Flag to indicate if we've encountered the "/* IP List */" line
AFTER_IP_LIST = False
# Counter for how much lines matched
ROW_COUNTER = 0
# Enter path to file
print("Enter path to header file: ")
path_to_header_file = input()
# Timer start
start_time = time.time()  # Remember the initial time
# Read the file
with open(path_to_header_file, "r", encoding="utf8") as file:
    input_text = file.read()
# Iterate through lines and process them after the "/* IP List */" line
for line in input_text.splitlines():
    if line.strip() == "/* IP List */":
        AFTER_IP_LIST = True
        continue  # Skip the line itself
    if not AFTER_IP_LIST:
        continue  # Skip lines before "/* IP List */"
    # Check if the line matches either pattern
    match1 = re.match(REGISTER_PATTERN1, line)
    match2 = re.match(REGISTER_PATTERN2, line)
    match3 = re.match(REGISTER_PATTERN3, line)
    match4 = re.match(REGISTER_PATTERN4, line)
    if match1:
        register_name = match1.group(1)
        if match1.group(2):
            value_hex = match1.group(5)
        else:
            value_hex = match1.group(4)
        value_int = int(value_hex, 16)
        # Check the 16th bit and update the 31st bit if necessary
        if value_int & (1 << 16):  # Check the 16th bit (bit at index 15)
            value_int |= (1 << 31) # Edit value in 31th bit to 1
            updated_value_hex = hex(value_int)
            data_list.append([register_name + "_S", updated_value_hex.upper().replace("X","x")])
        else:
            updated_value_hex = hex(value_int)
            data_list.append([register_name, updated_value_hex.upper().replace("X","x")])
        ROW_COUNTER += 1
    elif match2:
        register_name = match2.group(1)
        value_hex_with_ul = match2.group(2)
        # Remove "UL" suffix from value_hex_with_ul
        if value_hex_with_ul.lower().endswith("ul"):
            value_hex = value_hex_with_ul[:-2]
        else:
            value_hex = value_hex_with_ul
        # Convert hex to integer and back to hex without "UL" suffix
        value_int = int(value_hex, 16)
        # Check the 16th bit and update the 31st bit if necessary
        if value_int & (1 << 16):  # Check the 16th bit (bit at index 15)
            value_int |= (1 << 31) # Edit value in 31th bit to 1
            updated_value_hex = hex(value_int)
            data_list.append([register_name + "_S", updated_value_hex.upper().replace("X","x")])
        else:
            updated_value_hex = hex(value_int)
            data_list.append([register_name, updated_value_hex.upper().replace("X","x")])
        ROW_COUNTER += 1
    elif match3:
        register_name = match3.group(1)
        register_value = int(match3.group(4),16)
        if register_value & (1 << 16):  # Check the 16th bit (bit at index 15)
            register_value |= (1 << 31) # Edit value in 31th bit to 1
            updated_value_hex = hex(register_value)
            data_list.append([register_name + "_S", updated_value_hex.upper().replace("X","x")])
        else:
            updated_value_hex = hex(register_value)
            data_list.append([register_name, updated_value_hex.upper().replace("X","x")])
        ROW_COUNTER += 1
    elif match4:
        register_name = match4.group(1)
        register_value = int(match4.group(4),16)
        if register_value & (1 << 16):  # Check the 16th bit (bit at index 15)
            register_value |= (1 << 31) # Edit value in 31th bit to 1
            updated_value_hex = hex(register_value)
            data_list.append([register_name + "_S", updated_value_hex.upper().replace("X","x")])
        else:
            updated_value_hex = hex(register_value)
            data_list.append([register_name, updated_value_hex.upper().replace("X","x")])
        ROW_COUNTER += 1
#Writing to CSV file
with open(CSV_FILE, mode="w", newline="" , encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Register", "Value"])
    writer.writerows(data_list)

end_time = time.time()    # Remember the final time
elapsed_time = end_time - start_time  # Difference between start time and end time

print(f"Time spent: {elapsed_time:.5f} seconds \nall lines: {ROW_COUNTER}")
