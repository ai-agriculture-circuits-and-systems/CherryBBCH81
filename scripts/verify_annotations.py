import os
import json
import glob
from PIL import Image
import argparse

def convert_yolo_to_coco_bbox(x_center, y_center, w, h, img_width, img_height):
    """Convert YOLO format to COCO format for verification"""
    x = (x_center - w/2) * img_width
    y = (y_center - h/2) * img_height
    w = w * img_width
    h = h * img_height
    return [x, y, w, h]

def verify_annotation_file(image_path, label_path, json_path):
    """Verify if the generated JSON annotation file is correct"""
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"ERROR: Image file not found: {image_path}")
        return False
    
    if not os.path.exists(json_path):
        print(f"ERROR: JSON annotation file not found: {json_path}")
        return False
    
    # Load JSON annotation
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            annotation_data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load JSON file {json_path}: {e}")
        return False
    
    # Verify JSON structure
    required_keys = ['info', 'images', 'annotations', 'categories']
    for key in required_keys:
        if key not in annotation_data:
            print(f"ERROR: Missing required key '{key}' in {json_path}")
            return False
    
    # Verify image info
    if len(annotation_data['images']) != 1:
        print(f"ERROR: Expected exactly 1 image, found {len(annotation_data['images'])} in {json_path}")
        return False
    
    image_info = annotation_data['images'][0]
    expected_filename = os.path.basename(image_path)
    
    if image_info['file_name'] != expected_filename:
        print(f"ERROR: Filename mismatch in {json_path}. Expected: {expected_filename}, Got: {image_info['file_name']}")
        return False
    
    # Verify image dimensions
    img = Image.open(image_path)
    actual_width, actual_height = img.size
    
    if image_info['width'] != actual_width or image_info['height'] != actual_height:
        print(f"ERROR: Image dimensions mismatch in {json_path}. Expected: {actual_width}x{actual_height}, Got: {image_info['width']}x{image_info['height']}")
        return False
    
    # Verify ID format (10 digits)
    image_id = image_info['id']
    if not isinstance(image_id, int) or image_id < 1000000000 or image_id > 9999999999:
        print(f"ERROR: Invalid image ID format in {json_path}. Expected 10-digit number, got: {image_id}")
        return False
    
    # Verify category
    if len(annotation_data['categories']) != 1:
        print(f"ERROR: Expected exactly 1 category, found {len(annotation_data['categories'])} in {json_path}")
        return False
    
    category = annotation_data['categories'][0]
    if category['name'] != 'AppleBBCH81' or category['supercategory'] != 'apple':
        print(f"ERROR: Invalid category in {json_path}. Expected: AppleBBCH81/apple, Got: {category['name']}/{category['supercategory']}")
        return False
    
    # Verify annotations if label file exists
    if os.path.exists(label_path):
        expected_annotations = []
        
        # Read YOLO format labels
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id, x_center, y_center, w, h = map(float, parts)
                    bbox = convert_yolo_to_coco_bbox(x_center, y_center, w, h, actual_width, actual_height)
                    expected_annotations.append(bbox)
        
        actual_annotations = annotation_data['annotations']
        
        if len(actual_annotations) != len(expected_annotations):
            print(f"ERROR: Annotation count mismatch in {json_path}. Expected: {len(expected_annotations)}, Got: {len(actual_annotations)}")
            return False
        
        # Verify each annotation
        for i, (expected_bbox, actual_annotation) in enumerate(zip(expected_annotations, actual_annotations)):
            # Check ID format
            annotation_id = actual_annotation['id']
            if not isinstance(annotation_id, int) or annotation_id < 1000000000 or annotation_id > 9999999999:
                print(f"ERROR: Invalid annotation ID format in {json_path}. Expected 10-digit number, got: {annotation_id}")
                return False
            
            # Check bbox
            actual_bbox = actual_annotation['bbox']
            if len(actual_bbox) != 4:
                print(f"ERROR: Invalid bbox format in {json_path}. Expected 4 values, got: {len(actual_bbox)}")
                return False
            
            # Compare bbox values with tolerance
            tolerance = 0.01
            for j in range(4):
                if abs(actual_bbox[j] - expected_bbox[j]) > tolerance:
                    print(f"ERROR: Bbox mismatch in {json_path} annotation {i}. Expected: {expected_bbox}, Got: {actual_bbox}")
                    return False
            
            # Check area calculation
            expected_area = expected_bbox[2] * expected_bbox[3]
            actual_area = actual_annotation['area']
            if abs(actual_area - expected_area) > tolerance:
                print(f"ERROR: Area mismatch in {json_path} annotation {i}. Expected: {expected_area}, Got: {actual_area}")
                return False
    
    else:
        # No label file, should have empty annotations
        if len(annotation_data['annotations']) != 0:
            print(f"ERROR: No label file found but annotations exist in {json_path}")
            return False
    
    return True

def verify_all_annotations(images_dir, labels_dir):
    """Verify all generated annotation files"""
    
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.jpg")))
    total_files = len(image_files)
    verified_files = 0
    failed_files = 0
    
    print(f"Starting verification of {total_files} annotation files...")
    
    for img_path in image_files:
        img_filename = os.path.basename(img_path)
        label_filename = os.path.splitext(img_filename)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_filename)
        json_filename = os.path.splitext(img_filename)[0] + ".json"
        json_path = os.path.join(images_dir, json_filename)
        
        if verify_annotation_file(img_path, label_path, json_path):
            verified_files += 1
        else:
            failed_files += 1
            print(f"FAILED: {img_filename}")
    
    print(f"\nVerification completed:")
    print(f"Total files: {total_files}")
    print(f"Verified: {verified_files}")
    print(f"Failed: {failed_files}")
    
    if failed_files == 0:
        print("SUCCESS: All annotation files are correct!")
        return True
    else:
        print("ERROR: Some annotation files have issues!")
        return False

def main():
    parser = argparse.ArgumentParser(description='Verify generated annotation JSON files')
    parser.add_argument('--images', type=str, default="data/images", help='Directory containing image files')
    parser.add_argument('--labels', type=str, default="data/labels", help='Directory containing YOLO format label files')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.images):
        print(f"Error: Images directory '{args.images}' does not exist")
        return
    
    if not os.path.exists(args.labels):
        print(f"Error: Labels directory '{args.labels}' does not exist")
        return
    
    verify_all_annotations(args.images, args.labels)

if __name__ == "__main__":
    main() 