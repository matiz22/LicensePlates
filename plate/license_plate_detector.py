import cv2
import time
from pathlib import Path
from ultralytics import YOLO

def detect_and_save_license_plates(input_dir, output_dir=None, conf_threshold=0.25):
    input_path = Path(input_dir)
    if output_dir is None:
        output_path = input_path / "detected_plates"
    else:
        output_path = Path(output_dir)
    
    output_path.mkdir(exist_ok=True, parents=True)
    
    start_time_total = time.time()
    model = YOLO("model/license_plate_detector.pt")
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
    
    count = 0
    
    for img_path in image_files:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        
        results = model(img, conf=conf_threshold)
        
        for i, result in enumerate(results):
            boxes = result.boxes
            for j, box in enumerate(boxes):
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                
                plate_img = img[y1:y2, x1:x2]
                
                output_file_path = output_path / img_path.name
                
                cv2.imwrite(str(output_file_path), plate_img)
                count += 1
    
    total_elapsed_time = time.time() - start_time_total
    
    num_images = len(image_files)
    avg_time_per_image = total_elapsed_time / num_images if num_images > 0 else 0
    estimated_time_100 = avg_time_per_image * 100
    
    print(f"Detection Summary: {count} plates from {num_images} images")
    print(f"Detection Time: {total_elapsed_time:.2f}s (avg: {avg_time_per_image:.4f}s/img, est. 100 imgs: {estimated_time_100:.2f}s)")
    
    return count, total_elapsed_time, avg_time_per_image

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect and save license plates from images")
    parser.add_argument("--input", "-i", required=True, help="Directory containing images")
    parser.add_argument("--output", "-o", help="Directory to save detected license plates")
    parser.add_argument("--conf", "-c", type=float, default=0.25, help="Confidence threshold")
    
    args = parser.parse_args()
    
    detect_and_save_license_plates(args.input, args.output, args.conf)
