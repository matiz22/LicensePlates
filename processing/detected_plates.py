import os
import time
import json
from pathlib import Path
from paddleocr import PaddleOCR

from ocr_utils.clean_plate import clean_license_plate_text
from ocr_utils.length_plate import is_valid_plate_length


def process_detected_plates(output_dir, annotations_dict, lang='en', save_results=True):
    total_start_time = time.time()

    ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    results = {
        'total': 0,
        'correct': 0,
        'incorrect': 0,
        'details': [],
        'timing': {
            'total_time': 0,
            'average_per_image': 0,
            'fastest_image': {'file': '', 'time': float('inf')},
            'slowest_image': {'file': '', 'time': 0}
        }
    }

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [f for f in os.listdir(output_dir)
                   if os.path.isfile(os.path.join(output_dir, f))
                   and Path(f).suffix.lower() in image_extensions]

    results['total'] = len(image_files)

    total_ocr_time = 0

    for image_file in image_files:
        image_path = os.path.join(output_dir, image_file)
        original_filename = image_file

        detected_text = ""
        raw_detected_text = ""

        image_start_time = time.time()

        try:
            ocr_result = ocr.ocr(image_path, cls=True)

            if ocr_result:
                if isinstance(ocr_result, list) and len(ocr_result) > 0:
                    if isinstance(ocr_result[0], list):
                        results_list = ocr_result[0]
                    else:
                        results_list = ocr_result

                    best_text = ""
                    best_conf = 0
                    valid_text_found = False

                    for line in results_list:
                        if isinstance(line, list) and len(line) > 1 and isinstance(line[1], tuple):
                            confidence = line[1][1]
                            text = line[1][0]
                            cleaned_text = clean_license_plate_text(text.strip())

                            if is_valid_plate_length(cleaned_text) and confidence > best_conf:
                                best_conf = confidence
                                best_text = text
                                valid_text_found = True

                    if not valid_text_found and results_list:
                        for line in results_list:
                            if isinstance(line, list) and len(line) > 1 and isinstance(line[1], tuple):
                                confidence = line[1][1]
                                text = line[1][0]
                                if confidence > best_conf:
                                    best_conf = confidence
                                    best_text = text

                    raw_detected_text = best_text.strip()
                    detected_text = clean_license_plate_text(raw_detected_text)
        except Exception as e:
            detected_text = ""
            raw_detected_text = ""

        image_process_time = time.time() - image_start_time
        total_ocr_time += image_process_time

        if image_process_time < results['timing']['fastest_image']['time']:
            results['timing']['fastest_image'] = {'file': image_file, 'time': image_process_time}
        if image_process_time > results['timing']['slowest_image']['time']:
            results['timing']['slowest_image'] = {'file': image_file, 'time': image_process_time}

        ground_truth = annotations_dict.get(original_filename)

        if ground_truth:
            clean_ground_truth = clean_license_plate_text(ground_truth)
        else:
            clean_ground_truth = None

        is_correct = False
        if clean_ground_truth and detected_text:
            is_correct = detected_text == clean_ground_truth

        if is_correct:
            results['correct'] += 1
        else:
            results['incorrect'] += 1
            # Only print when there's a mismatch
            print(f"✗ {image_file}: OCR='{detected_text}', Truth='{clean_ground_truth}'")

        detail = {
            'image_file': image_file,
            'original_file': original_filename,
            'raw_detected_text': raw_detected_text,
            'cleaned_detected_text': detected_text,
            'ground_truth': ground_truth,
            'cleaned_ground_truth': clean_ground_truth,
            'is_correct': is_correct,
            'process_time': image_process_time
        }

        results['details'].append(detail)

    accuracy = (results['correct'] / results['total']) * 100 if results['total'] > 0 else 0

    total_execution_time = time.time() - total_start_time

    results['timing']['total_time'] = total_execution_time
    results['timing']['ocr_time'] = total_ocr_time
    results['timing']['average_per_image'] = total_ocr_time / results['total'] if results['total'] > 0 else 0
    
    estimated_time_100 = results['timing']['average_per_image'] * 100

    print(f"\nOCR Summary: {results['correct']}/{results['total']} correct ({accuracy:.2f}%)")
    print(f"OCR Time: {total_ocr_time:.2f}s (avg: {results['timing']['average_per_image']:.4f}s/img, est. 100 imgs: {estimated_time_100:.2f}s)")

    if save_results:
        results_file = os.path.join(os.path.dirname(output_dir), "ocr_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=4)

    return results
