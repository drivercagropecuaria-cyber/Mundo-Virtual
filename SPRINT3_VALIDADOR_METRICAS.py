#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPRINT 3 - VALIDADOR DE MÉTRICAS
Valida resultados e emite relatório final pós-execução
Objetivo: Confirmar sucesso de cada FASE e gerar aprovação para produção
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def load_metrics(phase_file):
    """Carrega arquivo de métricas JSON"""
    try:
        with open(phase_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {phase_file}: {e}")
        return None

def validate_fase6(metrics):
    """Valida FASE 6 - Post-Migration Baseline (CRÍTICA)"""
    print("\n[VALIDAÇÃO] FASE 6 - POST-MIGRATION BASELINE")
    print("=" * 60)
    
    if not metrics:
        print("❌ FALHA: Arquivo de métricas não encontrado")
        return False
    
    checks = {
        "overall_delta_pct_negative": metrics.get("overall_delta_pct", 0) < 0,
        "zero_regressions": sum(1 for q in metrics.values() 
                               if isinstance(q, dict) and q.get("verdict") == "REGRESSION") == 0,
        "final_verdict_pass": metrics.get("final_verdict") == "PASS"
    }
    
    print(f"Overall improvement: {metrics.get('overall_delta_pct', 0)}%")
    print(f"Final verdict: {metrics.get('final_verdict', 'UNKNOWN')}")
    print(f"Q1 delta: {metrics.get('Q1_ST_Contains', {}).get('delta_pct', 0)}%")
    print(f"Q2 delta: {metrics.get('Q2_ST_Intersects', {}).get('delta_pct', 0)}%")
    print(f"Q3 delta: {metrics.get('Q3_ST_DWithin', {}).get('delta_pct', 0)}%")
    
    if all(checks.values()):
        print("✅ FASE 6 VALIDADA - Migration bem-sucedida")
        return True
    else:
        print("❌ FASE 6 FALHOU - Regressions ou erro detectado")
        return False

def validate_fase8(metrics):
    """Valida FASE 8 - Rollback Testing"""
    print("\n[VALIDAÇÃO] FASE 8 - ROLLBACK TESTING")
    print("=" * 60)
    
    if not metrics:
        print("❌ FALHA: Arquivo de métricas não encontrado")
        return False
    
    checks = {
        "snapshot_created": metrics.get("snapshot_created", False),
        "rollback_executed": metrics.get("rollback_executed", False),
        "rollback_validated": metrics.get("rollback_validated", False),
        "data_integrity": metrics.get("data_integrity", False)
    }
    
    for check_name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {check_name}: {status}")
    
    if all(checks.values()):
        print("✅ FASE 8 VALIDADA - Rollback pronto")
        return True
    else:
        print("❌ FASE 8 FALHOU - Rollback não validado")
        return False

def validate_fase9(metrics):
    """Valida FASE 9 - Sign-Off"""
    print("\n[VALIDAÇÃO] FASE 9 - SHADOW DEPLOYMENT SIGN-OFF")
    print("=" * 60)
    
    if not metrics:
        print("❌ FALHA: Arquivo de métricas não encontrado")
        return False
    
    status = metrics.get("status", "UNKNOWN")
    print(f"Deployment status: {status}")
    print(f"Phases completed: {metrics.get('phases_completed', 0)}/10")
    
    if status == "READY_FOR_PRODUCTION" and metrics.get("phases_completed") >= 9:
        print("✅ FASE 9 VALIDADA - PRONTO PARA PRODUÇÃO")
        return True
    else:
        print("❌ FASE 9 FALHOU - Não pronto para produção")
        return False

def main():
    """Executa validação completa"""
    results_dir = Path("archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results")
    
    if not results_dir.exists():
        print("❌ Diretório archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results/ não encontrado")
        print("   Execute SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py primeiro")
        return False
    
    print("\n" + "="*60)
    print("VALIDADOR DE METRICAS - SPRINT 3 SHADOW DEPLOYMENT")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Encontrar arquivos de métricas
    fase6_files = list(results_dir.glob("FASE6_POST_MIGRATION_BASELINE_*.json"))
    fase8_files = list(results_dir.glob("FASE8_ROLLBACK_TESTING_*.json"))
    fase9_files = list(results_dir.glob("FASE9_SIGN_OFF_*.json"))
    
    all_passed = True
    
    # Validar FASE 6
    if fase6_files:
        metrics = load_metrics(fase6_files[-1])  # Arquivo mais recente
        if not validate_fase6(metrics):
            all_passed = False
    else:
        print("\n❌ FASE 6 não encontrada - Execute o orchestrator")
        all_passed = False
    
    # Validar FASE 8
    if fase8_files:
        metrics = load_metrics(fase8_files[-1])
        if not validate_fase8(metrics):
            all_passed = False
    else:
        print("\n❌ FASE 8 não encontrada")
        all_passed = False
    
    # Validar FASE 9
    if fase9_files:
        metrics = load_metrics(fase9_files[-1])
        if not validate_fase9(metrics):
            all_passed = False
    else:
        print("\n❌ FASE 9 não encontrada")
        all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ VALIDAÇÃO COMPLETA - SUCESSO")
        print("   Status: APROVADO PARA PRODUCTION DEPLOYMENT")
    else:
        print("❌ VALIDAÇÃO FALHOU - Erros detectados")
        print("   Revisar logs em archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results/")
    
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


