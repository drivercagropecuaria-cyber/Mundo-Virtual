import os
import xml.etree.ElementTree as ET

path = r'c:\Users\rober\Downloads\KML(2)\KML'
files = os.listdir(path)
print(f"Files in {path}: {len(files)}")
target = os.path.join(path, 'Aeródromo.kml')
if os.path.exists(target):
    print(f"Found {target}")
    try:
        tree = ET.parse(target)
        root = tree.getroot()
        print(f"Root tag: {root.tag}")
        count = 0
        for elem in root.iter():
            if elem.tag.endswith('Placemark'):
                count += 1
        print(f"Found {count} placemarks.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File not found.")
