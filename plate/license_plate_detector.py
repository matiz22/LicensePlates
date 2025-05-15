import cv2
import time
import torch
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
    
    model.model.eval()
    torch.set_grad_enabled(False)
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
    
    count = 0
    
    batch_size = 4
    for i in range(0, len(image_files), batch_size):
        batch_paths = image_files[i:i+batch_size]
        batch_images = []
        batch_originals = []
        
        for img_path in batch_paths:
            img = cv2.imread(str(img_path))
            if img is not None:
                batch_images.append(img)
                batch_originals.append((img_path, img))
            
        if not batch_images:
            continue
            
        results = model(batch_images, conf=conf_threshold)
        
        for idx, result in enumerate(results):
            img_path, original_img = batch_originals[idx]
            boxes = result.boxes
            
            if len(boxes) == 0:
                continue
                
            for box in boxes:
                try:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    
                    h, w = original_img.shape[:2]
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    
                    if x2 <= x1 or y2 <= y1:
                        continue
                        
                    plate_img = original_img[y1:y2, x1:x2]
                    output_file_path = output_path / img_path.name
                    cv2.imwrite(str(output_file_path), plate_img)
                    count += 1
                    
                    break
                except (IndexError, ValueError) as e:
                    continue
    
    total_elapsed_time = time.time() - start_time_total
    
    num_images = len(image_files)
    avg_time_per_image = total_elapsed_time / num_images if num_images > 0 else 0
    estimated_time_100 = avg_time_per_image * 100
    
    print(f"Detection Summary: {count} plates from {num_images} images")
    print(f"Detection Time: {total_elapsed_time:.2f}s (avg: {avg_time_per_image:.4f}s/img, est. 100 imgs: {estimated_time_100:.2f}s)")
    
    return count, total_elapsed_time, avg_time_per_image
