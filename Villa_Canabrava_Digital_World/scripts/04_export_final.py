import geopandas as gpd
import os
import json
from datetime import datetime

# --- CONFIGURAÇÃO ---
INPUT_FILE = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\processed\villa_canabrava_semantic_v1.geojson"
OUTPUT_DIR = r"c:\Users\rober\Downloads\Villa_Canabrava_Digital_World\data\final_export"
OUTPUT_FILENAME = "VILLA_CANABRAVA_DIGITAL_TWIN_GOLDEN.geojson"
README_FILENAME = "README_IMPORTAR_NA_ENGINE.md"

def export_final():
    print("🚀 Iniciando ETAPA 4: Exportação Final (Golden Source)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Arquivo de entrada não encontrado: {INPUT_FILE}")
        return

    # Criar diretório final se não existir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    readme_path = os.path.join(OUTPUT_DIR, README_FILENAME)

    print("📂 Carregando Dados Enriquecidos...")
    gdf = gpd.read_file(INPUT_FILE)
    
    # Otimização: Arredondar coordenadas para 6 casas decimais (~10cm de precisão) para reduzir tamanho
    # Nota: GeoPandas não tem função nativa fácil para isso sem recriar geometrias, 
    # mas o driver GeoJSON aceita 'coordinate_precision'.
    
    print(f"💾 Salvando 'Golden Source' em: {output_path}")
    gdf.to_file(output_path, driver='GeoJSON', engine='pyogrio') 
    
    # Gerar Estatísticas para o README
    stats = gdf['render_type'].value_counts().to_dict()
    total_objs = len(gdf)
    
    print("📝 Gerando Documentação de Importação...")
    
    readme_content = f"""# 🌍 VILLA CANABRAVA DIGITAL TWIN - PACOTE DE IMPORTAÇÃO
**Data de Geração:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Arquivo Mestre:** `{OUTPUT_FILENAME}`
**Total de Objetos:** {total_objs}

---

## 🎨 COMO IMPORTAR NA GAME ENGINE (UNITY/UNREAL)

Este arquivo GeoJSON contém metadados ("Tags Semânticas") para automação.
Não importe como geometria simples! Use um script de "Spawn" para ler as propriedades.

### 📋 Mapeamento de Classes (Render Types)

| Render Type (Tag) | Qtd | Ação Recomendada (Blueprint/Prefab) |
|-------------------|-----|-------------------------------------|
"""
    
    for rtype, count in stats.items():
        readme_content += f"| `{rtype}` | {count} | Ver documentação de assets | \n"
    
    readme_content += """
---

## 🔧 PROPRIEDADES DOS DADOS (Atributos)

Cada objeto possui as seguintes propriedades úteis:
1. **`game_layer`**: Categoria lógica (ex: `Infrastructure_Irrigation`).
2. **`asset_class`**: Sugestão de nome de asset (ex: `BP_PivotSystem`).
3. **`anim_loop`**: Se existir, indica animação necessária (ex: `rotate_slow`).
4. **`collision`**: Booleano (True/False) indicando se deve gerar colisor.

---
**Gerado automaticamente pelo Pipeline de Execução Digital Twin v1.0**
"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README gerado em: {readme_path}")
    print("💎 PROCESSO CONCLUÍDO! O Digital Twin está pronto.")

if __name__ == "__main__":
    export_final()
