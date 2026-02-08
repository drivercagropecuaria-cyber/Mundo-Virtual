# 📋 PADRÕES E PROTOCOLOS
## Especificação Técnica de Standards Adotados

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Obrigatório para Conformidade Atemporal

---

## 🎯 SUMÁRIO EXECUTIVO

Este documento especifica **todos os padrões abertos obrigatórios** para o Universo Virtual Villa Canabrava. A adoção rigorosa destes padrões garante a atemporalidade, interoperabilidade e preservação do mundo virtual.

**Regra Fundamental:** *Nenhuma tecnologia proprietária pode ser adotada se não houver caminho de exportação para um padrão aberto equivalente.*

---

## 📊 MATRIZ DE PADRÕES

| Categoria | Padrão | Versão | Status | RFC/Especificação |
|-----------|--------|--------|--------|-------------------|
| **XR Nativo** | OpenXR | 1.0+ | Obrigatório | Khronos Group |
| **XR Web** | WebXR | 2023 | Obrigatório | W3C |
| **Render Web** | WebGPU | 2024 | Obrigatório | W3C |
| **Assets Runtime** | glTF | 2.0 | Obrigatório | ISO/IEC 12113:2022 |
| **Cenas/Produção** | OpenUSD | 23.08+ | Obrigatório | AOUSD/Pixar |
| **Transporte** | QUIC | RFC 9000 | Obrigatório | IETF |
| **HTTP Moderno** | HTTP/3 | RFC 9114 | Obrigatório | IETF |
| **Geoespacial** | OGC 3D Tiles | 1.1 | Obrigatório | OGC |
| **Geoespacial** | GeoJSON | RFC 7946 | Obrigatório | IETF |
| **Identidade** | OpenID Connect | 1.0 | Obrigatório | OpenID Foundation |
| **Autenticação** | WebAuthn | Level 2 | Recomendado | W3C/FIDO |
| **Tokens** | JWT | RFC 7519 | Obrigatório | IETF |
| **APIs** | OpenAPI | 3.1.0 | Obrigatório | OpenAPI Initiative |
| **GraphQL** | GraphQL Spec | Oct2021 | Opcional | GraphQL Foundation |
| **gRPC** | Protocol Buffers | proto3 | Obrigatório | Google/Cloud Native |
| **JSON** | JSON | RFC 8259 | Obrigatório | IETF |
| **JSON-LD** | JSON-LD | 1.1 | Recomendado | W3C |
| **Semântica** | Schema.org | Latest | Recomendado | Schema.org |
| **Compressão** | Zstd | 1.5+ | Obrigatório | Facebook/Meta |
| **Compressão** | Brotli | RFC 7932 | Obrigatório | Google |
| **Imagens** | WebP | 1.3 | Obrigatório | Google |
| **Imagens** | AVIF | 1.0 | Recomendado | AOMedia |
| **Texturas 3D** | KTX2 | 2.0 | Obrigatório | Khronos Group |
| **Áudio** | Opus | RFC 6716 | Obrigatório | IETF |
| **Vídeo** | AV1 | 1.0 | Recomendado | AOMedia |
| **Fontes** | WOFF2 | 1.0 | Obrigatório | W3C |

---

## 🥽 OPENXR (XR Nativo)

### Especificação

**Versão:** 1.0+  
**Especificação:** https://www.khronos.org/openxr/  
**Status:** Obrigatório para clientes nativos VR/AR

### Uso no Projeto

```cpp
// Inicialização OpenXR
XrInstanceCreateInfo createInfo{XR_TYPE_INSTANCE_CREATE_INFO};
strcpy(createInfo.applicationInfo.applicationName, "Villa Canabrava VR");
createInfo.applicationInfo.applicationVersion = 1;
strcpy(createInfo.applicationInfo.engineName, "AtemporalEngine");
createInfo.applicationInfo.engineVersion = 1;
createInfo.applicationInfo.apiVersion = XR_CURRENT_API_VERSION;

const char* extensions[] = {
    XR_EXT_HAND_TRACKING_EXTENSION_NAME,
    XR_EXT_EYE_GAZE_INTERACTION_EXTENSION_NAME
};
createInfo.enabledExtensionCount = 2;
createInfo.enabledExtensionNames = extensions;

XrInstance instance;
xrCreateInstance(&createInfo, &instance);
```

### Extensões Obrigatórias

| Extensão | Propósito |
|----------|-----------|
| `XR_EXT_hand_tracking` | Rastreamento de mãos |
| `XR_EXT_eye_gaze_interaction` | Interação por olhar |
| `XR_KHR_composition_layer_depth` | Profundidade para reprojeção |
| `XR_EXT_local_floor` | Reference space de chão |

