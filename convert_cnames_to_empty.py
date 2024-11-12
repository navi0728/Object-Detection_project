import os
import json
from tqdm import tqdm

def convert_to_empty_class_for_all(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all JSON files in the input directory
    json_files = [file for file in os.listdir(input_dir) if file.endswith(".json")]

    # Initialize tqdm progress bar
    for filename in tqdm(json_files, desc="Converting all class names into Empty", unit="file"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)

        # Load JSON data
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Convert "bbox2d" entries to "Empty"
        if "bbox2d" in data:
            for bbox in data["bbox2d"]:
                bbox["name"] = "empty"

        # Convert "segmentation" entries to "Empty"
        if "segmentation" in data:
            for segment in data["segmentation"]:
                segment["name"] = "empty"

        # Save the modified data to the output directory
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            #


# User's file directory -> Replace these
# (1) test/labels (2) train/labels (3) val/labels
input_directory = "./merge_dataset_copy/test/labels"
output_directory = "./merge_dataset_copy/test/labels"

convert_to_empty_class_for_all(input_directory, output_directory)
