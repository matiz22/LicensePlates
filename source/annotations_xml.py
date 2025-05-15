import xml.etree.ElementTree as ET
from source.dataset import get_ue_kat_dataset

def load_annotations_dict(annotation_file):
    annotations_dict = {}
    try:
        tree = ET.parse(annotation_file)
        root = tree.getroot()

        for image in root.findall(".//image"):
            filename = image.get("name")
            for box in image.findall(".//box"):
                for attribute in box.findall('.//attribute[@name="plate number"]'):
                    annotations_dict[filename] = attribute.text.strip()
        return annotations_dict
    except FileNotFoundError:
        print(f"File {annotation_file} not found.")
        return {}
    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return {}

def check_plate_number(annotations, photo_filename):
    if isinstance(annotations, dict):
        return annotations.get(photo_filename)
    
    try:
        tree = ET.parse(annotations)
        root = tree.getroot()

        for image in root.findall(".//image"):
            if image.get("name") == photo_filename:
                for box in image.findall(".//box"):
                    for attribute in box.findall('.//attribute[@name="plate number"]'):
                        return attribute.text.strip()
        return None
    except FileNotFoundError:
        return None
    except ET.ParseError:
        return None

if __name__ == "__main__":
    print("Example usage:")
    print(load_annotations_dict(get_ue_kat_dataset()["annotations"]))
