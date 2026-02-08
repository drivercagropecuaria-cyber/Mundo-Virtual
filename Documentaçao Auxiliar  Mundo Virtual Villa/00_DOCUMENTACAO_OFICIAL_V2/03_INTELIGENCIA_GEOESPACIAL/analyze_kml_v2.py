import os
import zipfile
import math
import json
import xml.etree.ElementTree as ET

# Constants
R_EARTH = 6371000  # meters

def haversine(lon1, lat1, lon2, lat2):
    try:
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        val = math.sqrt(a)
        # clamp for float errors
        if val > 1: val = 1
        c = 2 * math.asin(val) 
        return R_EARTH * c
    except Exception:
        return 0

def calculate_length(coords):
    length = 0
    for i in range(len(coords) - 1):
        length += haversine(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
    return length

def calculate_area(coords):
    if len(coords) < 3:
        return 0
    
    try:
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
    except Exception:
        return 0

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
                coords.append((lon, lat))
            except ValueError:
                continue
    return coords

def extract_features(root, filename):
    features = []
    for elem in root.iter():
        if elem.tag.endswith('Placemark'):
            feature = {
                'source_file': filename,
                'name': 'Unnamed',
                'description': '',
                'type': 'Unknown',
                'properties': {}
            }
            
            # Name
            for child in elem:
                if child.tag.endswith('name') and child.text:
                    feature['name'] = child.text
                    break
            
            # Description
            for child in elem:
                if child.tag.endswith('description') and child.text:
                    feature['description'] = child.text
                    break

            # Geometry
            geom_found = False
            for child in elem.iter():
                if child.tag.endswith('Polygon'):
                    feature['type'] = 'Polygon'
                    geom_found = True
                    # Coordinates
                    for sub in child.iter():
                        if sub.tag.endswith('coordinates') and sub.text:
                            coords = parse_coordinates(sub.text)
                            if coords:
                                area = calculate_area(coords)
                                feature['properties']['area_ha'] = area / 10000.0
                                feature['properties']['area_m2'] = area
                                feature['properties']['centroid'] = (sum(c[1] for c in coords)/len(coords), sum(c[0] for c in coords)/len(coords))
                            break
                    break
                elif child.tag.endswith('LineString'):
                    feature['type'] = 'LineString'
                    geom_found = True
                    for sub in child.iter():
                        if sub.tag.endswith('coordinates') and sub.text:
                            coords = parse_coordinates(sub.text)
                            if coords:
                                length = calculate_length(coords)
                                feature['properties']['length_m'] = length
                                feature['properties']['length_km'] = length / 1000.0
                                feature['properties']['centroid'] = (coords[0][1], coords[0][0])
                            break
                    break
                elif child.tag.endswith('Point'):
                    feature['type'] = 'Point'
                    geom_found = True
                    for sub in child.iter():
                        if sub.tag.endswith('coordinates') and sub.text:
                            coords = parse_coordinates(sub.text)
                            if coords:
                                feature['properties']['centroid'] = (coords[0][1], coords[0][0])
                            break
                    break
            
            features.append(feature)
            
    return features

def main():
    folder_path = r'c:\Users\rober\Downloads\KML(2)\KML'
    print(f"Scanning {folder_path}...")
    
    if not os.path.exists(folder_path):
        print(f"Path does not exist: {folder_path}")
        return

    all_features = []
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.kml') or f.lower().endswith('.kmz')]
    print(f"Found {len(files)} KML/KMZ files.")
    
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
                        root = ET.fromstring(kml_content)
                        feats = extract_features(root, f)
                        all_features.extend(feats)
            else:
                tree = ET.parse(full_path)
                root = tree.getroot()
                feats = extract_features(root, f)
                all_features.extend(feats)
        except Exception as e:
            print(f"Error processing {f}: {e}")

    print(f"Extracted {len(all_features)} features.")
    
    out_path = r'c:\Users\rober\Downloads\KML(2)\kml_analysis.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_features, f, indent=2, ensure_ascii=False)
    print(f"Saved to {out_path}")

if __name__ == '__main__':
    main()
