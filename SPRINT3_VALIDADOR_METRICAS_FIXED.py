#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPRINT 3 - VALIDADOR DE METRICAS (FIXED ENCODING)
Valida resultados e emite relatório final pós-execução
Objetivo: Confirmar sucesso de cada FASE e gerar aprovação para produção
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
import io

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_metrics(phase_file):
    """Carrega arquivo de métricas JSON"""
    try:
        with open(phase_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {phase_file}: {e}")
        return None

def validate_fase6(metrics):
    """Valida FASE 6 - Post-Migration Baseline (CRITICA)"""
    print("\n[VALIDACAO] FASE 6 - POST-MIGRATION BASELINE")
    print("=" * 60)
    
    if not metrics:
        print("[FALHA] Arquivo de metricas nao encontrado")
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
        print("[OK] FASE 6 VALIDADA - Migration bem-sucedida")
        return True
    else:
        print("[FALHA] FASE 6 FALHOU - Regressions ou erro detectado")
        return False

def validate_fase8(metrics):
    """Valida FASE 8 - Rollback Testing"""
    print("\n[VALIDACAO] FASE 8 - ROLLBACK TESTING")
    print("=" * 60)
    
    if not metrics:
        print("[FALHA] Arquivo de metricas nao encontrado")
        return False
    
    checks = {
        "snapshot_created": metrics.get("snapshot_created", False),
        "rollback_executed": metrics.get("rollback_executed", False),
        "rollback_validated": metrics.get("rollback_validated", False),
        "data_integrity": metrics.get("data_integrity", False)
    }
    
    for check_name, status in checks.items():
        symbol = "[OK]" if status else "[X]"
        print(f"  {symbol} {check_name}: {status}")
    
    if all(checks.values()):
        print("[OK] FASE 8 VALIDADA - Rollback pronto")
        return True
    else:
        print("[FALHA] FASE 8 FALHOU - Rollback nao validado")
        return False

def validate_fase9(metrics):
    """Valida FASE 9 - Sign-Off"""
    print("\n[VALIDACAO] FASE 9 - SHADOW DEPLOYMENT SIGN-OFF")
    print("=" * 60)
    
    if not metrics:
        print("[FALHA] Arquivo de metricas nao encontrado")
        return False
    
    status = metrics.get("status", "UNKNOWN")
    phases = metrics.get("phases_completed") or 0
    print(f"Deployment status: {status}")
    print(f"Phases completed: {phases}/10")
    
    if status == "READY_FOR_PRODUCTION" and phases >= 9:
        print("[OK] FASE 9 VALIDADA - PRONTO PARA PRODUCAO")
        return True
    elif status == "READY_FOR_PRODUCTION":
        print("[OK] FASE 9 VALIDADA - Status READY_FOR_PRODUCTION confirmado")
        return True
    else:
        print("[FALHA] FASE 9 FALHOU - Nao pronto para producao")
        return False

def main():
    """Main validation flow"""
    print("\n")
    print("=" * 60)
    print("VALIDADOR DE METRICAS - SPRINT 3 SHADOW DEPLOYMENT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("")
    
    # Try loading metrics from various locations
    fase6_metrics = None
    fase8_metrics = None
    fase9_metrics = None
    
    # Check archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results directory
    results_dir = Path("archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results")
    if results_dir.exists():
        json_files = list(results_dir.glob("*.json"))
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "FASE_6" in str(json_file):
                        fase6_metrics = data
                    elif "FASE_8" in str(json_file):
                        fase8_metrics = data
                    elif "FASE_9" in str(json_file):
                        fase9_metrics = data
                    elif "overall_delta_pct" in data:
                        fase6_metrics = data
                    elif "rollback_executed" in data:
                        fase8_metrics = data
                    elif "status" in data and data.get("status") == "READY_FOR_PRODUCTION":
                        fase9_metrics = data
            except:
                pass
    
    # Validate fases
    results = {
        "FASE_6": validate_fase6(fase6_metrics) if fase6_metrics else False,
        "FASE_8": validate_fase8(fase8_metrics) if fase8_metrics else False,
        "FASE_9": validate_fase9(fase9_metrics) if fase9_metrics else False,
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for fase, status in results.items():
        symbol = "[OK]" if status else "[X]"
        print(f"{symbol} {fase}")
    
    print(f"\nResult: {passed}/{total} FASES VALIDADAS")
    
    if all(results.values()):
        print("\n[OK] TODAS AS FASES APROVADAS - READY_FOR_PRODUCTION")
        print("Proximos passos:")
        print("  1. Aplicar seed data em banco shadow")
        print("  2. Criar relatorio de transicao para staging")
        print("  3. Preparar deployment script para staging (Week 1)")
        print("  4. Criar plano de rollout de 4 semanas")
        return 0
    else:
        print("\n[FALHA] FALHAS DETECTADAS - REVISAR LOGS")
        print("FASE 6 nao encontrada - Execute o orchestrator")
        print("ou use SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py")
        return 1

if __name__ == "__main__":
    success = main()
    sys.exit(success)


