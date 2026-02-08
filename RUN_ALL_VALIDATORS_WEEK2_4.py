#!/usr/bin/env python3
"""
Master Validator Runner: OPT2-OPT5 Complete Validation Suite
Executa todos os validadores sequencialmente e gera relatório consolidado
"""

import json
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidatorRunner:
    """Executa suite completa de validadores OPT2-OPT5"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {}
        self.validators = [
            {
                "name": "OPT2_COLUMNAR_STORAGE_VALIDATOR",
                "script": "OPT2_COLUMNAR_STORAGE_VALIDATOR.py",
                "output": "OPT2_COLUMNAR_STORAGE_VALIDATION_REPORT.json",
                "description": "Validar armazenamento columnar (12.4M geometrias)"
            },
            {
                "name": "OPT3_INDEXED_VIEWS_RPC_SEARCH_VALIDATOR",
                "script": "OPT3_INDEXED_VIEWS_VALIDATOR.py",
                "output": "OPT3_INDEXED_VIEWS_RPC_VALIDATION_REPORT.json",
                "description": "Validar views indexadas + RPC search optimization"
            },
            {
                "name": "OPT45_PARTITION_SCHEDULING_VALIDATOR",
                "script": "OPT45_PARTITION_SCHEDULING_VALIDATOR.py",
                "output": "OPT45_PARTITION_SCHEDULING_VALIDATION_REPORT.json",
                "description": "Validar scheduling automático de partições"
            },
            {
                "name": "OPT2_OPT5_PERFORMANCE_SIMULATOR",
                "script": "OPT2_OPT5_PERFORMANCE_SIMULATOR.py",
                "output": "OPT2_OPT5_PERFORMANCE_SIMULATION_REPORT.json",
                "description": "Simular performance combinada OPT2-OPT5"
            },
        ]
    
    def run_validator(self, validator_info: dict) -> bool:
        """Executar um validador individual"""
        logger.info("=" * 80)
        logger.info(f"EXECUTANDO: {validator_info['name']}")
        logger.info(f"Descrição: {validator_info['description']}")
        logger.info("=" * 80)
        
        try:
            script_path = Path(validator_info["script"])
            if not script_path.exists():
                logger.error(f"Script não encontrado: {script_path}")
                return False
            
            # Executar script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"Script falhou com código {result.returncode}")
                logger.error(f"STDERR: {result.stderr}")
                return False
            
            # Ler output JSON
            output_path = Path(validator_info["output"])
            if output_path.exists():
                with open(output_path, 'r') as f:
                    data = json.load(f)
                    self.results[validator_info["name"]] = {
                        "status": "SUCCESS",
                        "output_file": str(output_path),
                        "report": data
                    }
                logger.info(f"✓ {validator_info['name']} concluído com sucesso")
                return True
            else:
                logger.error(f"Arquivo de output não encontrado: {output_path}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout executando {validator_info['name']}")
            return False
        except Exception as e:
            logger.error(f"Erro executando {validator_info['name']}: {e}")
            return False
    
    def run_all_validators(self) -> bool:
        """Executar todos os validadores sequencialmente"""
        logger.info("\n" + "=" * 80)
        logger.info("INICIANDO SUITE DE VALIDADORES OPT2-OPT5")
        logger.info("=" * 80)
        logger.info(f"Timestamp: {self.start_time.isoformat()}")
        logger.info(f"Total de validadores: {len(self.validators)}")
        
        success_count = 0
        for i, validator in enumerate(self.validators, 1):
            logger.info(f"\n[{i}/{len(self.validators)}] Executando {validator['name']}...")
            
            if self.run_validator(validator):
                success_count += 1
                time.sleep(1)  # Pequeno delay entre execuções
            else:
                logger.warning(f"Falha ao executar {validator['name']}")
        
        logger.info("\n" + "=" * 80)
        logger.info(f"RESUMO: {success_count}/{len(self.validators)} validadores executados com sucesso")
        logger.info("=" * 80)
        
        return success_count == len(self.validators)
    
    def generate_consolidated_report(self) -> dict:
        """Gerar relatório consolidado de todos os validadores"""
        logger.info("\n" + "=" * 80)
        logger.info("GERANDO RELATÓRIO CONSOLIDADO")
        logger.info("=" * 80)
        
        # Extrair métricas principais
        opt2_report = self.results.get("OPT2_COLUMNAR_STORAGE_VALIDATOR", {}).get("report", {})
        opt3_report = self.results.get("OPT3_INDEXED_VIEWS_RPC_SEARCH_VALIDATOR", {}).get("report", {})
        opt45_report = self.results.get("OPT45_PARTITION_SCHEDULING_VALIDATOR", {}).get("report", {})
        opt25_report = self.results.get("OPT2_OPT5_PERFORMANCE_SIMULATOR", {}).get("report", {})
        
        # Consolidado
        consolidated = {
            "execution_timestamp": self.start_time.isoformat(),
            "execution_duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "total_validators_run": len(self.results),
            "all_validators_successful": len(self.results) == len(self.validators),
            
            "summary_metrics": {
                "opt2_storage_reduction_percent": self._get_metric(
                    opt2_report, "summary", "key_metrics", "storage_reduction_percent", 0
                ),
                "opt3_avg_improvement_percent": self._get_metric(
                    opt3_report, "validation_sections", "materialized_views", "avg_improvement_percent", 0
                ),
                "opt45_partition_improvement_percent": self._get_metric(
                    opt45_report, "summary", "key_metrics", "cpu_overhead_percent", 0
                ),
                "combined_overhead_reduction_percent": self._get_metric(
                    opt25_report, "summary", "achieved_overhead_reduction_percent", None, 0
                ),
            },
            
            "validation_results": {
                "opt2_ready": self._get_metric(
                    opt2_report, "summary", "opt2_ready_for_staging", False
                ),
                "opt3_ready": self._get_metric(
                    opt3_report, "summary", "opt3_ready_for_staging", False
                ),
                "opt45_ready": self._get_metric(
                    opt45_report, "summary", "opt4_opt5_ready_for_staging", False
                ),
                "performance_target_met": self._get_metric(
                    opt25_report, "summary", "target_met", False
                ),
            },
            
            "recommendations": {
                "opt2": self._get_metric(opt2_report, "summary", "recommendation", ""),
                "opt3": self._get_metric(opt3_report, "summary", "recommendation", ""),
                "opt45": self._get_metric(opt45_report, "summary", "recommendation", ""),
                "combined": self._get_metric(opt25_report, "summary", "recommendation", ""),
            },
            
            "individual_reports": {
                "opt2": opt2_report,
                "opt3": opt3_report,
                "opt45": opt45_report,
                "combined": opt25_report,
            }
        }
        
        return consolidated
    
    @staticmethod
    def _get_metric(obj, *keys, default=None):
        """Extrair métrica aninhada de um dicionário"""
        current = obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    @staticmethod
    def _format_percent(value, fallback="0.0%"):
        if value is None:
            return fallback
        try:
            return f"{float(value):.1f}%"
        except Exception:
            return str(value)
    
    def save_consolidated_report(self, report: dict):
        """Salvar relatório consolidado em arquivo"""
        output_file = "CONSOLIDATED_VALIDATION_REPORT_WEEK2_4.json"
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Relatório consolidado salvo em: {output_file}")
        
        return output_file
    
    def print_summary(self, report: dict):
        """Imprimir resumo de validação"""
        logger.info("\n" + "=" * 80)
        logger.info("RESUMO FINAL DE VALIDAÇÃO")
        logger.info("=" * 80)
        
        metrics = report.get("summary_metrics", {})
        
        logger.info("\nMÉTRICAS PRINCIPAIS:")
        val = metrics.get("opt2_storage_reduction_percent") or 0.0
        logger.info(f"  OPT2 Storage Reduction: {float(val):.1f}%")
        logger.info(
            "  OPT3 Average Improvement: "
            f"{self._format_percent(metrics.get('opt3_avg_improvement_percent'))}"
        )
        logger.info(
            "  Combined Overhead Reduction: "
            f"{self._format_percent(metrics.get('combined_overhead_reduction_percent'))}"
        )
        
        validation = report.get("validation_results", {})
        logger.info("\nSTATUS DE PRONTO:")
        logger.info(f"  OPT2 Ready: {'✓ YES' if validation.get('opt2_ready') else '✗ NO'}")
        logger.info(f"  OPT3 Ready: {'✓ YES' if validation.get('opt3_ready') else '✗ NO'}")
        logger.info(f"  OPT4-OPT5 Ready: {'✓ YES' if validation.get('opt45_ready') else '✗ NO'}")
        logger.info(f"  Performance Target Met: {'✓ YES' if validation.get('performance_target_met') else '✗ NO'}")
        
        recommendations = report.get("recommendations", {})
        logger.info("\nRECOMENDAÇÕES:")
        if recommendations.get('combined'):
            logger.info(f"  Combined: {recommendations.get('combined', '')}")
        
        if report.get("all_validators_successful"):
            logger.info("\n✅ TODOS OS VALIDADORES EXECUTADOS COM SUCESSO")
        else:
            logger.info("\n⚠️  ALGUNS VALIDADORES FALHARAM")
        
        duration = report.get("execution_duration_seconds", 0)
        logger.info(f"\nDuração total de execução: {duration:.1f}s ({duration/60:.1f}min)")
    
    def run_complete_validation(self):
        """Executar validação completa"""
        try:
            # Executar todos os validadores
            all_success = self.run_all_validators()
            
            if not all_success and len(self.results) == 0:
                logger.error("Nenhum validador foi executado com sucesso")
                return False
            
            # Gerar relatório consolidado
            report = self.generate_consolidated_report()
            
            # Salvar relatório
            self.save_consolidated_report(report)
            
            # Imprimir resumo
            self.print_summary(report)
            
            return all_success
            
        except Exception as e:
            logger.error(f"Erro durante validação completa: {e}", exc_info=True)
            return False

def main():
    """Executar suite de validadores"""
    logger.info("\n")
    logger.info("╔" + "=" * 78 + "╗")
    logger.info("║" + " " * 78 + "║")
    logger.info("║" + "  VALIDAÇÃO WEEK 2-4: OPT2-OPT5 STAGING PREPARATION".center(78) + "║")
    logger.info("║" + "  Infraestrutura completa para validação em staging".center(78) + "║")
    logger.info("║" + " " * 78 + "║")
    logger.info("╚" + "=" * 78 + "╝\n")
    
    runner = ValidatorRunner()
    success = runner.run_complete_validation()
    
    if success:
        logger.info("\n" + "=" * 80)
        logger.info("✅ VALIDAÇÃO COMPLETA COM SUCESSO")
        logger.info("   Infraestrutura pronta para WEEK 2-4 staging deployment")
        logger.info("=" * 80 + "\n")
        return 0
    else:
        logger.error("\n" + "=" * 80)
        logger.error("❌ VALIDAÇÃO INCOMPLETA")
        logger.error("   Verifique os logs acima para detalhes de erros")
        logger.error("=" * 80 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