---

## 🌐 WEBXR (XR no Navegador)

### Especificação

**Versão:** Device API + Gamepads Module  
**Especificação:** https://immersive-web.github.io/webxr/  
**Status:** Obrigatório para acesso web imersivo

### Uso no Projeto

```javascript
// Verificar suporte
if ('xr' in navigator) {
    const isSupported = await navigator.xr.isSessionSupported('immersive-vr');
    if (isSupported) {
        // Habilitar botão de VR
    }
}

// Iniciar sessão VR
async function enterVR() {
    const session = await navigator.xr.requestSession('immersive-vr', {
        requiredFeatures: ['local-floor'],
        optionalFeatures: ['hand-tracking', 'layers']
    });
    
    // Configurar reference space
    const referenceSpace = await session.requestReferenceSpace('local-floor');
    
    // Configurar render loop
    const gl = canvas.getContext('webgl2', { xrCompatible: true });
    const xrLayer = new XRWebGLLayer(session, gl);
    session.updateRenderState({ baseLayer: xrLayer });
    
    // Iniciar loop
    session.requestAnimationFrame(onXRFrame);
}

// Render frame
function onXRFrame(time, frame) {
    const session = frame.session;
    const pose = frame.getViewerPose(referenceSpace);
    
    if (pose) {
        for (const view of pose.views) {
            renderView(view);
        }
    }
    
    session.requestAnimationFrame(onXRFrame);
}
```

### Feature Requirements

| Feature | Necessidade | Fallback |
|---------|-------------|----------|
| `local-floor` | Obrigatório | `local` |
| `hand-tracking` | Recomendado | Controllers |
| `layers` | Recomendado | - |

---

## 🎨 WEBGPU (Render Moderno Web)

### Especificação

**Versão:** W3C Working Draft 2024  
**Especificação:** https://www.w3.org/TR/webgpu/  
**Status:** Obrigatório para render web

### Uso no Projeto

```javascript
// Inicialização WebGPU
async function initWebGPU() {
    if (!navigator.gpu) {
        throw new Error('WebGPU não suportado');
    }
    
    const adapter = await navigator.gpu.requestAdapter({
        powerPreference: 'high-performance'
    });
    
    if (!adapter) {
        throw new Error('Nenhum adaptador GPU encontrado');
    }
    
    const device = await adapter.requestDevice({
        requiredFeatures: [],
        requiredLimits: {}
    });
    
    return { adapter, device };
}

// Configurar canvas
const canvas = document.getElementById('world-canvas');
const context = canvas.getContext('webgpu');

const canvasFormat = navigator.gpu.getPreferredCanvasFormat();
context.configure({
    device,
    format: canvasFormat,
    alphaMode: 'premultiplied'
});

// Pipeline de renderização
const pipeline = device.createRenderPipeline({
    layout: 'auto',
    vertex: {
        module: device.createShaderModule({
            code: vertexShaderCode
        }),
        entryPoint: 'main'
    },
    fragment: {
        module: device.createShaderModule({
            code: fragmentShaderCode
        }),
        entryPoint: 'main',
        targets: [{ format: canvasFormat }]
    },
    primitive: {
        topology: 'triangle-list'
    },
    depthStencil: {
        depthWriteEnabled: true,
        depthCompare: 'less',
        format: 'depth24plus'
    }
});
```

### Fallback para WebGL2

```javascript
// Detecção e fallback
async function initRenderer() {
    if (navigator.gpu) {
        try {
            return await initWebGPU();
        } catch (e) {
            console.warn('WebGPU falhou, usando WebGL2');
        }
    }
    
    // Fallback WebGL2
    return initWebGL2();
}
```

---

## 🧊 GLTF (ASSETS 3D RUNTIME)

### Especificação

**Versão:** 2.0  
**Especificação:** https://www.khronos.org/gltf/  
**ISO:** ISO/IEC 12113:2022  
**Status:** Obrigatório para todos os assets 3D runtime

### Estrutura do Formato

