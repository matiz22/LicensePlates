import xml.etree.ElementTree as ET


def check_plate_number(annotation_file, photo_filename):
    """Extract the plate number from an annotation file based on the given photo filename."""
    try:
        tree = ET.parse(annotation_file)
        root = tree.getroot()

        for image in root.findall(".//image"):
            if image.get("name") == photo_filename:
                for box in image.findall(".//box"):
                    for attribute in box.findall('.//attribute[@name="plate number"]'):
                        return attribute.text.strip()
        return f"No plate number found for {photo_filename}"
    except FileNotFoundError:
        return f"File {annotation_file} not found."
    except ET.ParseError as e:
        return f"Failed to parse XML file: {e}"
