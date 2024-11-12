import os
import json
from PIL import Image

# Class mapping example: Modify this based on your dataset's class names
class_mapping = {
    "empty": 0,
    "occupied": 1
}

def process_json_files(dataset_root):
    """
    Processes all JSON files in the train, validation, and test splits and converts
    bounding boxes to YOLO format in text files, resizing images to 640x640.

    Args:
    - dataset_root (str): Path to the root directory of the dataset
    """
    # Loop through the train, validation, and test splits
    for split in ["train", "validation", "test"]:
        label_dir = os.path.join(dataset_root, split, "labels")
        image_dir = os.path.join(dataset_root, split, "images")

        # Process each JSON file in the labels folder
        for json_file_name in os.listdir(label_dir):
            if json_file_name.endswith(".json"):
                json_path = os.path.join(label_dir, json_file_name)

                # Image file name changes from .json to .jpg
                img_base_name = json_file_name.replace(".json", ".jpg")
                image_path = os.path.join(image_dir, img_base_name)
                txt_path = os.path.join(label_dir, json_file_name.replace(".json", ".txt"))

                try:
                    # Load and resize the image to 640x640
                    with Image.open(image_path) as img:
                        image_width, image_height = img.size
                        img_resized = img.resize((640, 640))
                        img_resized.save(image_path)  # Overwrite the original image

                except FileNotFoundError:
                    print(f"Image file not found for JSON: {json_path}")
                    continue  # Skip if the image is not found

                # Read the JSON file
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)

                # Create the YOLO-formatted .txt file
                with open(txt_path, 'w') as txt_file:
                    # Scaling factors for resizing
                    scale_x = 640 / image_width
                    scale_y = 640 / image_height

                    # Process bounding boxes (bbox2d)
                    if "bbox2d" in data:
                        for item in data["bbox2d"]:
                            class_name = item.get("name")
                            if class_name in class_mapping:
                                class_id = class_mapping[class_name]
                                x_min, y_min, x_max, y_max = item["bbox"]
                                # Adjust coordinates for resized image
                                x_min, x_max = x_min * scale_x, x_max * scale_x
                                y_min, y_max = y_min * scale_y, y_max * scale_y
                                x_center = (x_min + x_max) / 2.0 / 640
                                y_center = (y_min + y_max) / 2.0 / 640
                                width = (x_max - x_min) / 640
                                height = (y_max - y_min) / 640
                                txt_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

                    # Process segmentation (convert to bounding box)
                    if "segmentation" in data:
                        for item in data["segmentation"]:
                            class_name = item.get("name")
                            if class_name in class_mapping:
                                class_id = class_mapping[class_name]
                                polygon = item["polygon"]
                                x_coords = [point[0] * scale_x for point in polygon]
                                y_coords = [point[1] * scale_y for point in polygon]
                                x_min, x_max = min(x_coords), max(x_coords)
                                y_min, y_max = min(y_coords), max(y_coords)
                                x_center = (x_min + x_max) / 2.0 / 640
                                y_center = (y_min + y_max) / 2.0 / 640
                                width = (x_max - x_min) / 640
                                height = (y_max - y_min) / 640
                                txt_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


# Example of how to call the function
dataset_root = './merge_dataset_copy'  # Update with your dataset path
process_json_files(dataset_root)