```json
{
  "asset": {
    "version": "2.0",
    "generator": "VillaCanabravaPipeline v1.0",
    "copyright": "© 2026 RC Agropecuária"
  },
  "scene": 0,
  "scenes": [
    {
      "nodes": [0, 1, 2]
    }
  ],
  "nodes": [
    {
      "mesh": 0,
      "translation": [0, 0, 0],
      "rotation": [0, 0, 0, 1],
      "scale": [1, 1, 1]
    }
  ],
  "meshes": [
    {
      "primitives": [
        {
          "attributes": {
            "POSITION": 0,
            "NORMAL": 1,
            "TEXCOORD_0": 2
          },
          "indices": 3,
          "material": 0,
          "mode": 4
        }
      ]
    }
  ],
  "materials": [
    {
      "pbrMetallicRoughness": {
        "baseColorTexture": {
          "index": 0
        },
        "metallicFactor": 0.0,
        "roughnessFactor": 0.8
      },
      "normalTexture": {
        "index": 1
      }
    }
  ],
  "textures": [
    {
      "sampler": 0,
      "source": 0
    }
  ],
  "images": [
    {
      "uri": "textures/sede_baseColor.ktx2"
    }
  ],
  "samplers": [
    {
      "magFilter": 9729,
      "minFilter": 9987,
      "wrapS": 10497,
      "wrapT": 10497
    }
  ],
  "accessors": [
    {
      "bufferView": 0,
      "componentType": 5126,
      "count": 1000,
      "type": "VEC3",
      "max": [10, 10, 10],
      "min": [-10, -10, -10]
    }
  ],
  "bufferViews": [
    {
      "buffer": 0,
      "byteOffset": 0,
      "byteLength": 12000
    }
  ],
  "buffers": [
    {
      "uri": "sede.bin",
      "byteLength": 12000
    }
  ],
  "extensionsUsed": [
    "KHR_draco_mesh_compression",
    "KHR_texture_basisu"
  ],
  "extensionsRequired": [
    "KHR_draco_mesh_compression"
  ]
}
```

### Extensões Obrigatórias

| Extensão | Propósito | Status |
|----------|-----------|--------|
| `KHR_draco_mesh_compression` | Compressão de geometria | Obrigatório |
| `KHR_texture_basisu` | Texturas KTX2/Basis | Obrigatório |
| `KHR_mesh_quantization` | Quantização de vértices | Recomendado |
| `KHR_materials_unlit` | Materiais não-iluminados | Opcional |
| `EXT_mesh_gpu_instancing` | Instancing para repetição | Recomendado |

---

## 🏗️ OPENUSD (CENAS E PRODUÇÃO)

### Especificação

**Versão:** 23.08+  
**Especificação:** https://openusd.org/  
**AOUSD:** Alliance for OpenUSD  
**Status:** Obrigatório para fonte de produção

### Estrutura de Camada

```python
# Estrutura OpenUSD para Villa Canabrava
from pxr import Usd, UsdGeom, Sdf, Gf

# Criar stage
stage = Usd.Stage.CreateNew('villa_canabrava.usda')

# Definir unidades (SI)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Estrutura hierárquica
root = stage.DefinePrim('/VillaCanabrava')
root.SetMetadata('comment', 'Universo Virtual Villa Canabrava')

# Sede
sede = stage.DefinePrim('/VillaCanabrava/Sede_VillaTerezinha')
sede.SetTypeName('Xform')
sede.GetReferences().AddReference('./sede.usda')

# Pivôs
pivos = stage.DefinePrim('/VillaCanabrava/Pivos')
for i in range(1, 8):
    pivo = stage.DefinePrim(f'/VillaCanabrava/Pivos/Pivo_{i}')
    pivo.GetReferences().AddReference(f'./pivo_{i}.usda')

# Mata (referenciada, não duplicada)
mata = stage.DefinePrim('/VillaCanabrava/Mata_Nativa')
mata.GetReferences().AddReference('./mata.usda')

# Salvar
stage.GetRootLayer().Save()
```

### Schema Customizado

```python
# Schema para elementos da fazenda
from pxr import Usd, UsdGeom, Sdf, Gf, Tf
from pxr import UsdSchemaBase

class FarmFeatureAPI(UsdSchemaBase):
    """API para features da fazenda"""
    
    @classmethod
    def _GetSchemaTypeName(cls):
        return 'FarmFeatureAPI'
    
    def GetFeatureTypeAttr(self):
        return self.GetPrim().GetAttribute('farm:featureType')
    
    def GetAreaHectaresAttr(self):
        return self.GetPrim().GetAttribute('farm:areaHectares')
    
    def GetCentroidAttr(self):
        return self.GetPrim().GetAttribute('farm:centroid')

# Uso
feature = FarmFeatureAPI.Apply(prim)
feature.GetFeatureTypeAttr().Set('pivo_irrigacao')
feature.GetAreaHectaresAttr().Set(45.89)
feature.GetCentroidAttr().Set(Gf.Vec3d(-43.947, -17.385, 850))
```

---

## 🌐 QUIC + HTTP/3 (TRANSPORTE)

### Especificação

