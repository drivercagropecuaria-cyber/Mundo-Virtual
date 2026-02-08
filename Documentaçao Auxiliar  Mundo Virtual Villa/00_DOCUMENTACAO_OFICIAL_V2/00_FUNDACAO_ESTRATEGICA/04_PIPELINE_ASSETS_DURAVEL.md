# 🔄 PIPELINE DE ASSETS DURÁVEL
## Da Produção ao Runtime: Preservação de Conteúdo 3D

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Pipeline de Produção Obrigatório

---

## 🎯 FILOSOFIA DO PIPELINE

> *"Um asset durável é aquele que pode ser editado daqui a 20 anos, exportado para qualquer engine, e ainda será compreensível."*

**Princípios:**
1. **Fonte Aberta:** Formatos de produção editáveis e documentados
2. **Exportação Garantida:** Caminho claro para padrões abertos
3. **Compressão Inteligente:** Otimizado sem perda de qualidade
4. **Versionamento Total:** Cada asset tem histórico completo
5. **Metadados Ricos:** Informação contextual preservada

---

## 📊 VISÃO GERAL DO PIPELINE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE ASSETS DURÁVEL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CAPTURA              PRODUÇÃO              PROCESSAMENTO         ENTREGA  │
│  ┌────────┐          ┌────────┐            ┌──────────────┐      ┌────────┐ │
│  │ FONTE  │─────────▶│ MASTER │───────────▶│   BUILD      │─────▶│ RUNTIME│ │
│  │        │          │        │            │              │      │        │ │
│  └────────┘          └────────┘            └──────────────┘      └────────┘ │
│       │                  │                       │                    │      │
│       ▼                  ▼                       ▼                    ▼      │
│  ┌────────────┐    ┌────────────┐        ┌────────────┐      ┌────────────┐│
│  │Fotos       │    │OpenUSD     │        │glTF        │      │CDN         ││
│  │Laser Scan  │    │Blender     │        │Draco       │      │HTTP/3      ││
│  │Modelagem   │    │Houdini     │        │KTX2        │      │Edge Cache  ││
│  │Procedural  │    │            │        │Basis Univ. │      │            ││
│  └────────────┘    └────────────┘        └────────────┘      └────────────┘│
│                                                                             │
│  CARACTERÍSTICAS:                                                          │
│  • Editável forever    • Versionável      • Otimizado    • Cache-friendly │
│  • Documentado         • Exportável       • Interoperável • Fast delivery │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
assets/
├── source/                    # FORMATO FONTE (editável)
│   ├── usd/                   # OpenUSD master files
│   │   ├── villa_canabrava.usd
│   │   ├── sede/
│   │   │   ├── sede_principal.usd
│   │   │   ├── interior/
│   │   │   └── exterior/
│   │   ├── pivos/
│   │   ├── mata/
│   │   └── infraestrutura/
│   │
│   ├── blender/               # Arquivos .blend (alternativa)
│   │   └── (backup only)
│   │
│   ├── textures/              # TEXTURAS FONTE
│   │   ├── raw/               # Scans originais
│   │   │   ├── sede_photos/
│   │   │   └── pivo_photos/
│   │   └── processed/         # PBR processado
│   │       ├── baseColor/
│   │       ├── normal/
│   │       ├── metallic/
│   │       ├── roughness/
│   │       └── ao/
│   │
│   ├── photogrammetry/        # FOTOGRAMETRIA
│   │   ├── realitycapture/
│   │   └── metashape/
│   │
│   └── references/            # REFERÊNCIAS
│       ├── fotos/
│       ├── plantas/
│       └── documentacao/
│
├── intermediate/              # FORMATO INTERMEDIÁRIO
│   ├── gltf/                  # glTF 2.0 (pré-otimização)
│   │   ├── sede.gltf
│   │   └── sede.bin
│   │
│   ├── unoptimized/           # glTF sem compressão
│   └── lod/                   # Níveis de detalhe
│       ├── sede_lod0.gltf     # Alto detalhe (próximo)
│       ├── sede_lod1.gltf     # Médio detalhe
│       └── sede_lod2.gltf     # Baixo detalhe (distante)
│
├── runtime/                   # FORMATO RUNTIME (otimizado)
│   ├── gltf/                  # glTF + Draco + KTX2
│   │   ├── sede.glb
│   │   ├── sede_lod0.glb
│   │   ├── sede_lod1.glb
│   │   └── sede_lod2.glb
│   │
│   ├── chunks/                # Chunked para streaming
│   │   └── sede/
│   │       ├── chunk_0_0.glb
│   │       ├── chunk_0_1.glb
│   │       └── ...
│   │
│   └── 3dtiles/               # OGC 3D Tiles
│       └── tileset.json
│
└── archive/                   # ARQUIVO HISTÓRICO
    ├── v1.0.0/                # Versão 1.0.0
    ├── v1.1.0/                # Versão 1.1.0
    └── ...
