import os
import geopandas as gpd
import pandas as pd
import fiona
from shapely.geometry import shape
import warnings

# --- CONFIGURAÇÃO ---
# Caminho da pasta que contém os KMLs (Documentação Oficial)
SOURCE_KML_DIR = r"c:\Users\rober\Downloads\Documentaçao Auxiliar  Mundo Virtual Villa\00_DOCUMENTACAO_OFICIAL_V2\03_INTELIGENCIA_GEOESPACIAL"
# Caminho de saída
OUTPUT_FILE = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\villa_canabrava_raw_v1.geojson"

# Habilitar suporte KML no Fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

def ingest_kmls(source_dir):
    print(f"🚀 Iniciando ingestão do 'Grande Filtro'...")
    print(f"📂 Lendo KMLs de: {source_dir}")

    all_features = []
    
    # Percorrer recursivamente
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.kml'):
                file_path = os.path.join(root, file)
                try:
                    # Ler KML usando GeoPandas
                    # Nota: KMLs podem ter múltiplas camadas, mas geralmente gdf.read_file lê a primeira
                    # Para ser robusto, iteramos camadas se fiona permitir, mas gpd.read_file é comumente suficiente para estrutura simples
                    gdf = gpd.read_file(file_path, driver='KML')
                    
                    if not gdf.empty:
                        # Adicionar metadados de origem
                        gdf['source_file'] = file
                        gdf['kml_folder'] = os.path.basename(root)
                        all_features.append(gdf)
                        print(f"  ✅ Lido: {file} ({len(gdf)} features)")
                    else:
                        print(f"  ⚠️ Vazio: {file}")
                
                except Exception as e:
                    print(f"  ❌ Erro ao ler {file}: {str(e)}")

    if not all_features:
        print("❌ Nenhum dado KML válido encontrado.")
        return

    # Consolidar tudo
    print("🔄 Consolidando dados...")
    full_gdf = pd.concat(all_features, ignore_index=True)
    
    # Converter de volta para GeoDataFrame (concat perde a classe as vezes)
    full_gdf = gpd.GeoDataFrame(full_gdf, geometry='geometry')
    
    # Definir CRS se estiver faltando (KML é sempre 4326, mas garantimos)
    if full_gdf.crs is None:
        full_gdf.set_crs(epsg=4326, inplace=True)
    else:
        full_gdf.to_crs(epsg=4326, inplace=True)

    # Limpeza Básica
    print("🧹 Limpando geometrias nulas...")
    original_len = len(full_gdf)
    full_gdf = full_gdf.dropna(subset=['geometry'])
    full_gdf = full_gdf[full_gdf.geometry.is_valid] # Remover geometrias inválidas
    
    print(f"📊 Estatísticas Finais:")
    print(f"   - Total Arquivos Lidos: {len(all_features)}")
    print(f"   - Total Elementos (Features): {len(full_gdf)}")
    print(f"   - Descartados (Inválidos/Nulos): {original_len - len(full_gdf)}")

    # Salvar GeoJSON
    print(f"💾 Salvando 'Golden Source' em: {OUTPUT_FILE}")
    full_gdf.to_file(OUTPUT_FILE, driver='GeoJSON')
    print("✅ Ingestão Concluída com Sucesso!")

if __name__ == "__main__":
    ingest_kmls(SOURCE_KML_DIR)
