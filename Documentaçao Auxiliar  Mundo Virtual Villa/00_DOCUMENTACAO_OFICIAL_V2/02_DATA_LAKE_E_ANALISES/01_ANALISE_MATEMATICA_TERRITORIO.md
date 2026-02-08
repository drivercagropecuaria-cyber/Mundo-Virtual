# 📐 ANÁLISE MATEMÁTICA DO TERRITÓRIO
## Modelagem Quantitativa e Algorítmica da Fazenda Villa Canabrava

**Versão:** 2.0 (Revisão Analítica Expandida)
**Data:** 06 de Fevereiro de 2026
**Base de Dados:** 252 camadas KML, 7.729,26 hectares
**Objetivo:** Fornecer base matemática para simulação física, econômica e ambiental.

---

## 📊  1.0 DIMENSÕES FUNDAMENTAIS E VARIÁVEIS ESPACIAIS

### Área e Perímetro

| Métrica | Valor | Unidade | Variável de Código |
|---------|-------|---------|--------------------|
| **Área Total** | 7.729,26 | hectares | `World_Size_Ha` |
| | 77,29 | km² | `World_Size_Km2` |
| **Perímetro** | 58,21 | km | `Boundary_Length` |
| **Extensão Leste-Oeste** | 13,40 | km | `World_Bounds_X` |
| **Extensão Norte-Sul** | 14,30 | km | `World_Bounds_Y` |

### Coordenadas Geográficas e Grid de Simulação

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTENSÃO GEOGRÁFICA (Bounding Box)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Latitude:  -17.441287°  ━━━━━━━━━━━━━━━━━━━━━━━  -17.312838°              │
│             (Sul)                              (Norte)                      │
│                                                                             │
│  Longitude: -44.005069°  ━━━━━━━━━━━━━━━━━━━━━━━  -43.884716°              │
│             (Oeste)                            (Leste)                      │
│                                                                             │
│  Centroide: -43.944892°, -17.377063°  (Origem do Mundo Virtual [0,0,0])     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Fórmulas de Conversão (Geo -> Game Engine)

**Metros por Grau (Aproximação em Latitude -17°):**
- 1° Lat ≈ 110.8 km
- 1° Long ≈ 106.4 km

**Fórmula de Projeção Planar Local:**
```python
def geo_to_vector3(lat, lon, alt):
    x = (lon - CENTROID_LON) * 106400
    z = (lat - CENTROID_LAT) * 110800
    y = alt
    return (x, y, z)
```

---

## 🌳 2.0 ANÁLISE DE PRESERVAÇÃO E BIOMASSA

### Distribuição e Potencial de Captura

| Categoria | Área (ha) | % do Total | Fórmula | Estimativa Carbono (t/ha/ano)* |
|-----------|-----------|------------|---------|------------------------------|
| **Mata Nativa** | 1.784,79 | 23,09% | A_mata / A_total | 10.5 |
| **Reserva Legal** | 1.568,96 | 20,30% | A_rl / A_total | 9.0 |
| **APPs** | 87,91 | 1,14% | A_app / A_total | 12.0 |
| **Área Preservada** | 3.441,66 | 44,53% | ΣA_preservada | *Média Ponderada* |
| **Área Produtiva** | 4.287,60 | 55,47% | - | - |

*\*Valores estimados para Cerrado/Mata de Transição.*

### Modelo de Sequestro de Carbono (Variável Dinâmica)

```
Sequestro_Total_Ano = Σ (Area_Bioma[i] * Fator_Sequestro[i] * Saude_Bioma)

Onde:
- Saude_Bioma é uma variável 0.0 a 1.0 controlada pelo Cenário Climático.
```
**Potencial Estimado:** ~35.000 toneladas de Carbono/ano (Baseline).

---

## 💧 3.0 MODELAGEM HÍDRICA PREDITIVA

**Volume de Reservatórios Virtuais:**
Considerando profundidade média de 1.5m para Lagoas e Brejos:

| Corpo D'água | Área (ha) | Volume Est. (m³) | Variável de Nível |
|--------------|-----------|-------------------|-------------------|
| Lagoas | 7.18 | ~107.700 | `Water_Level_Lakes` |
| Brejos | 22.69 | ~340.350 | `Water_Level_Swamps` |

**Cenário de Seca (Alert Trigger):**
Se `Precipitacao_Acumulada_30d < 50mm` AND `Uso_Pivos > 80%`:
-> Reduzir `Water_Level` em 0.5% ao dia.
-> Alterar texturas da borda para "Lama Seca".

---

## 📏 4.0 DENSIDADE DE ELEMENTOS E COMPLEXIDADE DE CENA

### Fórmula Geral de Densidade

```
Densidade = Número de Elementos / Área (km²)
```

### Densidades Calculadas para Otimização de Instancing

| Elemento | Quantidade | Densidade (por km²) | Estratégia de Render |
|----------|------------|---------------------|----------------------|
| Cercas | 312 | 4,04 | Spline Mesh Component |
| Poços Artesianos | 19 | 0,25 | Blueprint Actor (Baixo custo) |
| Casas de Colono | 8 | 0,10 | Mesh Único (Hero Asset) |
| Pivôs | 7 | 0,09 | Animação Procedural |
| Árvores (Est.) | ~1.5M | ~19.000 | Foliage System + HISM |
| Mata (fragmentos) | 154 | 1,99 |

### Análise de Distribuição Espacial

**Área média por fragmento de mata:**
```
Ā_fragmento = A_mata / N_fragmentos
            = 1.784,79 / 154
            = 11,59 ha
```

**Comprimento médio de cerca:**
```
L_cerca_total = 1.164,15 km (perímetro total das cercas)
L_cerca_média = 1.164,15 / 312 = 3,73 km
```

---

## 📐 GEOMETRIA DOS PIVÔS

### Áreas dos Sistemas de Irrigação

| Pivô | Área (ha) | Status | Raio Estimado (m) |
|------|-----------|--------|-------------------|
| Pivô 1 | 45,89 | Ativo | 382 |
| Pivô 2 | 52,77 | Ativo | 410 |
| Pivô 3 | 49,50 | Ativo | 397 |
| Pivô 4 | 12,50 | Ativo | 200 |
| Pivô 6 | 28,42 | Ativo | 301 |
| Pivô 7 | 46,28 | Projeto | 383 |
| Pivô 8 | 14,00 | Projeto | 211 |

### Cálculo do Raio

Para um pivô central circular:
```
A = π × r²
r = √(A / π)

Exemplo (Pivô 1):
r = √(45,89 × 10.000 / π) = √146.089 = 382 m
```

### Área Total Irrigada

```
A_total_pivos = Σ A_i
              = 45,89 + 52,77 + 49,50 + 12,50 + 28,42 + 46,28 + 14,00
              = 249,36 ha

A_ativa = 45,89 + 52,77 + 49,50 + 12,50 + 28,42 = 189,08 ha
A_projeto = 46,28 + 14,00 = 60,28 ha
```

---

## 🌲 ANÁLISE DA MATA NATIVA

### Fragmentação

| Métrica | Valor | Fórmula |
|---------|-------|---------|
| Número de fragmentos | 154 | - |
| Área total | 1.784,79 ha | - |
| Área média | 11,59 ha | A_total / N |
| Perímetro total | 179,24 km | - |
| Maior fragmento | 1.034,45 ha | max(A_i) |

### Índice de Área de Mancha (PAI)

```
PAI = A_maior / A_total
    = 1.034,45 / 1.784,79
    = 0,580
```

**Interpretação:**
- PAI > 0,5: Dominância de um grande fragmento
- 0,2 < PAI < 0,5: Distribuição moderada
- PAI < 0,2: Alta fragmentação