**QUIC:** RFC 9000  
**HTTP/3:** RFC 9114  
**Status:** Obrigatório para comunicação cliente-servidor

### Implementação

```go
// Servidor HTTP/3 em Go (quic-go)
package main

import (
    "context"
    "crypto/tls"
    "log"
    
    "github.com/quic-go/quic-go"
    "github.com/quic-go/quic-go/http3"
)

func main() {
    // Configuração TLS 1.3 (obrigatório para QUIC)
    tlsConfig := &tls.Config{
        MinVersion: tls.VersionTLS13,
        Certificates: []tls.Certificate{cert},
    }
    
    // Configuração QUIC
    quicConfig := &quic.Config{
        MaxIdleTimeout: 30 * time.Second,
        EnableDatagrams: true,  // Para WebTransport
    }
    
    // Servidor HTTP/3
    server := &http3.Server{
        Addr:      ":443",
        TLSConfig: tlsConfig,
        QuicConfig: quicConfig,
        Handler:   handler,
    }
    
    log.Fatal(server.ListenAndServe())
}
```

### Vantagens sobre TCP/HTTP/2

| Aspecto | TCP+HTTP/2 | QUIC+HTTP/3 | Benefício |
|---------|------------|-------------|-----------|
| Handshake | 2-3 RTT | 0-1 RTT | Latência reduzida |
| Head-of-line | Sim (TCP) | Não | Multiplexação real |
| Migração | Reconecta | Mantém | WiFi ↔ 4G sem perda |
| Congestion | TCP Reno/Cubic | BBRv2 | Mais eficiente |

---

## 🗺️ OGC 3D TILES (GEOSPACIAL)

### Especificação

**Versão:** 1.1  
**Especificação:** https://www.ogc.org/standards/3DTiles  
**Status:** Obrigatório para streaming de dados geoespaciais massivos

### Estrutura de Tileset

```json
{
  "asset": {
    "version": "1.1",
    "tilesetVersion": "1.0.0",
    "generator": "VillaCanabravaGIS"
  },
  "geometricError": 1000,
  "root": {
    "boundingVolume": {
      "region": [
        -44.005069, -17.441287, -43.884716, -17.312838,
        800, 1200
      ]
    },
    "geometricError": 500,
    "refine": "REPLACE",
    "content": {
      "uri": "root.b3dm"
    },
    "children": [
      {
        "boundingVolume": {
          "region": [
            -44.0, -17.4, -43.9, -17.35,
            800, 1000
          ]
        },
        "geometricError": 100,
        "content": {
          "uri": "sede/tileset.json"
        }
      },
      {
        "boundingVolume": {
          "region": [
            -44.0, -17.45, -43.95, -17.4,
            800, 1000
          ]
        },
        "geometricError": 100,
        "content": {
          "uri": "pivos/tileset.json"
        }
      }
    ]
  }
}
```

### Conversão de KML para 3D Tiles

```python
# Pipeline de conversão
from py3dtiles import Tileset, B3dm, GlTF
import geopandas as gpd

def kml_to_3dtiles(kml_path, output_dir):
    # Ler KML
    gdf = gpd.read_file(kml_path)
    
    # Converter para glTF
    gltf = convert_to_gltf(gdf)
    
    # Criar B3DM (Batched 3D Model)
    b3dm = B3dm.from_gltf(gltf)
    
    # Criar tileset
    tileset = Tileset()
    tileset.root.bounding_volume = calculate_bbox(gdf)
    tileset.root.content = b3dm
    
    # Salvar
    tileset.save(output_dir)
```

---

## 🔐 OPENID CONNECT (IDENTIDADE)

### Especificação

**Versão:** Core 1.0 + Discovery + Dynamic Registration  
**Especificação:** https://openid.net/developers/specs/  
**Status:** Obrigatório para autenticação

### Fluxo de Autenticação

```
┌─────────┐                                    ┌─────────┐
│ Cliente │                                    │  OIDC   │
│   App   │                                    │ Provider│
└────┬────┘                                    └────┬────┘
     │                                             │
     │ 1. /authorize?client_id=...&redirect_uri=...│
     │────────────────────────────────────────────▶│
     │                                             │
     │ 2. Redirect para Login do Provider          │
     │◀────────────────────────────────────────────│
     │                                             │
     │ 3. Usuário autentica                        │
     │────────────────────────────────────────────▶│
     │                                             │
     │ 4. Redirect com code=xxx                    │
     │◀────────────────────────────────────────────│
     │                                             │
     │ 5. /token (code, client_secret)             │
     │────────────────────────────────────────────▶│
     │                                             │
     │ 6. {access_token, id_token, refresh_token}  │
     │◀────────────────────────────────────────────│
     │                                             │
     │ 7. /userinfo (access_token)                 │
     │────────────────────────────────────────────▶│
     │                                             │
     │ 8. {sub, name, email, picture}              │
     │◀────────────────────────────────────────────│
```

