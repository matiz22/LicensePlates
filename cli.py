import argparse
import os
import time
from pathlib import Path

from plates.detection.detect_plate import detect_license_plate
from sources.annotations.annotations_xml import check_plate_number
from sources.dataset import get_ue_kat_dataset
from sources.photos.load_photos import load_photo_paths
from plates.text.read import read_plate_text
from tests.calculate_final_grade import calculate_final_grade


def process_dataset(photos_dir, annotations, verbose=False, sample_size=None):
    """Process a dataset of license plate images and return statistics."""
    try:
        photo_paths = load_photo_paths(photos_dir)

        if sample_size and sample_size < len(photo_paths):
            photo_paths = photo_paths[:sample_size]

        if verbose:
            print(f"Found {len(photo_paths)} photos to process")

        total_plates_detected = 0
        total_plates_read = 0
        correct_readings = 0
        total_with_annotations = 0

        start_time = time.time()

        for i, image_path in enumerate(photo_paths):
            if verbose:
                print(f"Processing image {i + 1}/{len(photo_paths)}: {image_path}")

            ground_truth = check_plate_number(annotations, os.path.basename(image_path))
            print(ground_truth)
            success, plate_img, plate_region, binary_plate = detect_license_plate(
                image_path
            )

            if success:
                total_plates_detected += 1
                ocr_success, plate_text = read_plate_text(
                    binary_plate if binary_plate is not None else plate_img
                )

                if ocr_success:
                    total_plates_read += 1
                    if verbose:
                        print(f"Read plate text: {plate_text}")

                    if ground_truth:
                        total_with_annotations += 1
                        if plate_text == ground_truth:
                            correct_readings += 1
                            if verbose:
                                print(f"✓ Correct match! Ground truth: {ground_truth}")
                        elif verbose:
                            print(f"✗ Mismatch. Ground truth: {ground_truth}")
            elif verbose and ground_truth:
                print(f"Failed to detect plate. Ground truth: {ground_truth}")

        processing_time = time.time() - start_time

        normalized_time = processing_time * (100 / len(photo_paths))

        accuracy = 0
        if total_with_annotations > 0:
            accuracy = (correct_readings / total_with_annotations) * 100

        return {
            "total_images": len(photo_paths),
            "plates_detected": total_plates_detected,
            "plates_read": total_plates_read,
            "correct_readings": correct_readings,
            "total_with_annotations": total_with_annotations,
            "accuracy": accuracy,
            "processing_time": processing_time,
            "normalized_time": normalized_time,
        }

    except Exception as e:
        print(f"Error processing dataset: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="License Plate Detection CLI")

    parser.add_argument("--dataset", help="Path to dataset directory (default: UE-KAT)")
    parser.add_argument("--photos", help="Path to photos directory (overrides dataset)")
    parser.add_argument(
        "--annotations", help="Path to annotations directory (overrides dataset)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument("--sample", "-s", type=int, help="Process only N images")

    args = parser.parse_args()

    photos_dir = None
    annotations_dir = None

    if args.photos and args.annotations:
        photos_dir = args.photos
        annotations_dir = args.annotations
    elif args.dataset:
        dataset_path = Path(args.dataset)
        photos_dir = dataset_path / "photos"
        annotations_dir = dataset_path / "annotations"
    else:
        dataset = get_ue_kat_dataset()
        photos_dir = dataset["photos"]
        annotations = dataset["annotations"]

    print(f"Processing license plates...")
    print(f"Photos: {photos_dir}")
    print(f"Annotations: {annotations_dir}")

    stats = process_dataset(photos_dir, annotations, args.verbose, args.sample)

    if stats:
        print("\n=== Results ===")
        print(f"Total images: {stats['total_images']}")
        print(
            f"Plates detected: {stats['plates_detected']} ({stats['plates_detected'] / stats['total_images'] * 100:.1f}%)"
        )

        if stats["plates_detected"] > 0:
            print(
                f"Plates read: {stats['plates_read']} ({stats['plates_read'] / stats['plates_detected'] * 100:.1f}%)"
            )

        if stats["total_with_annotations"] > 0:
            print(f"\n=== Accuracy ===")
            print(f"Images with annotations: {stats['total_with_annotations']}")
            print(f"Correct readings: {stats['correct_readings']}")
            print(f"Accuracy: {stats['accuracy']:.2f}%")

        print(f"\n=== Performance ===")
        print(f"Processing time: {stats['processing_time']:.2f} seconds")
        print(f"Normalized time (100 images): {stats['normalized_time']:.2f} seconds")

        print(stats["accuracy"], stats["normalized_time"])
        grade = calculate_final_grade(stats["accuracy"], stats["normalized_time"])
        print(f"\n=== Final Grade ===")
        print(f"Grade: {grade:.1f}")


if __name__ == "__main__":
    main()
