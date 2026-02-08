# 🛠️ GUIA TÉCNICO - CAMINHOS E CONFIGURAÇÕES PRÉ-FLIGHT
## Mundo Virtual Villa Canabrava - Windows 11 Environment

**Data:** 6 FEB 2026 18:07 UTC-3  
**Sistema:** Windows 11  
**Shell Padrão:** cmd.exe  
**Ambiente:** VS Code + Supabase CLI + PostgreSQL  

---

## 📍 LOCALIZAÇÃO DOS ARQUIVOS PRINCIPAIS

### 1️⃣ DOCKER COMPOSE

```
CAMINHO: BIBLIOTECA/supabase/docker-compose.yml
CONFIRMADO: ✅ Arquivo existe em BIBLIOTECA/supabase/
TIPO: docker-compose.yml (Supabase stack)

USAR COMANDO:
cd BIBLIOTECA && docker-compose -f supabase/docker-compose.yml ps

OU (versão mais nova):
cd BIBLIOTECA && docker compose -f supabase/docker-compose.yml ps
```

### 2️⃣ POSTGRESQL CLIENT (psql)

#### Opção A: Via WSL (Recomendado no Windows)
```
Se PostgreSQL instalado no WSL:
wsl psql -U postgres -d villa_canabrava -c "SELECT version();"

Ou no WSL shell:
psql -U postgres -d villa_canabrava -c "SELECT version();"
```

#### Opção B: Via PostgreSQL Windows Installation
```
Se PostgreSQL instalado no Windows:
C:\Program Files\PostgreSQL\15\bin\psql.exe

COMANDO COMPLETO:
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -d villa_canabrava -c "SELECT version();"

OU adicionar ao PATH e usar:
psql -U postgres -d villa_canabrava -c "SELECT version();"
```

#### Opção C: Via Docker (Dentro do Container)
```
Se Docker container está rodando:
docker-compose -f BIBLIOTECA/supabase/docker-compose.yml exec db psql -U postgres -d villa_canabrava -c "SELECT version();"
```

#### Opção D: Via Docker Exec (Alternativa)
```
docker exec <container_id> psql -U postgres -d villa_canabrava -c "SELECT version();"

Onde <container_id> pode ser obtido com:
docker ps | grep supabase
```

---

## 🔍 COMO VERIFICAR QUAL OPÇÃO USAR

### Verificar se Docker está instalado
```powershell
docker --version

Se sucesso: Docker version X.X.X
Se erro: Docker não instalado
```

### Verificar se PostgreSQL está instalado (Windows)
```powershell
psql --version

Se sucesso: psql (PostgreSQL) X.X
Se erro: PostgreSQL não no PATH
```

### Verificar se WSL está disponível
```powershell
wsl --list --verbose

Se sucesso: Lista WSL distros
Se erro: WSL não configurado
```

---

## 🚀 PASSOS PRÉ-FLIGHT CORRIGIDOS

### PASSO 1: Verificar Docker

```powershell
# Terminal PowerShell ou cmd.exe

# Comando 1: Ver se Docker está rodando
docker ps

# Esperado: Lista de containers (pode estar vazia)
# Ou: Docker Desktop deve estar rodando

# Comando 2: Verificar docker-compose
cd BIBLIOTECA
docker-compose -f supabase/docker-compose.yml ps

# Esperado:
# supabase-api       Up (healthy)
# supabase-db        Up (healthy)
# supabase-studio    Up
```

### PASSO 2: Verificar PostgreSQL Client

**Se usando Docker (recomendado):**
```powershell
# Modo 1: Via docker-compose exec
cd BIBLIOTECA
docker-compose -f supabase/docker-compose.yml exec db psql -U postgres -c "SELECT version();"

# Esperado:
# PostgreSQL 13.x (or newer) on x86_64...
```

**Se usando PostgreSQL Windows:**
```powershell
# Verificar versão primeiro
psql --version

# Se funciona, testar conexão:
psql -U postgres -d villa_canabrava -c "SELECT version();"
```

**Se usar WSL:**
```powershell
# Via WSL
wsl psql -U postgres -d villa_canabrava -c "SELECT version();"
```

### PASSO 3: Verificar Migrations

```powershell
# Via PowerShell - verificar se arquivos existem
Test-Path "BIBLIOTECA\supabase\migrations\1770500100_auto_partition_creation_2029_plus.sql"
Test-Path "BIBLIOTECA\supabase\migrations\1770500200_mv_refresh_scheduling_cron.sql"

# Esperado: True (arquivo existe)

# Via cmd.exe
dir BIBLIOTECA\supabase\migrations\1770500100*
dir BIBLIOTECA\supabase\migrations\1770500200*
```

### PASSO 4: Validar SQL Syntax

**Via Docker Compose Exec:**
```powershell
cd BIBLIOTECA
docker-compose -f supabase/docker-compose.yml exec db psql -U postgres -d villa_canabrava < supabase\migrations\1770500100_auto_partition_creation_2029_plus.sql

# Esperado:
# Sem mensagens de erro
# Função criada
# Trigger criado
```

