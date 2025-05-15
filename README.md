# License Plate Detection and OCR Pipeline

This project implements a pipeline for detecting license plates in images and performing OCR (Optical Character Recognition) to extract the plate text.

## Features

- License plate detection using YOLOv8
- OCR using PaddleOCR
- Support for different languages
- Performance metrics tracking
- Automatic result validation against ground truth

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LicensePlates.git
cd LicensePlates
```

2. Install the required dependencies:
```bash
pip install ultralytics paddleocr opencv-python kagglehub
```

## Usage

### Command Line Interface

Run the full pipeline with default settings:
```bash
python cli.py
```

Customize the pipeline with command-line arguments:
```bash
python cli.py --input /path/to/images --output /path/to/output --annotations /path/to/annotations.xml --conf 0.25 --lang pl
```

### Arguments

- `--input, -i`: Directory containing input images (default: uses Poland dataset)
- `--output, -o`: Directory to save detected license plates
- `--annotations, -a`: XML file with license plate text annotations
- `--conf, -c`: Confidence threshold for detection (default: 0.25)
- `--lang, -l`: Language for OCR (default: en)

## Project Structure

- `cli.py`: Command-line interface for running the pipeline
- `plate/license_plate_detector.py`: License plate detection using YOLOv8
- `processing/detected_plates.py`: OCR processing of detected plates
- `processing/dataset.py`: Dataset management
- `source/annotations_xml.py`: Functions for handling annotations
- `test/calculate_final_grade.py`: Evaluation of the pipeline performance

## Dataset

By default, the project uses the [Poland Vehicle License Plate Dataset](https://www.kaggle.com/datasets/piotrstefaskiue/poland-vehicle-license-plate-dataset) from Kaggle.

## Models Used

### Vehicle Detection
We use a pre-trained YOLOv8n model for initial vehicle detection.

### License Plate Detection
For license plate detection, we utilize a custom YOLOv8 model that was trained on a specialized license plate dataset. The model is available at [Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8](https://github.com/Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8).

The license plate detector model achieves high accuracy in detecting license plates across different lighting conditions and angles.

### OCR Processing
Once license plates are detected, we use PaddleOCR to recognize the text on the license plates. This powerful OCR engine works well with the specific characteristics of license plate text.

## Performance Metrics

The pipeline measures:
- Detection accuracy
- OCR accuracy
- Processing time per image
- Estimated time for 100 images
- Final grade based on accuracy and processing time

## References

- [Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8](https://github.com/Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Poland Vehicle License Plate Dataset](https://www.kaggle.com/datasets/piotrstefaskiue/poland-vehicle-license-plate-dataset)

