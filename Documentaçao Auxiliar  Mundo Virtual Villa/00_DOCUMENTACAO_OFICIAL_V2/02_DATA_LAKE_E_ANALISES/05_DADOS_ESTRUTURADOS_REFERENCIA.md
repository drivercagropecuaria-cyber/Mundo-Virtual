# 📊 DADOS ESTRUTURADOS DE REFERÊNCIA
## Banco de Dados para Construção do Mundo Virtual

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Formatos:** JSON, CSV, Parquet

---

## 📁 ARQUIVOS DISPONÍVEIS

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `dados_geoespaciais.json` | JSON | Dimensões, coordenadas, áreas |
| `dados_ecologicos.json` | JSON | Mata, carbono, biodiversidade |
| `dados_irrigacao.json` | JSON | Pivôs, consumo de água |
| `metricas_performance.json` | JSON | LOD, triângulos, FPS |
| `projecao_usuarios.csv` | CSV | Crescimento 2026-2035 |
| `projecao_trafego.csv` | CSV | Banda, CDN, storage |
| `projecao_financeira.csv` | CSV | Receitas, custos, lucro |
| `projecao_shards.csv` | CSV | Infraestrutura necessária |
| `dados_pivos.csv` | CSV | Sistemas de irrigação |
| `analise_lod.csv` | CSV | Níveis de detalhe |

---

## 🗺️ DADOS GEOESPACIAIS

### Estrutura (JSON)

```json
{
  "area_total_ha": 7729.26,
  "area_total_km2": 77.29,
  "perimetro_km": 58.21,
  "coordenadas": {
    "longitude_min": -44.005069,
    "longitude_max": -43.884716,
    "latitude_min": -17.441287,
    "latitude_max": -17.312838,
    "centroide": [-43.944892, -17.377063]
  },
  "areas_por_categoria": {
    "mata_nativa": 1784.79,
    "reserva_legal": 1568.96,
    "app": 87.91,
    ...
  },
  "area_preservada_ha": 3441.66,
  "area_produtiva_ha": 4287.60,
  "percentual_preservado": 44.53,
  "percentual_produtivo": 55.47
}
```

### Uso

```python
import json

with open('dados_geoespaciais.json') as f:
    dados = json.load(f)

area_total = dados['area_total_ha']
centroide = dados['coordenadas']['centroide']
```

---

## 👥 PROJEÇÃO DE USUÁRIOS

### Estrutura (CSV)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `ano` | int | Ano da projeção |
| `usuarios_total` | int | Total de usuários cadastrados |
| `usuarios_mensal_medio` | int | Média mensal de usuários ativos |
| `usuarios_diario_medio` | int | Média diária de usuários |
| `usuarios_concorrentes_pico` | int | Pico de usuários simultâneos |
| `crescimento_yoy` | float | Crescimento ano sobre ano (%) |

### Exemplo de Dados

```csv
ano,usuarios_total,usuarios_mensal_medio,usuarios_diario_medio,usuarios_concorrentes_pico,crescimento_yoy
2026,1049,87,2,157,0.0
2027,2189,182,5,328,108.6
2028,5232,436,14,784,139.0
...
```

### Uso

```python
import pandas as pd

df = pd.read_csv('projecao_usuarios.csv')
usuarios_2030 = df[df['ano'] == 2030]['usuarios_total'].values[0]
```

---

## 💰 PROJEÇÃO FINANCEIRA

### Estrutura (CSV)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `ano` | int | Ano |
| `receitas` | int | Total de receitas (USD) |
| `custos` | int | Total de custos (USD) |
| `lucro` | int | Lucro líquido (USD) |
| `margem` | float | Margem de lucro (%) |

### Exemplo de Dados

```csv
ano,receitas,custos,lucro,margem
2026,90524,25671,64853,71.6
2027,141094,25907,115187,81.6
2028,202616,26451,176165,86.9
...
```

---

## ⚡ MÉTRICAS DE PERFORMANCE

### Estrutura (JSON)