```

---

## 🏗️ ETAPA 1: CAPTURA

### 1.1 Fotogrametria

**Ferramenta:** RealityCapture / Metashape  
**Saída:** Nuvem de pontos + malha + texturas

```bash
# Pipeline RealityCapture
realitycapture.exe \
    -addFolder "./fotos/sede/" \
    -align \
    -calculateNormalModel \
    -calculateTexture \
    -save "./source/photogrammetry/sede.rcproj" \
    -exportModel "./source/usd/sede/sede_photogrammetry.usd" "usd"
```

**Especificações de Captura:**

| Aspecto | Especificação |
|---------|---------------|
| Resolução de foto | Mínimo 20MP |
| Sobreposição | 80% frontal, 60% lateral |
| Iluminação | Difusa (nublado ou sombra) |
| Referências | Targets de escala |
| GPS | RTK quando possível |

### 1.2 Laser Scanning (LiDAR)

**Ferramenta:** FARO Focus / Leica BLK  
**Saída:** Nuvem de pontos de alta precisão

```bash
# Registro de scans
scene.exe \
    --import "scan_001.e57" \
    --import "scan_002.e57" \
    --register \
    --export "./source/photogrammetry/sede_lidar.e57"
```

### 1.3 Modelagem Manual

**Ferramenta:** Blender / Houdini / Maya (com export USD)  
**Saída:** OpenUSD ou .blend

**Requisitos:**
- UVs bem organizados
- Nomenclatura consistente
- Escala 1:1 (metros)
- Origem no centro geométrico

---

## 🎨 ETAPA 2: PRODUÇÃO (MASTER)

### 2.1 OpenUSD como Formato Master

**Por que OpenUSD?**
- ✅ Editável em múltiplas ferramentas
- ✅ Composição de cenas complexas
- ✅ Referências (não duplicação)
- ✅ Variantes (LOD, season, etc.)
- ✅ Versionamento nativo

**Estrutura de Camada USD:**

```python
# villa_canabrava.usd - Root layer
#version 0.8

