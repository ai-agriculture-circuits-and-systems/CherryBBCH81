import os
import json
import time
from PIL import Image
import glob
import argparse

def generate_unique_id():
    """Generate a unique 10-digit ID with last 3 digits as timestamp"""
    timestamp = int(time.time()) % 1000  # Last 3 digits of timestamp
    # Generate a random 7-digit number
    import random
    random_part = random.randint(1000000, 9999999)
    return random_part * 1000 + timestamp

def convert_yolo_to_coco_bbox(x_center, y_center, w, h, img_width, img_height):
    """Convert YOLO format (center_x, center_y, width, height) to COCO format (x, y, width, height)"""
    x = (x_center - w/2) * img_width
    y = (y_center - h/2) * img_height
    w = w * img_width
    h = h * img_height
    return [x, y, w, h]

def generate_annotation_file(image_path, label_path, output_path):
    """Generate individual annotation file for a single image"""
    
    # Get image info
    img = Image.open(image_path)
    width, height = img.size
    
    # Get file info
    file_name = os.path.basename(image_path)
    file_size = os.path.getsize(image_path)
    
    # Generate unique IDs
    image_id = generate_unique_id()
    category_id = generate_unique_id()
    
    # Initialize annotation structure
    annotation_data = {
        "info": {
            "description": "data",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [
            {
                "id": image_id,
                "width": width,
                "height": height,
                "file_name": file_name,
                "size": file_size,
                "format": "JPEG",
                "url": "",
                "hash": "",
                "status": "success"
            }
        ],
        "annotations": [],
        "categories": [
            {
                "id": category_id,
                "name": "AppleBBCH81",
                "supercategory": "apple"
            }
        ]
    }
    
    # Read and convert annotations from YOLO format
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id, x_center, y_center, w, h = map(float, parts)
                    
                    # Convert to COCO format
                    bbox = convert_yolo_to_coco_bbox(x_center, y_center, w, h, width, height)
                    area = bbox[2] * bbox[3]  # width * height
                    
                    # Generate unique annotation ID
                    annotation_id = generate_unique_id()
                    
                    annotation_data["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "segmentation": [],
                        "area": area,
                        "bbox": bbox
                    })
    
    # Save annotation file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(annotation_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated annotation for {file_name}: {len(annotation_data['annotations'])} annotations")

def process_all_images(images_dir, labels_dir, output_dir=None):
    """Process all images and generate individual annotation files"""
    
    if output_dir is None:
        output_dir = images_dir
    
    # Get all image files
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.jpg")))
    
    print(f"Found {len(image_files)} images to process...")
    
    for img_path in image_files:
        # Get corresponding label file
        img_filename = os.path.basename(img_path)
        label_filename = os.path.splitext(img_filename)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_filename)
        
        # Generate output path (same name as image but with .json extension)
        output_filename = os.path.splitext(img_filename)[0] + ".json"
        output_path = os.path.join(output_dir, output_filename)
        
        # Generate annotation file
        generate_annotation_file(img_path, label_path, output_path)

def main():
    parser = argparse.ArgumentParser(description='Generate individual annotation JSON files for images')
    parser.add_argument('--images', type=str, default="data/images", help='Directory containing the image files')
    parser.add_argument('--labels', type=str, default="data/labels", help='Directory containing the YOLO format label files')
    parser.add_argument('--output', type=str, default=None, help='Output directory (defaults to images directory)')
    
    args = parser.parse_args()
    
    # Check if directories exist
    if not os.path.exists(args.images):
        print(f"Error: Images directory '{args.images}' does not exist")
        return
    
    if not os.path.exists(args.labels):
        print(f"Error: Labels directory '{args.labels}' does not exist")
        return
    
    # Process all images
    process_all_images(args.images, args.labels, args.output)
    print("Annotation generation completed!")

if __name__ == "__main__":
    main() 