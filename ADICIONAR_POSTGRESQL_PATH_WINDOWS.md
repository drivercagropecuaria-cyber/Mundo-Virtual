# ADICIONAR POSTGRESQL AO PATH DO WINDOWS

**Problema:** `psql` não reconhecido no PowerShell

---

## 🔧 SOLUÇÃO RÁPIDA (2 minutos)

### Passo 1: Abrir "Variáveis de Ambiente"
```
Windows Search → "Variáveis de Ambiente" → Enter
Clique: "Editar Variáveis de Ambiente do Sistema"
```

### Passo 2: Clique em "Variáveis de Ambiente..."

### Passo 3: Na seção "Variáveis do Sistema"
```
Procure: "Path"
Clique: "Editar"
```

### Passo 4: Clique "Novo" e adicione:
```
C:\Program Files\PostgreSQL\15\bin
```

(Se instalou em local diferente, ajuste o número da versão)

### Passo 5: Clique OK → OK → OK

### Passo 6: Feche todas as janelas PowerShell/CMD

### Passo 7: Abra NOVA janela PowerShell e teste:
```powershell
psql --version
```

Se aparecer `psql (PostgreSQL) 15.X`, funcionou!

---

## ⚡ PRÓXIMO

```powershell
# Testar conexão
psql -h localhost -p 5433 -U postgres -c "SELECT version();"

# Se funcionar, execute:
python SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py
```

---

**Tempo:** ~2 minutos  
**Depois:** Orchestrator roda automaticamente por ~90 min