def "VillaCanabrava" (
    doc = "Universo Virtual Villa Canabrava"
)
{
    def Xform "Geography" (
        doc = "Dados geoespaciais de referência"
    )
    {
        double3 xformOp:translate = (-43.947776, -17.385117, 850)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
    
    def Xform "Sede_VillaTerezinha" (
        doc = "Sede principal da fazenda"
        references = @./sede/sede.usd@</Sede>
    )
    {
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
    
    def Xform "Pivos" (
        doc = "Sistemas de irrigação"
    )
    {
        def Xform "Pivo_01" (
            references = @./pivos/pivo_01.usd@</Pivo>
        )
        {
            double3 xformOp:translate = (-1000, 500, 0)
        }
        
        # ... mais pivôs
    }
    
    def Xform "Mata_Nativa" (
        doc = "Vegetação nativa preservada"
        references = @./mata/mata_combined.usd@</Mata>
    )
    {
        # Referência para toda a mata
    }
    
    def Xform "Infraestrutura" (
        doc = "Estradas, cercas, postes"
    )
    {
        # Subcamadas
    }
}
```

### 2.2 Sistema de Variantes (LOD)

```python
# sede.usd com variantes de LOD

def "Sede" (
    doc = "Sede Villa Terezinha com LODs"
)
{
    variantSet "lod" = {
        "lod0" (
            doc = "Alto detalhe - uso próximo"
            references = @./sede_lod0.usd@
        )
        "lod1" (
            doc = "Médio detalhe - uso médio"
            references = @./sede_lod1.usd@
        )
        "lod2" (
            doc = "Baixo detalhe - uso distante"
            references = @./sede_lod2.usd@
        )
    }
    
    # Variante padrão
    variantSet "season" = {
        "dry" (
            doc = "Estação seca"
            references = @./sede_dry.usd@
        )
        "wet" (
            doc = "Estação chuvosa"
            references = @./sede_wet.usd@
        )
    }
}
```

### 2.3 Texturização PBR

**Workflow:**
1. **Base Color** (sRGB) - Cor difusa
2. **Normal** (Linear) - Detalhes de superfície
3. **Metallic** (Linear) - 0=dielétrico, 1=metálico
4. **Roughness** (Linear) - 0=espelho, 1=diffuso
5. **AO** (Linear) - Oclusão ambiente
6. **Emissive** (sRGB, opcional) - Luz própria

**Formato de Exportação:** KTX2 + Basis Universal

```bash
# Converter texturas para KTX2
ktx create \
    --format R8G8B8_SRGB \
    --encode uastc \
    --uastc-quality 2 \
    --zstd 18 \
    ./textures/raw/sede_baseColor.png \
    ./source/textures/processed/sede_baseColor.ktx2
```

---

## ⚙️ ETAPA 3: PROCESSAMENTO (BUILD)

### 3.1 Pipeline de Build Automatizado

```yaml
# asset-pipeline.yaml
pipeline:
  name: villa_canabrava_assets
  version: 1.0.0

stages:
  # Stage 1: Validação
  - name: validate
    script: |
      usdval ./source/usd/villa_canabrava.usd
      check_textures ./source/textures/
    
  # Stage 2: Export glTF
  - name: export_gltf
    script: |
      usd2gltf \
        --input ./source/usd/villa_canabrava.usd \
        --output ./intermediate/gltf/ \
        --embed-textures false \
        --separate-meshes true
        
  # Stage 3: Gerar LODs
  - name: generate_lods
    script: |
      for model in ./intermediate/gltf/*.gltf; do
        gltf-lod-generator \
          --input $model \
          --output ./intermediate/lod/ \
          --ratios 0.5,0.25,0.1 \
          --distances 50,150,500
      done
      
  # Stage 4: Compressão
  - name: compress
    script: |
      # Draco para geometria
      gltf-pipeline \
        --input ./intermediate/gltf/sede.gltf \
        --output ./runtime/gltf/sede.glb \
        --draco.compressionLevel 7 \
        --draco.quantizePositionBits 14 \
        --draco.quantizeNormalBits 10 \
        --draco.quantizeTexcoordBits 12
        
      # KTX2 para texturas
      for tex in ./intermediate/gltf/textures/*; do
        ktx create \
          --encode basis-lz \
          --zstd 18 \
          $tex \
          ./runtime/gltf/textures/$(basename $tex .png).ktx2
      done
      
  # Stage 5: Chunking (para streaming)
  - name: chunk
    script: |
      gltf-chunker \
        --input ./runtime/gltf/sede.glb \
        --output ./runtime/chunks/sede/ \
        --chunk-size 100x100 \
        --overlap 10
        
  # Stage 6: 3D Tiles (geoespacial)
  - name: 3dtiles
    script: |
      gltf-to-3d-tiles \
        --input ./runtime/gltf/ \
        --output ./runtime/3dtiles/ \
        --geometric-error 100,50,20,5 \
        --region "-44.0,-17.4,-43.9,-17.35,800,1000"
        
  # Stage 7: Validação final
  - name: validate_runtime
    script: |
      gltf-validator ./runtime/gltf/*.glb
      check_ktx2 ./runtime/gltf/textures/
      
  # Stage 8: Publicação
  - name: publish
    script: |
      aws s3 sync ./runtime/ s3://villa-canabrava-assets/production/ \
        --cache-control "max-age=31536000,immutable"
```

### 3.2 Compressão Draco

```javascript
// Configuração de compressão Draco
const dracoOptions = {
  compressionLevel: 7,        // 0-10 (10 = máxima compressão)
  quantizePositionBits: 14,   // Precisão de posição
  quantizeNormalBits: 10,     // Precisão de normal
  quantizeTexcoordBits: 12,   // Precisão de UV
  quantizeColorBits: 8,       // Precisão de cor
  quantizeGenericBits: 12     // Precisão de atributos genéricos
};

// Aplicação via gltf-pipeline
const gltfPipeline = require('gltf-pipeline');
const fs = require('fs');

const gltf = fs.readFileSync('./intermediate/sede.gltf');

const options = {
  dracoOptions: dracoOptions,
  resourceDirectory: './intermediate/textures/'
};

gltfPipeline.gltfToGlb(gltf, options)
  .then(result => {
    fs.writeFileSync('./runtime/sede.glb', result.glb);
  });
```

### 3.3 Compressão de Texturas (KTX2 + Basis Universal)

```bash
#!/bin/bash
# compress_textures.sh

INPUT_DIR="./intermediate/textures"
OUTPUT_DIR="./runtime/textures"

for file in "$INPUT_DIR"/*.png; do
    filename=$(basename "$file" .png)
    
    # Detectar tipo de textura pelo sufixo
    if [[ $filename == *_baseColor* ]] || [[ $filename == *_emissive* ]]; then
        # sRGB para cores
        ktx create \
            --format R8G8B8A8_SRGB \
            --encode uastc \
            --uastc-quality 2 \
            --zstd 18 \
            "$file" \
            "$OUTPUT_DIR/${filename}.ktx2"
    else
        # Linear para dados (normal, metallic, roughness, AO)
        ktx create \
            --format R8G8B8A8_UNORM \
            --encode uastc \
            --uastc-quality 1 \
            --zstd 18 \
            "$file" \
            "$OUTPUT_DIR/${filename}.ktx2"
    fi
done
```

---

## 🚀 ETAPA 4: ENTREGA (RUNTIME)

### 4.1 Estrutura de Assets Runtime

```
runtime/
├── manifest.json              # Manifesto de assets
├── sede/
│   ├── manifest.json          # Manifesto do asset
│   ├── sede.glb               # Asset principal
│   ├── sede_lod0.glb          # LOD 0
│   ├── sede_lod1.glb          # LOD 1
│   ├── sede_lod2.glb          # LOD 2
│   └── textures/
│       ├── sede_baseColor.ktx2
│       ├── sede_normal.ktx2
│       ├── sede_metallicRoughness.ktx2
│       └── sede_ao.ktx2
├── pivos/
│   └── ...
└── chunks/
    └── sede/
        ├── manifest.json
        ├── chunk_0_0.glb
        ├── chunk_0_1.glb
        └── ...
```

### 4.2 Manifesto de Asset

```json
{
  "asset_id": "sede_villa_terezinha",
  "version": "1.2.3",
  "created_at": "2026-02-06T00:00:00Z",
  "format": "glTF 2.0",
  "extensions": ["KHR_draco_mesh_compression", "KHR_texture_basisu"],
  
  "variants": {
    "default": {
      "uri": "sede.glb",
      "size_bytes": 5242880,
      "checksum": "sha256:abc123..."
    },
    "lod0": {
      "uri": "sede_lod0.glb",
      "size_bytes": 10485760,
      "geometric_error": 0.0,
      "screen_space_error": 0.0
    },
    "lod1": {
      "uri": "sede_lod1.glb",
      "size_bytes": 2621440,
      "geometric_error": 10.0,
      "screen_space_error": 2.0
    },
    "lod2": {
      "uri": "sede_lod2.glb",
      "size_bytes": 655360,
      "geometric_error": 50.0,
      "screen_space_error": 8.0
    }
  },
  
  "bounding_box": {
    "min": [-50, 0, -30],
    "max": [50, 25, 30]
  },
  
  "georeference": {
    "crs": "EPSG:4326",
    "centroid": [-43.947776, -17.385117, 850]
  },
  
  "dependencies": {
    "textures": [
      "textures/sede_baseColor.ktx2",
      "textures/sede_normal.ktx2"
    ]
  },
  
  "metadata": {
    "name": {
      "pt": "Sede Villa Terezinha",
      "en": "Villa Terezinha Headquarters"
    },
    "description": {
      "pt": "Sede principal da Fazenda Villa Canabrava",
      "en": "Main headquarters of Villa Canabrava Farm"
    },
    "tags": ["sede", "arquitetura", "historia"],
    "created_by": "pipeline@v1.0.0",
    "source_reference": "usd://source/sede/sede.usd"
  }
}
```

### 4.3 CDN e Cache

```javascript
// Configuração de CDN
const cdnConfig = {
  baseUrl: 'https://assets.villacanabrava.world',
  
  // Headers de cache
  cacheControl: {
    // Assets versionados: cache forever
    versioned: 'public, max-age=31536000, immutable',
    // Manifestos: cache curto
    manifest: 'public, max-age=60, stale-while-revalidate=300',
    // Índices: cache médio
    index: 'public, max-age=3600'
  },
  
  // Compressão
  compression: {
    brotli: true,
    gzip: true
  },
  
  // HTTP/3
  http3: true
};

// Carregamento de asset com LOD
async function loadAsset(assetId, cameraDistance) {
  // Determinar LOD baseado na distância
  const lod = selectLOD(cameraDistance);
  
  // Construir URL
  const url = `${cdnConfig.baseUrl}/${assetId}/${assetId}_${lod}.glb`;
  
  // Carregar com cache
  const response = await fetch(url, {
    headers: {
      'Accept': 'model/gltf-binary, application/octet-stream'
    }
  });
  
  const arrayBuffer = await response.arrayBuffer();
  
  // Parse glTF
  const gltf = await parseGLB(arrayBuffer);
  
  return gltf;
}

function selectLOD(distance) {
  if (distance < 50) return 'lod0';
  if (distance < 150) return 'lod1';
  return 'lod2';
}
```

---

## 📊 MÉTRICAS DE QUALIDADE

### Métricas por Asset

| Métrica | Target | Máximo |
|---------|--------|--------|
| Tamanho LOD0 | < 10 MB | 20 MB |
| Tamanho LOD1 | < 3 MB | 5 MB |
| Tamanho LOD2 | < 1 MB | 2 MB |
| Draw calls | < 100 | 200 |
| Triângulos LOD0 | < 500k | 1M |
| Triângulos LOD1 | < 100k | 200k |
| Triângulos LOD2 | < 20k | 50k |
| Texturas | < 10 | 20 |
| Resolução máxima | 4K | 8K |

### Compressão

| Tipo | Taxa de Compressão | Qualidade |
|------|-------------------|-----------|
| Draco | 5-20x | Lossy controlado |
| KTX2/Basis | 4-8x | Lossy perceptual |
| Zstd | 2-5x | Lossless |

---

**FIM DO PIPELINE DE ASSETS**
