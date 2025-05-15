import os
import time
import cv2
from pathlib import Path
from paddleocr import PaddleOCR

from ocr_utils.clean_plate import clean_license_plate_text
from ocr_utils.validate_registration import validate_registration

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

def process_ocr_results(ocr_result, best_conf=0, detected_text="", raw_detected_text=""):
    if not ocr_result or not isinstance(ocr_result, list) or not ocr_result[0]:
        return best_conf, detected_text, raw_detected_text
    
    results_list = ocr_result[0] if isinstance(ocr_result[0], list) else ocr_result
    for line in results_list:
        if not isinstance(line, list) or len(line) <= 1 or not isinstance(line[1], tuple):
            continue
            
        confidence = line[1][1]
        text = line[1][0]
        cleaned_text = clean_license_plate_text(text.strip())
        
        if len(cleaned_text) < 5 or len(cleaned_text) > 8:
            continue
        if not validate_registration(cleaned_text):
            continue
        if confidence > best_conf:
            best_conf = confidence
            detected_text = cleaned_text
            raw_detected_text = text
            
    return best_conf, detected_text, raw_detected_text

def process_detected_plates(output_dir, annotations_dict, lang='en'):
    total_start_time = time.time()
    ocr = PaddleOCR(use_gpu=True, use_angle_cls=True, lang=lang, show_log=False)
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
        best_conf = 0
        image_start_time = time.time()
        
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise Exception("Image not found")
                
            binary_img = preprocess_image(image_path)
            variants = [img]
            if binary_img is not None:
                variants.append(binary_img)
                
            # Process each image variant
            for v in variants:
                temp_path = os.path.join(output_dir, f"__temp_{image_file}")
                cv2.imwrite(temp_path, v)
                ocr_result = ocr.ocr(temp_path, cls=True)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
                best_conf, detected_text, raw_detected_text = process_ocr_results(
                    ocr_result, best_conf, detected_text, raw_detected_text)
                    
            # Try original image if no text detected
            if not detected_text:
                ocr_result = ocr.ocr(image_path, cls=True)
                best_conf, detected_text, raw_detected_text = process_ocr_results(
                    ocr_result, best_conf, detected_text, raw_detected_text)
                    
        except Exception as e:
            detected_text = ""
            raw_detected_text = ""
            
        image_process_time = time.time() - image_start_time
        total_ocr_time += image_process_time
        
        # Update timing stats
        if image_process_time < results['timing']['fastest_image']['time']:
            results['timing']['fastest_image'] = {'file': image_file, 'time': image_process_time}
        if image_process_time > results['timing']['slowest_image']['time']:
            results['timing']['slowest_image'] = {'file': image_file, 'time': image_process_time}
            
        # Compare with ground truth
        ground_truth = annotations_dict.get(original_filename)
        clean_ground_truth = clean_license_plate_text(ground_truth) if ground_truth else None
        is_correct = False
        
        if clean_ground_truth and detected_text:
            is_correct = detected_text == clean_ground_truth
            
        if is_correct:
            results['correct'] += 1
        else:
            ocr_valid = validate_registration(detected_text) if detected_text else False
            truth_valid = validate_registration(clean_ground_truth) if clean_ground_truth else False
            print(f"✗ {image_file}: OCR='{detected_text}' (regex: {ocr_valid}), Truth='{clean_ground_truth}' (regex: {truth_valid})")
            
        results['details'].append({
            'image_file': image_file,
            'original_file': original_filename,
            'raw_detected_text': raw_detected_text,
            'cleaned_detected_text': detected_text,
            'ground_truth': ground_truth,
            'cleaned_ground_truth': clean_ground_truth,
            'is_correct': is_correct,
            'process_time': image_process_time
        })
        
    # Calculate stats
    accuracy = (results['correct'] / results['total']) * 100 if results['total'] > 0 else 0
    total_execution_time = time.time() - total_start_time
    results['timing']['total_time'] = total_execution_time
    results['timing']['ocr_time'] = total_ocr_time
    results['timing']['average_per_image'] = total_ocr_time / results['total'] if results['total'] > 0 else 0
    estimated_time_100 = results['timing']['average_per_image'] * 100
    
    print(f"\nOCR Summary: {results['correct']}/{results['total']} correct ({accuracy:.2f}%)")
    print(f"OCR Time: {total_ocr_time:.2f}s (avg: {results['timing']['average_per_image']:.4f}s/img, est. 100 imgs: {estimated_time_100:.2f}s)")
    
    return results
