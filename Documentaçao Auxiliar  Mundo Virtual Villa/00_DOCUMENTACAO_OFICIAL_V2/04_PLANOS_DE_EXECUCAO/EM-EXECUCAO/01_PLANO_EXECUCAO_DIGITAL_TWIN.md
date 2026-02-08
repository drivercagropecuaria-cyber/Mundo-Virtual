# 🛠️ PLANO DE EXECUÇÃO TÁTICA 001: GENESE DO DIGITAL TWIN
## Estruturação Geoespacial e Pipeline de Dados

**Versão:** 1.0
**Alvo:** Objetivo Primário (Digital Twin / Gêmeo Digital)
**Status:** 🚀 PRONTO PARA INÍCIO
**Arquitetura:** Python (ETL) -> GeoJSON (Intercâmbio) -> Game Engine (Consumo)

---

## 🧠 1.0 INTELIGÊNCIA DE DADOS E VISÃO AMPLIADA

Para atingir o objetivo de um "Digital Twin" que não seja apenas um desenho 3D vazio, mas um **banco de dados espacial vivo**, nossa execução seguirá a lógica de **Enriquecimento Semântico**.

**O que isso significa na prática?**
Não vamos apenas converter "linhas" e "pontos". Vamos converter **significados**.
*   **Antes (KML):** Uma linha amarela sem nome.
*   **Depois (Digital Twin):** Objeto do tipo `Infrastructure.Fence`, Subtipo `BarbedWire`, Estado `Preserved`, Extensão `1540m`, Coordenadas XYZ.

---

## 📋 2.0 CHECKLIST DO USUÁRIO (SUAS AÇÕES IMEDIATAS)

Para que eu (o Agente) possa executar os scripts de processamento, preciso que você garanta o ambiente base.

### 2.1 Instalação de Ferramentas Essenciais
*   [ ] **Python 3.10+**: Certifique-se de que está instalado no Windows e adicionado ao PATH.
    *   *Teste:* Abra o terminal e digite `python --version`.
*   [ ] **QGIS (Opcional mas Recomendado):** Para você visualizar os dados geográficos "crus" e validar meu trabalho visualmente.
    *   *Download:* [QGIS Website](https://qgis.org/en/site/forusers/download.html)
*   [ ] **VS Code Extensions:**
    *   Instale a extensão **Generate Data** (Se quiser ver prévias de dados).
    *   Instale a extensão **Geo Data Viewer** (Para ver GeoJSON direto no VS Code).

### 2.2 Conexões e Chaves (Access Tokens)
*   [ ] **Mapbox (Opcional para MVP, Obrigatório para Fase 2):** Se formos usar mapas de fundo online no futuro. Crie uma conta gratuita em [mapbox.com](https://mapbox.com) e guarde a chave pública.
*   [ ] **Google Earth Pro:** Mantenha instalado para tirar dúvidas de comparação se necessário.

---

## ⚙️ 3.0 O PLANO DE ATAQUE (MINHAS AÇÕES DE EXECUÇÃO)

Eu irei criar e executar scripts Python dedicados para cada etapa abaixo. Você só precisa autorizar a execução.

### ETAPA 1: O "Grande Filtro" (Data Ingestion & Cleaning)
*   **Ação:** Criar script `01_ingest_kml.py`.
*   **O que faz:**
    1.  Lê recursivamente todos os 252 arquivos KML na pasta `03_INTELIGENCIA_GEOESPACIAL`.
    2.  Separa o que é 2D (áreas) do que é 3D (elevação).
    3.  **Correção Automática:** Fecha polígonos abertos, remove vértices duplicados (cleaning).
    4.  **Padronização:** Converte tudo para o sistema de coordenadas WGS84 (EPSG:4326).

### ETAPA 2: Validação Matemática (Topology Check)
*   **Ação:** Criar script `02_validate_topology.py`.
*   **O que faz:**
    1.  Verifica se polígonos de mata se sobrepõem a estruturas.
    2.  Calcula a área total matemática e compara com documentação (7.729 ha).
    3.  Gera um relatório de **Discrepâncias Críticas** (ex: "A área da Mata X invade a Estrada Y em 5 metros").

### ETAPA 3: Enriquecimento Semântico (Semantic Tagging)
*   **Ação:** Criar script `03_enrich_data.py`.
*   **O que faz:**
    1.  Adiciona metadados de *Game Design* aos dados brutos.
    2.  Exemplo: Se o dado é "Pivô Central", adiciona tags `{ "render_type": "blueprint_actor", "anim_loop": "rotate_slow" }`.
    3.  Prepara o arquivo para ser lido pela Unity/Unreal sem configuração manual.

### ETAPA 4: Exportação Final (The Golden Source)
*   **Ação:** Gerar o arquivo mestre `VILLA_CANABRAVA_DIGITAL_TWIN_V1.geojson`.
*   **Resultado:** Um único arquivo (ou conjunto particionado) contendo TODO o universo, leve, limpo e pronto para importação.

---

## 🛠️ 4.0 FERRAMENTAS E BIBLIOTECAS QUE USAREI
Para executar isso, usarei as seguintes libs Python (precisaremos instalar via pip):

```bash
pip install geopandas shapely fiona matplotlib unidecode Rtree
```

*   **GeoPandas:** O "Excel" dos dados geográficos.
*   **Shapely:** A geometria pura (cálculos matemáticos).
*   **Fiona:** Leitura e escrita de arquivos GIS.
*   **Rtree:** Índice espacial para buscas ultra-rápidas.

---

## 🚦 5.0 PRÓXIMO PASSO (ACTION REQUEST)

Para darmos o *start* na **ETAPA 1 (O Grande Filtro)**, valide se você tem o Python instalado. Se sim, me autorize a:

1.  Criar o ambiente virtual Python (`myenv`).
2.  Instalar as dependências listadas acima.
3.  Escrever e rodar o script de ingestão.