```json
{
  "triangulos_sem_lod": 500000000,
  "triangulos_com_lod": 48095800,
  "triangulos_apos_occlusion": 33667060,
  "triangulos_apos_frustum": 26933648,
  "reducao_total_percent": 94.6,
  "economia_lod_percent": 90.4,
  "capacidade_shard_jogadores": 1000,
  "fps_target": 60,
  "tempo_frame_ms": 16.67
}
```

---

## 🌱 DADOS ECOLÓGICOS

### Estrutura (JSON)

```json
{
  "area_mata_ha": 1784.79,
  "num_fragmentos": 154,
  "perimetro_mata_km": 179.24,
  "area_borda_ha": 896.20,
  "area_interior_ha": 888.59,
  "maior_fragmento_ha": 1034.45,
  "indice_pai": 0.580,
  "indice_divisao": 0.785,
  "sequestro_carbono_ton_co2_ano": 13386,
  "arvores_equivalentes": 669296,
  "saldo_carbono_ton_co2_ano": 12630
}
```

---

## 💧 DADOS DE IRRIGAÇÃO

### Estrutura (JSON)

```json
{
  "area_total_pivos_ha": 249.36,
  "area_ativa_ha": 189.08,
  "area_projeto_ha": 60.28,
  "volume_anual_m3": 3403440,
  "vazao_necessaria_lps": 292,
  "vazao_necessaria_m3h": 1050,
  "eficiencia_pivo": 0.85,
  "economia_agua_m3_ano": 3828870,
  "economia_percent": 53
}
```

---

## 🧊 ANÁLISE LOD

### Estrutura (CSV)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `distancia` | int | Distância do observador (m) |
| `lod` | int | Nível de detalhe |
| `triangulos` | int | Número de triângulos |
| `reducao_percent` | float | % de redução vs LOD0 |

### Exemplo de Dados

```csv
distancia,lod,triangulos,reducao_percent
10,0,500000,0.0
50,1,125000,75.0
100,2,31250,93.75
250,3,7813,98.44
500,4,1953,99.61
1000,5,488,99.90
```

---

## 🔄 INTEGRAÇÃO COM SISTEMAS

### Importação para Banco de Dados

```sql
-- PostgreSQL
COPY projecao_usuarios FROM '/path/to/projecao_usuarios.csv' DELIMITER ',' CSV HEADER;

-- Criar views
CREATE VIEW usuarios_por_ano AS
SELECT ano, usuarios_total, usuarios_concorrentes_pico
FROM projecao_usuarios;
```

### Importação para Python

```python
import pandas as pd
import json

# CSV
df_usuarios = pd.read_csv('projecao_usuarios.csv')
df_financeiro = pd.read_csv('projecao_financeira.csv')

# JSON
with open('dados_geoespaciais.json') as f:
    geo = json.load(f)

with open('dados_ecologicos.json') as f:
    eco = json.load(f)
```

### Importação para JavaScript

```javascript
// Fetch JSON
const response = await fetch('/data/dados_geoespaciais.json');
const geo = await response.json();

// Parse CSV
import Papa from 'papaparse';
const usuarios = Papa.parse(csvText, { header: true }).data;
```

---

## 📊 VISUALIZAÇÃO RECOMENDADA

### Gráficos Sugeridos

| Dado | Tipo de Gráfico | Ferramenta |
|------|-----------------|------------|
| Crescimento de usuários | Linha | Matplotlib, D3.js |
| Projeção financeira | Área | Matplotlib, Chart.js |
| Distribuição de áreas | Pizza | Matplotlib, Plotly |
| LOD | Barras | Matplotlib |
| Shards necessários | Linha | Matplotlib |

### Exemplo (Python)

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('projecao_usuarios.csv')

plt.figure(figsize=(10, 6))
plt.plot(df['ano'], df['usuarios_total'], marker='o')
plt.xlabel('Ano')
plt.ylabel('Usuários')
plt.title('Projeção de Crescimento')
plt.yscale('log')
plt.grid(True)
plt.savefig('crescimento.png')
```

---

**FIM DOS DADOS ESTRUTURADOS**
