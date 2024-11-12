import json
from PIL import Image, ImageDraw    # pillow library

def draw_bbox(img_path, json_path, bbox_img_path):
    """
    Func(define):
    - Processes JSON & corresponding image files, draw bbox on the image, then save it as 'bbox_img.jpg'

    Args:
    - img(str): Path to image.jpg that you want to check
    - json(str): Path to corresponding JSON file of the input image
    - bbox_img(str): path to output image has a bounding box from JSON file.
    """
    # Open the image
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)

    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Assuming JSON format contains a list of bounding boxes
    # with coordinates specified as x_min, y_min, x_max, y_max
    for box in data['bounding_boxes']:
        x_min, y_min, x_max, y_max = box['x_min'], box['y_min'], box['x_max'], box['y_max']

        # Draw the bounding box on the image
        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)

    # Save the image with drawn bounding boxes
    image.save(bbox_img_path)
    print(f"Image saved to {bbox_img_path}")

# Example usage
img_path = "path/to/your/image.jpg"
json_path= "path/to/your/data.json"
bbox_img_path = "path/to/your/output_image.jpg"
draw_bbox(img_path, json_path, bbox_img_path)