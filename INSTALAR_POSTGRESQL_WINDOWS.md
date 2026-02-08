# INSTALAR POSTGRESQL 15 NO WINDOWS

**Duração:** ~5-10 minutos  
**Sistema:** Windows 11  
**Objetivo:** Instalar PostgreSQL para rodar o orchestrator  

---

## 🚀 OPÇÃO RÁPIDA (Recomendado)

### 1. Download

Clique no link:
👉 https://www.postgresql.org/download/windows/

Você verá: "PostgreSQL 15.X Download"

### 2. Executar Instalador

- Baixará arquivo `.exe` (~100MB)
- Dê duplo clique para instalar
- Selecione:
  - ✅ PostgreSQL Server
  - ✅ pgAdmin 4 (útil para gerenciar BD)
  - ✅ Stack Builder (pular)
  - ✅ Command Line Tools (IMPORTANTE!)

### 3. Senha

Durante instalação:
```
Usuário: postgres
Senha: postgres
```

Guarde essa senha!

### 4. Porta

Deixe padrão: `5432`

### 5. Finalize

Clique "Finish"

---

## ✅ VERIFICAR INSTALAÇÃO

### Abra PowerShell e execute:

```powershell
psql --version
```

**Esperado:**
```
psql (PostgreSQL) 15.X
```

Se não funcionar, adicione ao PATH manualmente (veja abaixo).

---

## 🔧 SE NÃO ENCONTRAR PSQL

### Adicione PostgreSQL ao PATH:

1. **Abra "Variáveis de Ambiente"**
   - Windows Search: "Variáveis de Ambiente"
   - Clique "Editar Variáveis de Ambiente do Sistema"

2. **Clique "Variáveis de Ambiente..."**

3. **Na seção "Variáveis do sistema", encontre "Path"**
   - Clique "Editar"

4. **Adicione o caminho do PostgreSQL**
   ```
   C:\Program Files\PostgreSQL\15\bin
   ```
   - Clique "Novo"
   - Cole o caminho acima
   - Clique "OK"

5. **Feche e abra novo PowerShell**

6. **Teste novamente:**
   ```powershell
   psql --version
   ```

---

## 🐳 OPÇÃO 2: DOCKER (Se preferir)

Se tiver Docker instalado:

```powershell
# Baixar imagem
docker pull postgres:15

# Rodar container
docker run --name pgserver -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres:15

# Verificar se rodando
docker ps
```

Pronto! PostgreSQL estará em `localhost:5432`

---

## 📋 CHECKLIST

- [ ] PostgreSQL 15 baixado
- [ ] Instalador executado
- [ ] Selecione "Command Line Tools"
- [ ] Senha configurada: `postgres`
- [ ] Porta: `5432` (padrão)
- [ ] Terminal fechado e reaberto
- [ ] `psql --version` funciona
- [ ] Visto: `psql (PostgreSQL) 15.X`

---

## ⏭️ PRÓXIMOS PASSOS

### Depois de instalar:

1. Verifique novamente:
```powershell
psql --version
```

2. Execute o orchestrator:
```powershell
cd "C:\Users\rober\Desktop\Mundo Virtual Villa Canabrava"
python SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py
```

3. Aguarde ~90 minutos

---

## 🆘 TROUBLESHOOTING

| Problema | Solução |
|----------|---------|
| `psql` not found | Adicione ao PATH (veja acima) |
| Port 5432 em uso | Mude porta na instalação ou: `netstat -ano \| findstr :5432` |
| Instalador não baixa | Use este link: https://sbp.enterprisedb.com/getfile.jsp?fileid=14745 |
| Problema de permissão | Abra PowerShell como Admin |

---

## 🎯 TEMPO TOTAL

```
5 min: Download + Instalação
2 min: Verificar PATH (se necessário)
1 min: Testar (psql --version)
─────────────
~8-10 minutos TOTAL
```

**Depois:** Execute o orchestrator (90 min mais)

---

**Data:** 2026-02-06  
**Status:** Guia de instalação rápida
