# CONFIGURAÇÃO PORTA PostgreSQL

**Porta Selecionada:** 5433 (não 5432)

---

## ⚠️ IMPORTANTE

Se você usou porta **5433** na instalação, precisa atualizar o script.

---

## 🔧 COMO CORRIGIR

### Opção 1: Usar Padrão (Recomendado)

Reinstale PostgreSQL com porta padrão **5432**:
```
Desinstalar → Reinstalar com porta 5432
```

### Opção 2: Atualizar Script

Se já instalou com 5433, abra `SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py`:

**Linha ~17, altere:**
```python
"shadow_db": {
    "host": "localhost",
    "port": 5433,  # <- ALTERE PARA 5433 (do padrão 5432)
    ...
}
```

---

## ✅ APÓS INSTALAR

Verifique:
```powershell
psql -h localhost -p 5433 -U postgres -c "SELECT version();"
```

Se funcionar, execute:
```powershell
python SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py
```

---

**Próximo:** Continuar com instalação
