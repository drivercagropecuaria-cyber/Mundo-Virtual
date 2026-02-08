# Relatorio de comandos para execucao

Data: 2026-02-07

## Limpeza segura (simulacao)

- Executar em modo WhatIf e revisar o log:

```powershell
.\scripts\repo_cleanup.ps1 -WhatIf -ExcludeLegacy
```

## Limpeza segura (execucao real, somente apos aprovacao)

```powershell
.\scripts\repo_cleanup.ps1 -WhatIf:$false -ExcludeLegacy
```

## Verificacao rapida de scripts Python

```powershell
& "C:\Users\rober\AppData\Local\Programs\Python\Python310\python.exe" -m compileall scripts
```

## Pipeline GIS (referencia rapida)

- Seguir o guia em [../docs/START_HERE.md](../docs/START_HERE.md) para importacao, validacao e exportacao.

## Observacao

- Nao executar comandos destrutivos sem aprovacao explicita.