### Claims Obrigatórios

```json
{
  "sub": "auth0|123456789",
  "name": "João Silva",
  "given_name": "João",
  "family_name": "Silva",
  "nickname": "joaosilva",
  "preferred_username": "joaosilva",
  "email": "joao.silva@email.com",
  "email_verified": true,
  "picture": "https://cdn.villacanabrava.world/avatars/joaosilva.webp",
  "updated_at": 1707177600,
  "https://villacanabrava.world/roles": ["user", "researcher"],
  "https://villacanabrava.world/permissions": ["read:world", "write:annotations"]
}
```

---

## 📡 GRPC + PROTOCOL BUFFERS (API INTERNA)

### Especificação

**Versão:** proto3  
**Especificação:** https://grpc.io/  
**Status:** Obrigatório para comunicação interna entre serviços

### Definição de Serviços

```protobuf
// villa_canabrava/world/v1/world.proto
syntax = "proto3";

package villa_canabrava.world.v1;

option go_package = "github.com/villacanabrava/api/go/world/v1";
option java_package = "world.villa_canabrava.world.v1";

// Serviço de estado do mundo
service WorldService {
  // Unary RPC
  rpc GetEntity(GetEntityRequest) returns (Entity);
  
  // Server streaming
  rpc StreamEntities(StreamEntitiesRequest) returns (stream EntityUpdate);
  
  // Client streaming
  rpc BatchUpdateEntities(stream EntityUpdate) returns (BatchUpdateResponse);
  
  // Bidirectional streaming
  rpc SyncEntities(stream EntityUpdate) returns (stream EntityUpdate);
}

message GetEntityRequest {
  string entity_id = 1;
}

message Entity {
  string entity_id = 1;
  string entity_type = 2;
  Transform transform = 3;
  map<string, bytes> properties = 4;
  int64 version = 5;
  int64 timestamp = 6;
}

message Transform {
  Vector3 position = 1;
  Quaternion rotation = 2;
  Vector3 scale = 3;
}

message Vector3 {
  double x = 1;
  double y = 2;
  double z = 3;
}

message Quaternion {
  double x = 1;
  double y = 2;
  double z = 3;
  double w = 4;
}

message EntityUpdate {
  string entity_id = 1;
  oneof update_type {
    TransformUpdate transform = 2;
    PropertyUpdate properties = 3;
    DeleteUpdate delete = 4;
  }
  int64 timestamp = 5;
  int64 version = 6;
}
```

---

## 📝 OPENAPI (DOCUMENTAÇÃO DE API)

### Especificação

**Versão:** 3.1.0  
**Especificação:** https://spec.openapis.org/oas/v3.1.0  
**Status:** Obrigatório para APIs públicas

### Exemplo de Especificação

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: Villa Canabrava API
  version: 1.0.0
  description: API pública do Universo Virtual Villa Canabrava
  contact:
    name: API Support
    email: api@villacanabrava.world
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0

servers:
  - url: https://api.villacanabrava.world/v1
    description: Production
  - url: https://api.staging.villacanabrava.world/v1
    description: Staging

paths:
  /world/entities/{entityId}:
    get:
      summary: Get entity by ID
      operationId: getEntity
      parameters:
        - name: entityId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Entity found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Entity'
        '404':
          description: Entity not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

components:
  schemas:
    Entity:
      type: object
      required:
        - entityId
        - entityType
        - transform
      properties:
        entityId:
          type: string
          format: uuid
        entityType:
          type: string
          enum: [sede, pivo, mata, casa_colono, curral]
        transform:
          $ref: '#/components/schemas/Transform'
        properties:
          type: object
          additionalProperties: true
    
    Transform:
      type: object
      properties:
        position:
          $ref: '#/components/schemas/Vector3'
        rotation:
          $ref: '#/components/schemas/Quaternion'
        scale:
          $ref: '#/components/schemas/Vector3'
    
    Vector3:
      type: object
      properties:
        x: { type: number, format: double }
        y: { type: number, format: double }
        z: { type: number, format: double }
    
    Quaternion:
      type: object
      properties:
        x: { type: number, format: double }
        y: { type: number, format: double }
        z: { type: number, format: double }
        w: { type: number, format: double }
```

---

**FIM DA ESPECIFICAÇÃO DE PADRÕES**