**Via psql local:**
```powershell
# Se PostgreSQL está no PATH
psql -U postgres -d villa_canabrava -f "BIBLIOTECA\supabase\migrations\1770500100_auto_partition_creation_2029_plus.sql"
```

---

## 📋 RECOMENDAÇÃO PARA AMBIENTE WINDOWS 11

### Setup Ideal
```
1. Docker Desktop (mais fácil no Windows)
   └─ Gerencia automaticamente containers
   └─ Não precisa instalar PostgreSQL separadamente

2. Docker Compose v2 (incluído no Docker Desktop)
   └─ Gerencia stack Supabase completo

3. VSCode com Docker Extension
   └─ Ver containers e logs visualmente
```

### Comandos Recomendados para Pré-Flight

```powershell
# PASSO 1: Verificar Docker
docker ps
docker --version

# PASSO 2: Iniciar Stack Supabase
cd BIBLIOTECA
docker-compose -f supabase/docker-compose.yml up -d

# Aguardar ~30 segundos para containers iniciarem
Start-Sleep -Seconds 30

# PASSO 3: Verificar se DB está pronto
docker-compose -f supabase/docker-compose.yml ps

# PASSO 4: Testar conexão PostgreSQL
docker-compose -f supabase/docker-compose.yml exec db psql -U postgres -c "SELECT version();"

# PASSO 5: Validar migrations
docker-compose -f supabase/docker-compose.yml exec db psql -U postgres -d villa_canabrava -f supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql

# Se tudo OK:
echo "✅ PRÉ-FLIGHT VALIDADO COM SUCESSO"
```

---

## ⚠️ TROUBLESHOOTING

### Erro: "docker: command not found"
```
Solução: Instalar Docker Desktop
https://www.docker.com/products/docker-desktop
```

### Erro: "postgres: command not found"
```
Solução 1: Usar Docker (comando docker-compose)
Solução 2: Instalar PostgreSQL no Windows
Solução 3: Usar WSL com PostgreSQL
```

### Erro: "Connection refused"
```
Solução: Verificar se containers estão rodando
docker ps | findstr supabase

Se não aparecer, iniciar:
docker-compose -f BIBLIOTECA/supabase/docker-compose.yml up -d
```

### Erro: "database villa_canabrava does not exist"
```
Solução: Aguardar container terminar inicialização (~30-60 seg)
Ou: Verificar no BIBLIOTECA/supabase/docker-compose.yml se DB está criado

Ou testar sem database:
psql -U postgres -c "SELECT version();"
```

---

## 📊 VERIFICAÇÃO FINAL - CHECKLIST

```
[ ] Docker instalado: ✅ / ❌
    Comando: docker --version
    
[ ] Docker Desktop rodando: ✅ / ❌
    Ver: Ícone Docker na taskbar
    
[ ] docker-compose funciona: ✅ / ❌
    Comando: docker-compose --version
    
[ ] Arquivo docker-compose.yml existe: ✅ / ❌
    Caminho: BIBLIOTECA/supabase/docker-compose.yml
    
[ ] Containers estão rodando: ✅ / ❌
    Comando: docker-compose -f BIBLIOTECA/supabase/docker-compose.yml ps
    
[ ] PostgreSQL acessível: ✅ / ❌
    Comando: docker-compose -f BIBLIOTECA/supabase/docker-compose.yml exec db psql -U postgres -c "SELECT 1;"
    
[ ] Database villa_canabrava existe: ✅ / ❌
    Comando: psql -U postgres -d villa_canabrava -c "SELECT 1;"
    
[ ] Migrations existem: ✅ / ❌
    Comando: ls BIBLIOTECA/supabase/migrations/1770500100*
    
RESULTADO FINAL: 🟢 PRONTO / 🟡 MAIORIA OK / 🔴 BLOQUEADO
```

---

## 🎯 PARA COMEÇAR AGORA

### Forma Mais Simples (Docker Recomendado)

```powershell
# 1. Abra PowerShell como Admin
# 2. Naveguue para o projeto
cd "c:\Users\rober\Desktop\Mundo Virtual Villa Canabrava"

# 3. Inicie o stack
cd BIBLIOTECA
docker-compose -f supabase/docker-compose.yml up -d

# 4. Aguarde 30 segundos
Start-Sleep -Seconds 30

# 5. Verifique se está tudo ok
docker-compose -f supabase/docker-compose.yml ps

# 6. Teste conexão
docker-compose -f supabase/docker-compose.yml exec db psql -U postgres -c "SELECT version();"
```

Se vir uma versão PostgreSQL, então ✅ **PRÉ-FLIGHT PASSOU!**

---

**Guia Técnico por:** Roo Agent - Infrastructure  
**Data:** 6 FEB 2026 18:07 UTC-3  
**Compatibilidade:** Windows 11, Docker Desktop, PostgreSQL 13+

---
