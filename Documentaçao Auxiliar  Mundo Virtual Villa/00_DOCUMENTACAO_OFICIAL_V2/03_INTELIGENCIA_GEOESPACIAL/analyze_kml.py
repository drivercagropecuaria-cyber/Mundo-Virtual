import os
import zipfile
import math
import json
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError

# Constants
R_EARTH = 6371000  # meters

def haversine(lon1, lat1, lon2, lat2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_EARTH * c

def calculate_length(coords):
    length = 0
    for i in range(len(coords) - 1):
        length += haversine(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
    return length

def calculate_area(coords):
    if len(coords) < 3:
        return 0
    
    # Simple projection Area approximation
    # Calculate centroid latitude for scaling longitude
    lats = [p[1] for p in coords]
    mean_lat = sum(lats) / len(lats)
    
    lat_scale = 111320
    lon_scale = 111320 * math.cos(math.radians(mean_lat))
    
    area = 0
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        x1, y1 = coords[i][0] * lon_scale, coords[i][1] * lat_scale
        x2, y2 = coords[j][0] * lon_scale, coords[j][1] * lat_scale
        area += x1 * y2
        area -= y1 * x2
        
    return abs(area) / 2.0

def parse_coordinates(coord_str):
    coords = []
    # Normalize whitespace
    coord_str = coord_str.strip().replace('\n', ' ').replace('\t', ' ')
    points = coord_str.split(' ')
    for p in points:
        if not p.strip(): continue
        parts = p.split(',')
        if len(parts) >= 2:
            try:
                lon = float(parts[0])
                lat = float(parts[1])
                # parts[2] is altitude, usually 0
                coords.append((lon, lat))
            except ValueError:
                continue
    return coords

def extract_features(root, filename):
    features = []
    
    # KML often uses namespace, e.g., {http://earth.google.com/kml/2.0}
    # We will strip namespaces for easier parsing or use generic method
    
    # Recursive search for Placemarks
    # Because namespace can vary, we'll iterate all elements and check tag name
    
    for elem in root.iter():
        if elem.tag.endswith('Placemark'):
            feature = {
                'source_file': filename,
                'name': 'Unnamed',
                'description': '',
                'type': 'Unknown',
                'properties': {}
            }
            
            # Get Name
            name_elem = elem.find('./*[local-name()="name"]')
            if name_elem is not None: feature['name'] = name_elem.text if name_elem.text else 'Unnamed'
            else:
                # Try finding name with namespace
                found_name = False
                for child in elem:
                    if child.tag.endswith('name'):
                        feature['name'] = child.text if child.text else 'Unnamed'
                        found_name = True
                        break
                        
            # Get Description
            desc_elem = elem.find('./*[local-name()="description"]')
            if desc_elem is not None: feature['description'] = desc_elem.text if desc_elem.text else ''
            else:
                 for child in elem:
                    if child.tag.endswith('description'):
                        feature['description'] = child.text if child.text else ''

            # Check Geometry
            # Polygon
            polygon = None
            for child in elem.iter():
                if child.tag.endswith('Polygon'):
                    polygon = child
                    break
            
            line_string = None
            for child in elem.iter():
                if child.tag.endswith('LineString'):
                    line_string = child
                    break
            
            point = None
            for child in elem.iter():
                if child.tag.endswith('Point'):
                    point = child
                    break
            
            if polygon is not None:
                feature['type'] = 'Polygon'
                # Find coordinates
                coords_elem = None
                for sub in polygon.iter():
                    if sub.tag.endswith('coordinates'):
                        coords_elem = sub
                        break
                if coords_elem is not None and coords_elem.text:
                    coords = parse_coordinates(coords_elem.text)
                    area_sqm = calculate_area(coords)
                    feature['properties']['area_ha'] = area_sqm / 10000.0
                    feature['properties']['area_m2'] = area_sqm
                    if len(coords) > 0:
                        feature['properties']['centroid'] = (sum(c[1] for c in coords)/len(coords), sum(c[0] for c in coords)/len(coords))

            elif line_string is not None:
                feature['type'] = 'LineString'
                coords_elem = None
                for sub in line_string.iter():
                    if sub.tag.endswith('coordinates'):
                        coords_elem = sub
                        break
                if coords_elem is not None and coords_elem.text:
                    coords = parse_coordinates(coords_elem.text)
                    length_m = calculate_length(coords)
                    feature['properties']['length_m'] = length_m
                    feature['properties']['length_km'] = length_m / 1000.0
                    if len(coords) > 0:
                         feature['properties']['centroid'] = (coords[0][1], coords[0][0]) # Start point

            elif point is not None:
                feature['type'] = 'Point'
                coords_elem = None
                for sub in point.iter():
                    if sub.tag.endswith('coordinates'):
                        coords_elem = sub
                        break
                if coords_elem is not None and coords_elem.text:
                    coords = parse_coordinates(coords_elem.text)
                    if len(coords) > 0:
                        feature['properties']['lat'] = coords[0][1]
                        feature['properties']['lon'] = coords[0][0]
                        feature['properties']['centroid'] = (coords[0][1], coords[0][0])
            
            features.append(feature)
            
    return features

def main():
    folder_path = r'c:\Users\rober\Downloads\KML(2)\KML'
    
    # Handle if path does not exist or files are in root
    if not os.path.exists(folder_path):
        folder_path = r'c:\Users\rober\Downloads\KML(2)'
        
    all_features = []
    
    try:
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.kml') or f.lower().endswith('.kmz')]
    except FileNotFoundError:
        print(f"Could not find folder {folder_path}")
        return

    print(f"Found {len(files)} files.")
    
    for f in files:
        full_path = os.path.join(folder_path, f)
        try:
            if f.lower().endswith('.kmz'):
                with zipfile.ZipFile(full_path, 'r') as z:
                    kml_content = None
                    for name in z.namelist():
                        if name.endswith('.kml'):
                            kml_content = z.read(name)
                            break
                    if kml_content:
                        try:
                            root = ET.fromstring(kml_content)
                            all_features.extend(extract_features(root, f))
                        except Exception as e:
                            print(f"Error parsing XML in {f}: {e}")
            else:
                try:
                    tree = ET.parse(full_path)
                    root = tree.getroot()
                    all_features.extend(extract_features(root, f))
                except Exception as e:
                    print(f"Error parsing XML in {f}: {e}")
        except Exception as e:
            print(f"Error opening {f}: {e}")
            
    output_path = os.path.join(os.path.dirname(folder_path), 'kml_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_features, f, indent=2, ensure_ascii=False)
        
    print(f"Processed {len(all_features)} features. Output saved to {output_path}")

if __name__ == '__main__':
    main()
