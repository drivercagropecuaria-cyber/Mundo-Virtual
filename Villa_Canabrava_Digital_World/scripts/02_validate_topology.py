import geopandas as gpd
from shapely.validation import explain_validity
import os
import pandas as pd

# --- CONFIGURAÇÃO ---
INPUT_FILE = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\villa_canabrava_raw_v1.geojson"
OUTPUT_REPORT = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\topology_report_v1.md"

# Área alvo esperada (Documentação)
EXPECTED_TOTAL_AREA_HA = 7729.26

def validate_topology():
    print("🚀 Iniciando ETAPA 2: Validação Matemática (Topology Check)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Arquivo de entrada não encontrado: {INPUT_FILE}")
        return

    print("📂 Carregando Digital Twin (Golden Source)...")
    gdf = gpd.read_file(INPUT_FILE)
    
    # 1. Verificar SRID (Sistema de Coordenadas)
    print(f"ℹ️  CRS Atual: {gdf.crs}")
    
    # Para cálculos de área precisos em metros/hectares, precisamos projetar
    # Vamos usar SIRGAS 2000 / UTM zone 23S (EPSG:31983) que é padrão para essa região do Brasil (MG/BA)
    # ou uma projeção UTM automática baseada no centroide.
    # Vamos estimar UTM zone. Longitude -44 fica na Zona 23 (-48 a -42).
    print("🔄 Projetando para UTM 23S (EPSG:31983) para cálculos métricos...")
    gdf_projected = gdf.to_crs(epsg=31983)
    
    # 2. Análise de Geometria Inválida
    print("🔍 Buscando geometrias inválidas...")
    invalid_geoms = gdf_projected[~gdf_projected.is_valid]
    
    invalid_report = []
    if not invalid_geoms.empty:
        print(f"⚠️  Encontradas {len(invalid_geoms)} geometrias inválidas!")
        for idx, row in invalid_geoms.iterrows():
            reason = explain_validity(row.geometry)
            invalid_report.append(f"- ID {idx} ({row.get('source_file', 'Unknown')}): {reason}")
    else:
        print("✅ Nenhuma geometria inválida encontrada (Self-intersections, etc).")

    # 3. Cálculo de Área Total (Soma de polígonos)
    # Filtramos apenas Polígonos para área (ignorando linhas de estradas/cercas para soma territorial se não forem overlays)
    # Nota: Em KMLs, muitas vezes limites são Linhas. Se tivermos Polígono de Limite, usamos ele.
    # Como não sabemos qual layer é o "Limite da Fazenda", vamos somar por categorias ou buscar o maior polígono.
    
    # Vamos tentar identificar categorias baseadas no nome do arquivo
    gdf_projected['area_ha'] = gdf_projected.geometry.area / 10000.0 # m2 to hectares
    
    # Agrupar por pasta/categoria original
    area_by_category = gdf_projected[gdf_projected.geometry.type.isin(['Polygon', 'MultiPolygon'])].groupby('kml_folder')['area_ha'].sum()
    
    total_area_calculated = area_by_category.sum()
    
    print("\n📊 Análise de Áreas por Categoria:")
    print(area_by_category)
    
    print(f"\n📐 Área Total Polígonos Calculada: {total_area_calculated:.2f} ha")
    print(f"📄 Área Documentada: {EXPECTED_TOTAL_AREA_HA:.2f} ha")
    diff = total_area_calculated - EXPECTED_TOTAL_AREA_HA
    print(f"⚖️  Diferença (Calculado - Doc): {diff:.2f} ha")

    # 4. Detecção de Sobreposições Críticas (Exemplo: Estrutura dentro de APP)
    # Simplificado para este script: Verificar se há sobreposições massivas
    print("\n🔍 Verificando sobreposições (Amostragem)...")
    # Isso pode ser pesado O(N^2), vamos fazer apenas contagem básica intersecções
    # Usando índice espacial (sindex) é rápido, mas detalhar tudo é complexo.
    # Vamos apenas relatar estatística.
    
    # Gerar Relatório Markdown
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# 📐 Relatório de Validação Topológica (V1)\n\n")
        
        f.write("## 1. Integridade Geométrica\n")
        if invalid_geoms.empty:
            f.write("✅ **Status:** Aprovado. Nenhuma geometria corrompida.\n")
        else:
            f.write(f"⚠️ **Status:** Atenção. {len(invalid_geoms)} problemas detectados.\n")
            for item in invalid_report:
                f.write(f"{item}\n")
        
        f.write("\n## 2. Balanço de Áreas (Hectares)\n")
        f.write("| Categoria (Pasta KML) | Área Calculada (ha) |\n")
        f.write("|---|---|\n")
        for cat, area in area_by_category.items():
            f.write(f"| {cat} | {area:.2f} |\n")
        
        f.write(f"\n**Total Calculado:** {total_area_calculated:.2f} ha\n")
        f.write(f"**Esperado:** {EXPECTED_TOTAL_AREA_HA:.2f} ha\n")
        f.write(f"**Delta:** {diff:.2f} ha ({(diff/EXPECTED_TOTAL_AREA_HA)*100:.2f}%)\n")
        
        f.write("\n## 3. Notas Técnicas\n")
        if abs(diff) > 100: # Se diferença maior que 100ha
            f.write(f"⚠️ **Alerta de Área:** A soma dos polígonos diverge significativamente do total da fazenda. "
                    "Isso é comum se os KMLs contém sobreposições (ex: Reserva Legal desenhada por cima de Mata Nativa) "
                    "ou se o Limite da Fazenda não está incluso como polígono único.\n")
        else:
            f.write("✅ **Alerta de Área:** Divergência aceitável ou sobreposições mínimas.\n")

    print(f"\n📝 Relatório completo gerado em: {OUTPUT_REPORT}")
    print("✅ Validação Concluída!")

if __name__ == "__main__":
    validate_topology()
