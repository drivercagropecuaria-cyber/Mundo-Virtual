# 📑 ESCOPO DA FUNDAÇÃO
## Escopo Definitivo da Fase 1 - Fundação Digital Villa Canabrava

**Versão:** 1.0 (Inicial)
**Data:** 06 de Fevereiro de 2026
**Estratégia:** Consolidação da Base Documental, Tecnológica e Conceitual
**Classificação:** Documento de Escopo - Referência para Aprovações

---

## 🎯 1.0 OBJETIVO DA FASE DE FUNDAÇÃO
A fase de "Fundação" não se trata apenas de construir documentação, mas de estabelecer a **infraestrutura imutável** sobre a qual todo o Universo Virtual será construído. O sucesso desta fase é medido pela qualidade, precisão e interoperabilidade dos ativos gerados, não pela quantidade visual final.

**Objetivo Primário:** Entregar um "Digital Twin" (Gêmeo Digital) de dados estruturados da fazenda (Geoespacial + Histórico), pronto para ser consumido por qualquer motor de renderização (Unreal, Unity, Web).

**Objetivo Secundário:** Estabelecer a governança dos dados e os pipelines de produção de ativos.

---

## ✅ 2.0 ESCOPO DO PRODUTO (O Que Será Entregue)

### 2.1 Módulo Geoespacial (A Base Física)
*   **Conversão de Dados:** Tradução perfeita de 252 camadas KML para formatos `GeoJSON` e `PostGIS`.
*   **Modelo de Terreno:** Criação de um *Heightmap* de alta precisão (LOD 0) da área total de 7.729 ha.
*   **Vetorização:** Mapeamento 3D de:
    *   312 feições de cercas (Splines).
    *   154 polígonos de mata nativa (Volumes de Procedural Foliage).
    *   7 sistemas de pivô (Blueprints com lógica de rotação).
*   **Validação:** Relatório de consistência topológica (sem sobreposições ou vértices órfãos).

### 2.2 Módulo Audiovisual e Histórico (A Alma)
*   **Museu Virtual (MVP):** Ambiente navegável (Web 3D) contendo:
    *   Hall de Entrada com Timeline Interativa da Fazenda.
    *   Sala de Mapas (Visualização GIS simplificada).
    *   Galeria de Fotos Históricas (Metadados padronizados).
*   **Biblioteca Digital:** Sistema indexado de busca para documentos, fotos e vídeos.
*   **Narrativa:** Roteiro base para o "Tour do Visitante" (Vozes, textos e waypoints).

### 2.3 Módulo de Infraestrutura (O Suporte)
*   **Arquitetura de Servidores:** Setup inicial de nuvem (AWS/Azure) para hospedagem de assets.
*   **Pipeline de CI/CD:** Automação básica para deploy do Museu Virtual.
*   **Controle de Versão:** Repositório Git estruturado para código e LFS (Large File Storage) para assets binários.

---

## 🚫 3.0 FORA DO ESCOPO (O Que NÃO Será Entregue Agora)
Para garantir o foco qualificado, definimos explicitamente o que fica para as **Fases 2 e 3**:

*   ❌ **Multijogador Massivo (MMO):** A fase 1 é focada na experiência *single-player* ou *assíncrona*.
*   ❌ **Simulação Física Complexa em Tempo Real:** Nada de fluídos dinâmicos ou física de destruição nesta etapa.
*   ❌ **Integração IoT em Tempo Real:** Dados de sensores dos pivôs entrarão apenas como *mockups* (dados simulados), não conexão ao vivo.
*   ❌ **VR/AR Full Experience:** O foco inicial é Web 3D (Acessível via browser). VR será uma extensão futura.
*   ❌ **Economia Virtual (Tokenomics):** Implementação de marketplace ou moedas fica para a Fase 4.

---

## 📋 4.0 CRITÉRIOS DE ACEITE (Definition of Done)

Para considerar a Fundação **concluída**, os seguintes itens devem ser validados:

1.  **Validação Geométrica:** O mapa 3D deve ter desvio máximo de < 1m em relação aos dados KML originais.
2.  **Performance Web:** O Museu Virtual deve carregar em < 10 segundos em conexões 4G padrão.
3.  **Documentação:** Todos os códigos e processos devem ter documentação técnica (sem dívida técnica inicial).
4.  **Acessibilidade:** A interface deve seguir padrões WCAG básicos (contraste, navegação por teclado).
5.  **Segurança:** Dados sensíveis (documentos privados da fazenda) devem estar em buckets criptografados, visíveis apenas a usuários autorizados.

---

## 📅 5.0 MARCOS DE ENTREGA (Milestones)

| Milestone | Descrição | Prazo Estimado |
|-----------|-----------|----------------|
| **MS-01** | **Frozen Geo:** Todos os dados KML processados e importados na Engine. | Mês 1 |
| **MS-02** | **Whitebox Museum:** Estrutura 3D do museu navegável (sem texturas finais). | Mês 2 |
| **MS-03** | **Alpha Release:** Primeira versão funcional com dados reais e assets visuais. | Mês 3 |
| **MS-04** | **Foundation Complete:** Validação final e entrega da documentação técnica. | Mês 4 |

---
