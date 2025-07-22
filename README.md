# CherryBBCH81 Dataset

A dataset of cherry fruit images captured during the beginning of fruit coloration (BBCH stage 81) in the LatHort orchard in Dobele, Latvia.

## Dataset Description

The CherryBBCH81 dataset is designed for cherry fruit detection tasks. It contains high-resolution images of cherry trees captured at the beginning of fruit coloration, making it suitable for computer vision, object detection, and deep learning research in agricultural applications.

- **Number of images**: Original images (6016x4000) cropped into 640x640 images
- **Image format**: YOLO format and COCO-style JSON
- **Overlap**: 30% between cropped images
- **BBCH stage**: 81 (beginning of ripening: berries begin to develop variety-specific colour)

## Database Structure

The dataset is organized as follows:

```
data/
├── images/         # Cropped images (640x640) and their annotation JSON files
│   ├── IMG_XXXX.jpg
│   ├── IMG_XXXX.json
│   └── ...
├── labels/         # YOLO format label files for each image
│   ├── IMG_XXXX.txt
│   └── ...
└── annotations.json # (Optional) COCO-style annotation file for the whole dataset
```

- `images/` contains all cropped images and their corresponding annotation files in JSON format (one per image).
- `labels/` contains YOLO format label files (one per image).
- `annotations.json` (if present) is a single file with all annotations in COCO format.

## Annotation Structure

Each image has a corresponding annotation JSON file with the following structure:

```json
{
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
      "id": 6979861700,
      "width": 640,
      "height": 640,
      "file_name": "IMGP9504_9.jpg",
      "size": 55157,
      "format": "JPEG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [
    {
      "id": 2459412700,
      "image_id": 6979861700,
      "category_id": 1811180700,
      "segmentation": [],
      "area": 788.53,
      "bbox": [576.07, 0.0, 25.60, 30.80]
    },
    ...
  ],
  "categories": [
    {
      "id": 1811180700,
      "name": "AppleBBCH81",
      "supercategory": "apple"
    }
  ]
}
```

- **info**: Metadata about the dataset and license.
- **images**: List with a single entry describing the image (id, size, filename, etc).
- **annotations**: List of bounding box annotations for the image. Each annotation includes:
  - `id`: Unique annotation ID
  - `image_id`: ID of the image
  - `category_id`: ID of the category (see `categories`)
  - `segmentation`: Empty list (no segmentation provided)
  - `area`: Area of the bounding box
  - `bbox`: Bounding box in `[x, y, width, height]` format (COCO style, absolute pixel values)
- **categories**: List of categories present in the image (usually one: "AppleBBCH81").

## Dataset Structure (Summary)

- Original high-resolution images (6016x4000)
- Cropped and annotated images (640x640)
- YOLO format annotations (`labels/`)
- COCO-style JSON annotations (`images/`)
- Two views per tree:
  - Perpendicular tree-facing view
  - Oblique view

## Data Collection

- **Location**: LatHort orchard in Dobele, Latvia
- **Timing**: At the beginning of fruit coloration (BBCH stage 81)
- **Annotation tool**: makesense.ai
- **Validation**: Manual validation of cropped images

## Applications

This dataset can be used for:
- Cherry fruit detection
- Yield estimation
- Object detection
- Computer vision research
- Deep learning model training
- Agricultural AI applications

## Categories

- Computer Science
- Artificial Intelligence
- Computer Vision
- Object Detection
- Machine Learning
- Agriculture
- Deep Learning
- Yield Estimation
- Precision Agriculture

## Citation

```
Ilmārs Apeināns, Marks Sondors, Lienīte Litavniece, Sergejs Kodors, Imants Zarembo, Daina Feldmane. "Cherry Fruitlet Detection using YOLOv5 or YOLOv8?," In Proceedings of the 15th International Scientific and Practical Conference "Environment. Technology. Resources.", Rezekne, Latvia, June 27-28, 2024, vol. 2, pp. 29-33, doi: 10.17770/etr2024vol2.8013
```

## License

This dataset is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Source

The dataset is available at:
- [Kaggle Dataset](https://www.kaggle.com/datasets/projectlzp201910094/cfruitlets81-640)
- [Papers with Code](https://paperswithcode.com/dataset/cherrybbch81) 