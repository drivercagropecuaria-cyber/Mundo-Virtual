# 📚 DOCUMENTAÇÃO DA BIBLIOTECA DIGITAL VILLA CANABRAVA
## Acervo Virtual da Casa de Memória e Futuro

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Documento de Planejamento

---

## 📋 VISÃO GERAL

A **Biblioteca Digital Villa Canabrava** é o repositório central de todo o acervo documental, fotográfico, audiovisual e cartográfico da fazenda. Constitui a base de dados para o Universo Virtual e a principal ferramenta de preservação e acesso ao patrimônio histórico e cultural da propriedade.

---

## 🎯 OBJETIVOS

### Objetivo Geral
Criar e manter uma biblioteca digital completa, acessível e sustentável que preserve e disponibilize o acervo da Fazenda Villa Canabrava para pesquisa, educação e fruição pública.

### Objetivos Específicos
1. Inventariar e digitalizar 100% do acervo físico existente
2. Criar sistema de busca avançada e intuitivo
3. Garantir preservação digital de longo prazo
4. Facilitar acesso ao público pesquisador
5. Integrar com o Universo Virtual Villa Canabrava
6. Estabelecer padrões de metadados internacionais

---

## 📁 ESTRUTURA DO ACERVO

### Coleções Principais

| Coleção | Itens Estimados | Status | Prioridade |
|---------|-----------------|--------|------------|
| Documentos Textuais | 5.000 | 20% digitalizado | Alta |
| Fotografias | 10.000 | 30% digitalizado | Alta |
| Vídeos | 500 | 50% digitalizado | Alta |
| Áudios | 200 | 10% digitalizado | Média |
| Mapas | 100 | 40% digitalizado | Alta |
| Objetos 3D | - | A criar | Média |

### Organização do Acervo

```
BIBLIOTECA_DIGITAL/
├── COLECOES/
│   ├── Documentos/
│   │   ├── Escrituras/
│   │   ├── Correspondencias/
│   │   ├── Registros_Administrativos/
│   │   └── Documentos_Oficiais/
│   │
│   ├── Fotografias/
│   │   ├── Fotos_Aereas/
│   │   ├── Infraestrutura/
│   │   ├── Atividades/
│   │   ├── Pessoas/
│   │   └── Eventos/
│   │
│   ├── Audiovisual/
│   │   ├── Documentarios/
│   │   ├── Entrevistas/
│   │   ├── Timelapses/
│   │   └── Registros_Sonoros/
│   │
│   ├── Mapas/
│   │   ├── Mapas_Historicos/
│   │   ├── Mapas_Cadastrais/
│   │   └── Mapas_Tematicos/
│   │
│   └── Objetos_Digitais/
│       ├── Modelos_3D/
│       ├── Panoramicas_360/
│       └── Assets/
│
├── METADADOS/
│   ├── Schemas/
│   ├── Templates/
│   └── Vocabularios_Controlados/
│
└── ADMINISTRACAO/
    ├── Usuarios/
    ├── Permissoes/
    └── Estatisticas/
```

---

## 🏷️ SISTEMA DE METADADOS

### Padrão Adotado: Dublin Core + Extensões

**Campos Obrigatórios:**

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| dc:title | Título | "Planta da Sede Villa Terezinha, 1985" |
| dc:creator | Criador | "João Silva, agrimensor" |
| dc:subject | Assunto | "Sede; Arquitetura; Planta baixa" |
| dc:description | Descrição | "Planta baixa da sede principal..." |
| dc:publisher | Publicador | "RC Agropecuária" |
| dc:date | Data | "1985-03-15" |
| dc:type | Tipo | "Mapa; Planta baixa" |
| dc:format | Formato | "image/jpeg; 300dpi" |
| dc:identifier | Identificador | "VC-MAPA-1985-001" |
| dc:source | Fonte | "Arquivo da Sede" |
| dc:language | Idioma | "pt-BR" |
| dc:coverage | Cobertura | "Villa Canabrava; Sede" |
| dc:rights | Direitos | "© RC Agropecuária" |

**Campos Específicos (Extensões):**

| Campo | Descrição | Aplicação |
|-------|-----------|-----------|
| vc:location | Localização geoespacial | Coordenadas WGS84 |
| vc:building | Edificação relacionada | Nome da construção |
| vc:person | Pessoas identificadas | Nomes de pessoas |
| vc:event | Evento relacionado | Nome do evento |
| vc:period | Período histórico | "Década de 1980" |
| vc:condition | Estado de conservação | "Bom; necessita restauração" |

