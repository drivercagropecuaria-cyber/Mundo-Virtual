# EVIDENCIAS PADRAO - TEMPLATE + CHECKLIST
**Objetivo:** Padronizar evidencias rastreaveis em cada sprint e anexar aos EXEC_REPORTs.
**Status:** Pronto para uso

---

## TEMPLATE DE EVIDENCIAS (PADRAO)

### 1) Identificacao do Ciclo
- Sprint: <S1 | S2 | S3>
- Data/Hora (ISO8601): <YYYY-MM-DDTHH:MM:SSZ>
- Responsavel: <nome/role>
- Ambiente: <local | CI | staging>
- Escopo: <P0 | Sprint 1 | Sprint 2>

### 2) Evidencia Primaria (Obrigatoria)
- Artefato: <arquivo/relatorio>
- Caminho: <path relativo no repo>
- Link rastreavel: <link relativo no repo>
- Resultado: <PASS/FAIL + resumo>

### 3) Evidencias Tecnicas (Logs/Outputs)
- Comando executado:
  - <comando completo>
- Exit code: <0 | 1>
- Output (resumo):
  - <linhas-chave>
- Arquivo de log (se existir): <path>

### 4) Evidencias Complementares (Opcional)
- Captura/print: <path>
- JSON de validacao: <path>
- Queries SQL executadas: <path>

---

## CHECKLIST AUTOMATICO (PREENCHIMENTO OBRIGATORIO)

- [ ] Pre-Flight executado e log salvo
- [ ] Grep/Findstr para termos obsoletos registrado
- [ ] Validacao de bounds GIS registrada
- [ ] Logs/outputs de RPCs registrados
- [ ] Relatorio JSON de geometria registrado (quando aplicavel)
- [ ] Migrations criticas citadas com link rastreavel
- [ ] RPCs/Views citadas com link rastreavel
- [ ] EXEC_REPORT atualizado com bloco de evidencias

---

## BLOCO PADRAO PARA EXEC_REPORT (COPIAR/COLAR)

```markdown
## EVIDENCIAS (PADRAO)
- **Pre-Flight**: <link> (Exit code: <0/1>)
- **Grep termos obsoletos**: <link> (Resultado: <PASS/FAIL>)
- **GIS Bounds**: <link> (Match: <percent>)
- **RPCs (logs/outputs)**: <link>
- **JSON Geometria**: <link> (Validity: <percent>)
- **Migrations**: <link(s)>
- **RPCs/Views**: <link(s)>
- **Timestamp**: <ISO8601>
```

---

## NOTAS DE USO
- Use links relativos para garantir rastreabilidade.
- Registre apenas evidencias do escopo fechado do sprint.
- Nunca use JSON legacy para bounds; validar bounds apenas no relatorio oficial.