**Conclusão:** A mata tem distribuição moderada com tendência à dominância do maior fragmento.

### Efeito de Borda

```
Profundidade de borda: 50 m

P_borda = Perímetro × Profundidade
        = 179,24 km × 50 m
        = 179.240 m × 50 m
        = 8.962.000 m²
        = 896,20 ha

A_interior = A_total - A_borda
           = 1.784,79 - 896,20
           = 888,59 ha (49,8%)
```

---

## 💧 ANÁLISE HÍDRICA

### Consumo de Água dos Pivôs

**Parâmetros:**
- Lamina aplicada: 10 mm/dia
- Período de irrigação: 180 dias/ano
- Eficiência do pivô: 85%

**Cálculos:**

```
Volume por hectare:
V_ha = 10 mm/dia × 180 dias × 10 m³/ha/mm
     = 18.000 m³/ha/ano

Volume total (área ativa):
V_total = 189,08 ha × 18.000 m³/ha
        = 3.403.440 m³/ano
        = 3,4 bilhões de litros

Vazão necessária:
Q = (189,08 ha × 10 mm × 10 m³/ha/mm) / (18 h × 3.600 s)
Q = 292 L/s
Q = 1.050 m³/h
```

### Economia de Água

Comparativo com irrigação por gravidade (eficiência 40%):

```
V_gravidade = V_pivo × (η_pivo / η_gravidade)
            = 3.403.440 × (0,85 / 0,40)
            = 7.232.310 m³

Economia = V_gravidade - V_pivo
         = 7.232.310 - 3.403.440
         = 3.828.870 m³/ano (53%)
```

---

## 🌍 SEQUESTRO DE CARBONO

### Estimativa de Sequestro

**Taxa para Cerrado:** 7,5 ton CO₂/ha/ano

```
Sequestro total = A_mata × Taxa
                = 1.784,79 ha × 7,5 ton/ha/ano
                = 13.386 ton CO₂/ano

Equivalente em árvores:
N_arvores = (13.386 × 1.000 kg) / 20 kg/árvore/ano
          = 669.296 árvores
```

### Balanço de Carbono

**Emissões da produção agrícola:**
```
Produção estimada = 189,08 ha × 8 ton/ha = 1.513 ton/ano
Pegada de carbono = 1.513 ton × 0,5 ton CO₂/ton = 756 ton CO₂/ano
```

**Saldo:**
```
Saldo = Sequestro - Emissões
      = 13.386 - 756
      = 12.630 ton CO₂/ano (NEGATIVO ✓)
```

---

## 📊 ESTATÍSTICAS SUMÁRIAS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESTATÍSTICAS VILLA CANABRAVA                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TERRITÓRIO:                                                               │
│  • Área: 7.729,26 ha (77,29 km²)                                           │
│  • Perímetro: 58,21 km                                                     │
│  • Extensão: 13,40 km (E-W) × 14,30 km (N-S)                               │
│                                                                             │
│  PRESERVAÇÃO:                                                              │
│  • Área preservada: 3.441,66 ha (44,53%)                                   │
│  • Mata nativa: 1.784,79 ha (23,09%)                                       │
│  • Reserva legal: 1.568,96 ha (20,30%)                                     │
│  • APPs: 87,91 ha (1,14%)                                                  │
│                                                                             │
│  INFRAESTRUTURA:                                                           │
│  • Pivôs: 7 (249,36 ha irrigados)                                          │
│  • Poços: 19 artesianos                                                    │
│  • Cercas: 312 (1.164 km)                                                  │
│  • Casas de colono: 8                                                      │
│                                                                             │
│  SUSTENTABILIDADE:                                                         │
│  • Sequestro de CO₂: 13.386 ton/ano                                        │
│  • Economia de água: 3,8 milhões m³/ano                                    │
│  • Saldo de carbono: -12.630 ton CO₂/ano (NEGATIVO)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**FIM DA ANÁLISE MATEMÁTICA DO TERRITÓRIO**
