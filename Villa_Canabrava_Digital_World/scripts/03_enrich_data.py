import geopandas as gpd
import pandas as pd
import unidecode
import os

# --- CONFIGURAÇÃO ---
INPUT_FILE = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\villa_canabrava_raw_v1.geojson"
OUTPUT_FILE = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\villa_canabrava_semantic_v1.geojson"

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    return unidecode.unidecode(text).lower()

def enrich_data():
    print("🚀 Iniciando ETAPA 3: Enriquecimento Semântico (Semantic Tagging)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Arquivo de entrada não encontrado: {INPUT_FILE}")
        return

    print("📂 Carregando Dados Brutos...")
    gdf = gpd.read_file(INPUT_FILE)
    
    print("🏷️  Aplicando regras de Game Design...")

    # --- DICIONÁRIO DE REGRAS ---
    # Estrutura: 'palavra_chave': { 'tags': ... }
    
    def apply_tags(row):
        # Tentar obter nome da layer ou description, se falhar usar source_file
        name = normalize_text(row.get('Name', ''))
        folder = normalize_text(row.get('kml_folder', ''))
        filename = normalize_text(row.get('source_file', ''))
        
        full_context = f"{name} {folder} {filename}"
        
        tags = {
            'game_layer': 'Info',        # Layer padrão
            'render_type': 'none',       # Não renderizar por padrão
            'collision': False,          # Sem colisão
            'asset_class': 'InfoActor'   # Classe genérica
        }

        # REGRA 1: SISTEMAS DE IRRIGAÇÃO (PIVÔS)
        if 'pivo' in full_context:
            tags.update({
                'game_layer': 'Infrastructure_Irrigation',
                'render_type': 'blueprint_actor',
                'asset_class': 'BP_PivotSystem',
                'anim_loop': 'rotate_slow',
                'collision': True
            })
        
        # REGRA 2: CERCAS
        elif 'cerca' in full_context:
            tags.update({
                'game_layer': 'Infrastructure_Fencing',
                'render_type': 'spline_mesh',
                'asset_class': 'BP_Fence_Wooden_01',
                'collision': True
            })
            
        # REGRA 3: MATA E VEGETAÇÃO (Física)
        elif 'mata' in full_context and 'reserva' not in full_context:
            tags.update({
                'game_layer': 'Environment_Vegetation',
                'render_type': 'procedural_volume',
                'asset_class': 'PCG_Cerrado_Biome', # Procedural Content Generation
                'density': 0.8,
                'is_overlay': False
            })
            
        # REGRA 4: RESERVA LEGAL E APP (Lógica/Sobreposição)
        elif 'reserva' in full_context or 'app' in full_context:
            tags.update({
                'game_layer': 'Data_Overlay_Environmental',
                'render_type': 'ui_overlay',
                'asset_class': 'UI_Zone_Indicator',
                'color_hex': '#00FF0055', # Verde translúcido
                'is_overlay': True
            })

        # REGRA 5: CORPOS D'ÁGUA
        elif 'lagoa' in full_context or 'represa' in full_context or 'corrego' in full_context:
            tags.update({
                'game_layer': 'Environment_Water',
                'render_type': 'water_body',
                'asset_class': 'BP_WaterLakes',
                'physics_volume': 'WaterVolume'
            })
            
        # REGRA 6: ESTRADAS
        elif 'estrada' in full_context:
            tags.update({
                'game_layer': 'Infrastructure_Roads',
                'render_type': 'spline_road',
                'asset_class': 'BP_DirtRoad_01',
                'nav_modifier': 'Road'
            })
            
        # REGRA 7: ESTRUTURAS CIVIS (Casas, Galpões)
        elif 'casa' in full_context or 'sede' in full_context or 'fabric' in full_context:
             tags.update({
                'game_layer': 'Structures_Civil',
                'render_type': 'static_mesh',
                'asset_class': 'SM_FarmHouse_Generic', # Placeholder
                'collision': True
            })

        return pd.Series(tags)

    # Aplicar função a todas as linhas
    tag_columns = gdf.apply(apply_tags, axis=1)
    
    # Concatenar tags com o GeoDataFrame original
    gdf_enriched = pd.concat([gdf, tag_columns], axis=1)
    
    # Filtrar colunas relevantes para exportação (limpar o geojson final)
    # Manter geometry e colunas novas, mais algumas originais importantes
    cols_to_keep = ['geometry', 'Name', 'Description', 'source_file', 'game_layer', 
                    'render_type', 'asset_class', 'collision', 'anim_loop', 'color_hex', 
                    'density', 'is_overlay', 'physics_volume', 'nav_modifier']
    
    # Garantir que só colunas existentes sejam selecionadas
    final_cols = [c for c in cols_to_keep if c in gdf_enriched.columns]
    gdf_final = gdf_enriched[final_cols]
    
    print("\n📊 Resumo da Classificação (Contagem por Tipo de Render):")
    print(gdf_final['render_type'].value_counts())

    print(f"\n💾 Salvando Arquivo Enriquecido em: {OUTPUT_FILE}")
    gdf_final.to_file(OUTPUT_FILE, driver='GeoJSON')
    print("✅ Enriquecimento Concluído!")

if __name__ == "__main__":
    enrich_data()
