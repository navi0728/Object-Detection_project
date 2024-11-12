import os
import json
from collections import Counter

# JSON directory = put your .JSON path
json_dir = './merged_dataset/**/labels/*.json'

# Counter to save # of class frequencies
count_class_nums = Counter()

# Check just in case if the directory does not exists
print("!Checking just in case if the directory does not exist")
print("---------------------------------")
if not os.path.isdir(json_dir):
    print("Directory does not exist:", json_dir)
else:
    print("Directory exists.")
print("--------------------------------")


# Loop through each JSON file in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        # Open and load the JSON file
        with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as file: # encoding='utf-8 -> default value as far as Ive known
            data = json.load(file)
            # Count 'bbox2d' annotation only cuz we only need it and update class count through the loop
            for annotation in data.get('bbox2d', []):
                class_name = annotation.get('name')
                if class_name:
                    count_class_nums[class_name] += 1

            # Check num of parking block
            '''
            if class_name == "Parking Block":
                print(f"Parking block is in : ", filename)
            '''

# Pring out the result
print("Class Names and Their Frequencies")
print("---------------------------------")

# Sort class names and counts in alphabetical order -> for class mapping
sorted_count_class_nums = sorted(count_class_nums.items())

# Print sorted class names and their frequencies
for class_name, count in sorted_count_class_nums:
    print(f"{class_name}: {count}")
