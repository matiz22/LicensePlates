import argparse
import time
from pathlib import Path
from plate.license_plate_detector import detect_and_save_license_plates
from processing.detected_plates import process_detected_plates
from source.dataset import get_ue_kat_dataset
from source.annotations_xml import load_annotations_dict
from test.calculate_final_grade import calculate_final_grade


def run_license_plate_pipeline(input_dir=None, output_dir=None, annotations_file=None, conf_threshold=0.25, lang='en'):
    # Setup paths and defaults
    if input_dir is None:
        dataset = get_ue_kat_dataset()
        input_dir = dataset["photos"]
        if annotations_file is None:
            annotations_file = dataset["annotations"]

    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir else input_path.parent / "detected_plates"

    print(f"Pipeline started with input: {input_path}")

    # Measure total pipeline time
    overall_start_time = time.time()
    
    # Count total input files first for accurate accuracy calculation
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    num_images = len([f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions])
    
    # Step 1: Detect and save license plates
    detection_count, detection_time, _ = detect_and_save_license_plates(input_path, output_path, conf_threshold)
    
    # Step 2: Load annotations and process plates with OCR
    annotations_dict = load_annotations_dict(annotations_file) if annotations_file else {}
    ocr_results = process_detected_plates(output_path, annotations_dict, lang)
    
    # Calculate and print final metrics
    overall_time = time.time() - overall_start_time
    avg_time_per_image = overall_time / num_images if num_images > 0 else 0
    estimated_time_100 = avg_time_per_image * 100
    
    # Updated: Calculate accuracy based on number of input files instead of detected plates
    accuracy = (ocr_results['correct'] / num_images) * 100 if num_images > 0 else 0
    
    final_grade = calculate_final_grade(accuracy, estimated_time_100)
    
    print("\n" + "="*50)
    print(f"OVERALL PIPELINE SUMMARY")
    print(f"Total input images: {num_images}")
    print(f"Detected plates: {detection_count}")
    print(f"Correctly read plates: {ocr_results['correct']}")
    print(f"Total execution time: {overall_time:.2f}s")
    print(f"Average time per image: {avg_time_per_image:.4f}s")
    print(f"Estimated time for 100 images: {estimated_time_100:.2f}s")
    print(f"Accuracy: {accuracy:.2f}% (correctly read / total input files)")
    print(f"FINAL GRADE: {final_grade}")
    print("="*50)
    
    return ocr_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="License Plate Detection and OCR Pipeline")
    parser.add_argument("--input", "-i", help="Directory containing input images (default: uses Poland dataset)")
    parser.add_argument("--output", "-o", help="Directory to save detected license plates")
    parser.add_argument("--annotations", "-a", help="JSON file with license plate text annotations")
    parser.add_argument("--conf", "-c", type=float, default=0.25, help="Confidence threshold for detection")
    parser.add_argument("--lang", "-l", default="en", help="Language for OCR (default: en)")
    
    args = parser.parse_args()
    
    run_license_plate_pipeline(
        args.input, 
        args.output, 
        args.annotations, 
        args.conf,
        args.lang
    )
