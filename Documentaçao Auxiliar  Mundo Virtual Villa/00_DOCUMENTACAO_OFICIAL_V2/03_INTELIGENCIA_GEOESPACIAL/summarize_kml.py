import json
import os
from collections import defaultdict

def format_area(m2):
    if m2 is None: return "N/A"
    return f"{m2/10000.0:.4f} ha"

def format_length(m):
    if m is None: return "N/A"
    return f"{m/1000.0:.3f} km"

def format_coords(lat, lon):
    if lat is None or lon is None: return ""
    return f"{lat:.6f}, {lon:.6f}"

def main():
    json_path = 'c:\\Users\\rober\\Downloads\\KML(2)\\kml_analysis.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    categories = defaultdict(list)
    
    # Categorization logic based on filename or name
    for item in data:
        name = item['name'].upper()
        filename = item['source_file'].upper()
        
        category = 'OUTROS'
        if 'MATA' in filename: category = 'VEGETACAO_NATIVA' # Forest
        elif 'RL ' in filename or 'RESERVA' in filename: category = 'RESERVA_LEGAL'
        elif 'APP' in filename: category = 'APP'
        elif 'PIV' in filename or 'PIVO' in filename: category = 'AGRICULTURA'
        elif 'CURRAL' in filename: category = 'PECUARIA_INFRA'
        elif 'CONFINAMENTO' in filename: category = 'PECUARIA_INFRA'
        elif 'PASTO' in filename: category = 'PECUARIA_PASTO'
        elif 'CASA' in filename or 'SEDE' in filename or 'ESCRITORIO' in filename: category = 'EDIFICACOES'
        elif 'POÇO' in filename or 'POCO' in filename: category = 'RECURSOS_HIDRICOS_POCOS'
        elif 'CORREGO' in filename or 'CÓRREGO' in filename: category = 'RECURSOS_HIDRICOS_RIOS'
        elif 'LAGOA' in filename or 'REPRESA' in filename: category = 'RECURSOS_HIDRICOS_LAGOS'
        elif 'BREJO' in filename: category = 'RECURSOS_HIDRICOS_BREJOS'
        elif 'AERODROMO' in filename or 'AERÓDROMO' in filename: category = 'INFRAESTRUTURA_GERAL'
        elif 'ESTRADA' in filename: category = 'INFRAESTRUTURA_ESTRADAS'
        elif 'FERROVIA' in filename: category = 'INFRAESTRUTURA_GERAL'
        elif 'SILO' in filename: category = 'INFRAESTRUTURA_ARMAZENAGEM'
        elif 'CERCA' in filename: category = 'INFRAESTRUTURA_CERCAS'
        elif 'PERIMETRO' in filename: category = 'LIMITES'
        
        categories[category].append(item)

    output_file = 'c:\\Users\\rober\\Downloads\\KML(2)\\final_report.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        def log(msg):
            print(msg)
            f.write(msg + '\n')
            
        log("# RELATÓRIO COMPLETO DE DADOS GEOESPACIAIS")
        log("\nEste documento consolida todas as informações extraídas dos arquivos KML/KMZ fornecidos, organizados por categoria para uso como banco de dados.\n")
        
        # Order of presentation
        cat_order = [
            'LIMITES',
            'AGRICULTURA',
            'PECUARIA_INFRA',
            'VEGETACAO_NATIVA',
            'RESERVA_LEGAL',
            'APP',
            'RECURSOS_HIDRICOS_POCOS',
            'RECURSOS_HIDRICOS_RIOS',
            'RECURSOS_HIDRICOS_LAGOS',
            'RECURSOS_HIDRICOS_BREJOS',
            'EDIFICACOES',
            'INFRAESTRUTURA_ARMAZENAGEM',
            'INFRAESTRUTURA_ESTRADAS',
            'INFRAESTRUTURA_CERCAS',
            'INFRAESTRUTURA_GERAL',
            'OUTROS'
        ]
        
        for cat in cat_order:
            items = categories.get(cat, [])
            if not items: continue
            
            log(f"## {cat.replace('_', ' ')}")
            
            # Calculate totals
            total_area = sum(i['properties'].get('area_m2', 0) for i in items if 'area_m2' in i['properties'])
            total_len = sum(i['properties'].get('length_m', 0) for i in items if 'length_m' in i['properties'])
            count = len(items)
            
            if total_area > 0:
                log(f"**Área Total:** {format_area(total_area)}")
            if total_len > 0:
                log(f"**Comprimento Total:** {format_length(total_len)}")
            log(f"**Quantidade de Registros:** {count}\n")
            
            # Table
            log("| Arquivo Fonte | Nome do Elemento | Tipo | Área (ha) | Comprimento (km) | Coordenadas Centrais (Lat, Lon) | Descrição |")
            log("|---|---|---|---|---|---|---|")
            
            for item in sorted(items, key=lambda x: x['source_file']):
                props = item['properties']
                centroid = props.get('centroid')
                coords_str = format_coords(centroid[0], centroid[1]) if centroid else ""
                
                # Additional detail for Pivots if in name
                name = item['name']
                desc = item['description'].replace('\n', ' ').strip()
                # Truncate desc if too long
                if len(desc) > 50: desc = desc[:47] + "..."
                
                area_ha = f"{props['area_ha']:.2f}" if 'area_ha' in props else "-"
                length_km = f"{props['length_km']:.2f}" if 'length_km' in props else "-"
                
                log(f"| {item['source_file']} | {name} | {item['type']} | {area_ha} | {length_km} | {coords_str} | {desc} |")
            
            log("\n")

if __name__ == '__main__':
    main()