### Esquema de Identificação

**Formato:** `VC-[TIPO]-[ANO]-[SEQUENCIAL]`

**Tipos:**
- DOC: Documentos
- FOT: Fotografias
- VID: Vídeos
- AUD: Áudios
- MAP: Mapas
- OBJ: Objetos 3D

**Exemplo:** `VC-FOT-1985-001` = Fotografia 001 do ano 1985

---

## 🔍 SISTEMA DE BUSCA

### Funcionalidades

**Busca Simples:**
- Por palavra-chave
- Por título
- Por autor/criador

**Busca Avançada:**
- Filtros múltiplos
- Intervalo de datas
- Tipo de material
- Localização geoespacial
- Coleção específica

**Busca por Similaridade:**
- Imagens similares
- Conteúdo relacionado
- Recomendações

### Facetas de Busca

| Faceta | Opções |
|--------|--------|
| Tipo | Documento, Foto, Vídeo, Áudio, Mapa |
| Data | Por década, ano, período |
| Tema | História, Infraestrutura, Pessoas, Eventos |
| Local | Sede, Retiros, Áreas produtivas |
| Formato | Digitalizado, Nativo digital |
| Idioma | Português, Inglês, Outros |
| Acesso | Público, Restrito, Pesquisador |

---

## 💻 INTERFACE DO USUÁRIO

### Telas Principais

**1. Página Inicial**
- Destaques do acervo
- Busca principal
- Navegação por coleções
- Estatísticas

**2. Resultados de Busca**
- Lista de itens
- Filtros laterais
- Visualização em grade/lista
- Paginação

**3. Página do Item**
- Visualizador de mídia
- Metadados completos
- Itens relacionados
- Opções de download/compartilhamento

**4. Coleções**
- Apresentação temática
- Narrativas guiadas
- Tours virtuais

### Visualizadores

**Documentos:**
- PDF.js para PDFs
- Zoom e navegação
- Anotações

**Imagens:**
- OpenSeadragon (zoom profundo)
- Comparação lado a lado
- Galeria

**Vídeos:**
- Video.js
- Legendas
- Capítulos

**Áudio:**
- WaveSurfer.js
- Transcrição sincronizada

---

## 🔐 GESTÃO DE ACESSO

### Níveis de Usuário

| Nível | Permissões | Requisitos |
|-------|------------|------------|
| Público | Visualização de itens públicos | Nenhum |
| Cadastrado | Download de baixa resolução | Cadastro gratuito |
| Pesquisador | Download de alta resolução | Aprovação de cadastro |
| Institucional | API, dados em massa | Convite institucional |
| Administrador | Gestão completa | Credencial interna |

### Política de Direitos

**Acesso Público:**
- Itens sem restrições de direitos
- Baixa resolução para web

**Acesso Restrito:**
- Itens com direitos autorais
- Documentos sensíveis
- Alta resolução sob solicitação

**Acesso Pesquisador:**
- Acervo completo
- Dados brutos
- API de consulta

---

## 💾 PRESERVAÇÃO DIGITAL

### Estratégia de Preservação

**3-2-1 Rule:**
- 3 cópias do acervo
- 2 tipos de mídia diferentes
- 1 cópia off-site

**Formatos de Preservação:**

| Tipo | Formato Mestre | Formato de Acesso |
|------|----------------|-------------------|
| Imagens | TIFF (não comprimido) | JPEG2000, JPEG |
| Documentos | PDF/A | PDF |
| Áudio | WAV (PCM) | MP3, OGG |
| Vídeo | FFV1/Matroska | MP4 (H.264) |
| Dados | XML, JSON | API REST |

### Verificação de Integridade

**Checksums:**
- MD5 para verificação rápida
- SHA-256 para preservação

**Monitoramento:**
- Verificação mensal de integridade
- Relatórios de erro
- Ações corretivas

---

## 📊 INDICADORES

### KPIs da Biblioteca

| Indicador | Meta Ano 1 | Meta Ano 3 | Meta Ano 5 |
|-----------|------------|------------|------------|
| Itens catalogados | 5.000 | 15.000 | 25.000 |
| Itens digitalizados | 2.000 | 10.000 | 20.000 |
| Usuários/mês | 500 | 3.000 | 10.000 |
| Downloads/mês | 1.000 | 5.000 | 15.000 |
| Buscas/mês | 2.000 | 10.000 | 30.000 |

---

**FIM DA DOCUMENTAÇÃO DA BIBLIOTECA DIGITAL**
