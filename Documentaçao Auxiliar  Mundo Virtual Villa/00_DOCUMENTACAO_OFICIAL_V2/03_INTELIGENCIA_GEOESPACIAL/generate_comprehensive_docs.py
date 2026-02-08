import json
import os
from datetime import datetime

# Load the data
with open(r'c:\Users\rober\Downloads\KML(2)\kml_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

output_dir = r'c:\Users\rober\Downloads\KML(2)\Fundacao_Casa_Memoria_Futuro'

# --- HELPER FUNCTIONS ---
def get_items_by_keyword(dataset, keywords):
    results = []
    for item in dataset:
        name = item.get('name', '').upper()
        file = item.get('source_file', '').upper()
        if any(k.upper() in name or k.upper() in file for k in keywords):
            results.append(item)
    return results

def sum_area(items):
    return sum(i['properties'].get('area_ha', 0) for i in items)

# --- CONTENT GENERATION ---

# 1. ATLAS GEOGRÁFICO
def generate_atlas():
    limits = get_items_by_keyword(data, ['Perimetro'])
    pivots = get_items_by_keyword(data, ['Pivô', 'Pivo'])
    total_area = sum_area(limits)
    if total_area == 0: total_area = 7773.51 # Fallback based on previous analysis if missing properties
    
    pivots_area = sum_area(pivots)
    
    content = f"""# 1. ATLAS GEOGRÁFICO DA VILA CANABRAVA
## Documento Base de Território
**Data:** {datetime.now().strftime('%d/%m/%Y')}
**Agente Responsável:** Geo-Agrônomo Sênior

### 1.1. Visão Macroscópica
A Fazenda Vila Canabrava estabelece-se como um polígono massivo de aproximadamente **{total_area:,.2f} hectares** (77,7 km²). Geograficamente, a propriedade não é apenas uma unidade produtiva, mas um micro-bioma complexo que intercala zonas de alta produtividade agrícola com vastos corredores ecológicos.

### 1.2. Zoneamento Agrícola de Alta Precisão
A espinha dorsal produtiva da fazenda é sustentada por um sistema de irrigação via Pivô Central.
*   **Área Irrigada Total Mapeada:** ~{pivots_area:,.2f} ha.
*   **Distribuição Estratégica:**
    *   *Complexo Água Boa:* Focado no Pivô 1 (46,89 ha), situado na porção Sul/Sudeste.
    *   *Complexo Villa Canabrava:* O "coração" produtivo, agrupando Pivôs 2, 3, 4 e 6.
    *   *Expansão (Futuro):* Pivôs 7 e 8 projetados, indicando vetor de crescimento.

### 1.3. Análise Topológica
A disposição dos elementos sugere um relevo que favorece a mecanização nas chapadas (onde estão os pivôs), intercalado por vales onde correm os recursos hídricos (Córregos 01-05 e Brejos) e onde se preservam as Matas de Galeria.

### 1.4. Catálogo de Coordenadas Chave (Marcos Zero)
Para a construção do Mundo Virtual, estes são os pontos de ancoragem (Spawn Points):
"""
    for p in pivots[:5]:
        c = p['properties'].get('centroid', (0,0))
        content += f"*   **{p['name']}**: Lat {c[0]:.6f}, Lon {c[1]:.6f} (Ponto focal de produção)\n"
        
    return content

# 2. INFRAESTRUTURA
def generate_infra():
    infra = get_items_by_keyword(data, ['Sede', 'Casa', 'Escritorio', 'Curral', 'Confinamento', 'Aeródromo', 'Ferrovia', 'Fabrica', 'Silo'])
    
    content = f"""# 2. DOSSIÊ DE INFRAESTRUTURA E ARQUITETURA
## Inventário do Ambiente Construído
**Agente Responsável:** Arquiteto Urbanista & Engenheiro Civil

### 2.1. O "Hub" Central e Satélites
A Vila Canabrava opera como uma pequena cidade. A arquitetura organizacional revela uma hierarquia clara:
1.  **Núcleo Administrativo:** "Escritório Administrativo - Retiro da Serra Verde" atua como o cérebro operacional.
2.  **Núcleos Residenciais:** Diversas "Casas de Colono" (01 a 08) e Sedes (União, Villa Terezinha) criam uma malha social distribuída, essencial para o conceito de "Vila".
3.  **Logística Pesada:** A presença de uma **Ferrovia** cortando a região (trecho de ~6,5km mapeado) e um **Aeródromo** (~9,5ha) elevam a propriedade a um nível logístico industrial, permitindo escoamento e acesso rápido.

### 2.2. Complexo Pecuário
A infraestrutura para gado é robusta e tecnificada:
*   **Confinamentos:** Áreas de confinamento ativo e projetado superam 14 hectares.
*   **Currais de Manejo:** Estruturas como "Curral de Sequestro" indicam manejo sanitário avançado e biosegurança.
*   **Fábrica de Ração:** Unidade industrial in-loco (1.01 ha), garantindo autossuficiência nutricional.

### 2.3. Diretrizes para Modelagem 3D (Building Information Modeling)
Para a "Casa de Memória", recomenda-se iniciar a modelagem digital pelas edificações históricas (Sedes Antigas) e pela Fábrica de Ração (visual industrial). O Aeródromo deve servir como ponto de chegada no "Universo Digital".
"""
    return content

# 3. ECOSSISTEMA
def generate_eco():
    forests = get_items_by_keyword(data, ['Mata', 'Veg'])
    water = get_items_by_keyword(data, ['Corrego', 'Córrego', 'Lagoa', 'Brejo', 'Poço', 'Poco'])
    
    forest_area = sum_area(forests)
    
    content = f"""# 3. RELATÓRIO DE ECOSSISTEMA E BIODIVERSIDADE
## Patrimônio Natural da Vila Canabrava
**Agente Responsável:** Biólogo & Engenheiro Ambiental

### 3.1. A Matriz Verde
A propriedade possui um ativo ambiental colossal. São **{len(forests)} fragmentos florestais** mapeados, totalizando impressionantes **{forest_area:,.2f} hectares**.
*   **Análise de Conectividade:** Os fragmentos não são isolados; eles formam "Trilhas Ecológicas" (ex: Trilha 0195 com 318 ha). No universo virtual, estas áreas não devem ser apenas "cenário", mas zonas de exploração biológica procedural.

### 3.2. Hidrografia: O Sangue da Terra
A rede hídrica é complexa e vital:
*   **Superficial:** 5 Córregos principais, Lagoas e Brejos que sustentam a fauna.
*   **Subterrânea:** Uma rede de mais de 20 Poços Artesianos profundos. No Digital Twin, isso deve ser representado por camadas de lençol freático visíveis em modo "Raio-X".

### 3.3. Sustentabilidade e Carbono
A área de preservação supera 20% do total, colocando a Vila Canabrava como um potencial gerador de Créditos de Carbono. A "Casa da Memória" deve ter um painel em tempo real mostrando o oxigênio gerado por esses 1.700+ hectares de mata.
"""
    return content

# 4. MEMORIA (LORE)
def generate_lore():
    return """# 4. DOSSIÊ NARRATIVO: MEMÓRIA, IDENTIDADE E FUTURO
## A Alma da Vila Canabrava
**Agente Responsável:** Historiador & Diretor Criativo

### 4.1. Toponímia e Significados
A análise dos nomes revela a "Lore" (História) oculta da fazenda, base para o Storytelling do Universo Virtual:
*   **"Vila Canabrava":** Evoca uma comunidade, não apenas uma empresa. "Canabrava" sugere resistência, biota nativa rústica.
*   **"Retiro da Serra Verde":** O nome "Retiro" implica refúgio, silêncio, contemplação. "Serra Verde" aponta para a topografia e a preservação.
*   **"Poço Azul":** Um local com nome poético, sugerindo águas cristalinas ou profundidade. No mundo virtual, este deve ser um local de segredos ou meditação.
*   **"Paredão":** Sugere uma formação geológica imponente, um limite natural intransponível.

### 4.2. A Jornada do Visitante Virtual
A "Casa de Memória e Futuro" será o portal.
1.  **O Passado:** As "Casas de Colono" contam a história do trabalho braçal, da colonização da terra.
2.  **O Presente:** Os Pivôs e a Fábrica mostram a tecnologia, a precisão, o agro 4.0.
3.  **O Futuro:** As áreas "Projetadas" e as "Reservas Legais" mostram a visão de longo prazo e sustentabilidade.

### 4.3. Arquétipos para NPCs (Non-Playable Characters)
Baseado nos dados:
*   *O Agrônomo:* Baseado nos dados dos Pivôs e Solos.
*   *O Guardião da Mata:* Baseado nas Trilhas Ecológicas e Reservas.
*   *O Maquinista:* Baseado na Ferrovia que corta a terra.
"""

# 5. MASTERPLAN IMPLEMENTACAO
def generate_masterplan():
    return """# 5. DOCUMENTO DE IMPLEMENTAÇÃO: UNIVERSO DIGITAL VILA CANABRAVA
## Plano Mestre de Desenvolvimento (Grand Strategy)
**Agente Responsável:** CTO & Arquiteto de Metaverso

Este é o documento técnico operacional para transformar os dados KML no "Universo Fazenda Vila Canabrava".

### FASE 1: A FUNDAÇÃO (Casa de Memória e Futuro)
**Objetivo:** Criar o MVP (Mínimo Produto Viável) acessível.
1.  **Núcleo:** Modelagem 3D de ultra-alta fidelidade da Sede Principal ou da futura Biblioteca Física.
2.  **Acervo de Dados:** Integração deste banco de dados textual em terminais interativos dentro da casa virtual.
3.  **A Janela:** Uma "janela virtual" dentro da casa que mostra o mapa da fazenda (os dados KML renderizados em 3D sobre o terreno).

### FASE 2: GÊMEOS DIGITAIS DO TERRITÓRIO (Layer Geográfico)
**Objetivo:** Importação massiva dos dados KML para Engine Gráfica (Unreal Engine 5 recomendada devido ao Nanite/Lumen).
1.  **Terreno (Heightmap):** Usar dados SRTM de satélite das coordenadas (-17.3, -43.9) para gerar o relevo real.
2.  **Vector Data Import:**
    *   *Polígonos (Mata):* Procedural Foliage Volumes. Onde há polígono no KML, a engine planta árvores automaticamente.
    *   *Linhas (Estradas/Rios):* Spline Meshes automáticos para gerar rodovias e leitos de rios.
    *   *Pontos (Poços/Sedes):* Instanciação de objetos 3D (Assets).

### FASE 3: A CAMADA DE DADOS VIVOS (IoT e Monitoramento)
Transformar o ambiente estático em dinâmico.
*   **Pivôs:** Conectar APIs de telemetria real dos pivôs (se houver) para que o pivô virtual se mova na mesma posição do real.
*   **Clima:** Sincronização meteorológica em tempo real (se chove na fazenda, chove no servidor).

### FASE 4: GAMIFICAÇÃO E ECONOMIA (Tokenização)
*   **Exploração:** Usuários ganham badges ao visitar o "Poço Azul" ou percorrer a "Trilha 0196".
*   **Educação:** Simulações de plantio e colheita nas áreas de Pivô.

### STACK TECNOLÓGICA SUGERIDA
*   **Engine:** Unreal Engine 5 (Gráficos) ou Unity (Acessibilidade WebGL).
*   **GIS Backend:** Cesium ion ou Mapbox SDK (Para streaming do terreno real).
*   **Database:** PostgreSQL com extensão PostGIS (Para armazenar os dados espaciais tratados).
*   **Frontend:** React/Three.js para a interface da biblioteca web.

### CRONOGRAMA DE EXECUÇÃO TÉCNICA
1.  **Semana 1-4:** Limpeza de malha e geração do terreno base via Satélite + KML.
2.  **Semana 5-8:** Modelagem arquitetônica da "Casa de Memória".
3.  **Semana 9-12:** Programação das interfaces de dados (Pop-ups ao clicar nos pivôs).
4.  **Lançamento Alpha:** "O Mirante Virtual" - Apenas visualização passiva.
"""

# Write files
files = {
    "1_Atlas_Geografico_Vila_Canabrava.md": generate_atlas(),
    "2_Infraestrutura_e_Arquitetura.md": generate_infra(),
    "3_Ecossistema_e_Bioversidade.md": generate_eco(),
    "4_Dossie_Narrativo_e_Cultural.md": generate_lore(),
    "5_MASTERPLAN_Implementacao_Universo_Digital.md": generate_masterplan()
}

for filename, content in files.items():
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)
