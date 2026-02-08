#!/usr/bin/env python3
"""
Sprint 3 - OPT5: Documentação Viva (Auto-Generated)
Objetivo: Gerar documentação automáticamente a partir do código
Status: NOVO - Sprint 3 Executor
Data: 2026-02-06 11:45 UTC
"""

import os
import json
import ast
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PARTE 1: Data Classes
# ============================================================================

@dataclass
class FunctionDoc:
    """Documentação de função"""
    name: str
    module: str
    docstring: Optional[str]
    parameters: List[str]
    return_type: Optional[str]
    
    def to_markdown(self) -> str:
        return f"""
### {self.name}
**Module:** `{self.module}`  
**Parameters:** {', '.join(self.parameters) if self.parameters else 'None'}  
**Returns:** {self.return_type or 'None'}

{self.docstring or 'No documentation provided'}
"""


@dataclass
class ClassDoc:
    """Documentação de classe"""
    name: str
    module: str
    docstring: Optional[str]
    methods: List[FunctionDoc]
    
    def to_markdown(self) -> str:
        methods_md = "\n".join([m.to_markdown() for m in self.methods])
        return f"""
## {self.name}
**Module:** `{self.module}`

{self.docstring or 'No documentation provided'}

### Methods
{methods_md}
"""


# ============================================================================
# PARTE 2: Parser de Código Python
# ============================================================================

class PythonCodeParser:
    """Extrai documentação de código Python"""
    
    @staticmethod
    def parse_file(filepath: Path) -> Dict[str, Any]:
        """Parse um arquivo Python e extrai funções/classes"""
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            
            result = {
                'file': str(filepath),
                'classes': [],
                'functions': [],
                'module_docstring': ast.get_docstring(tree)
            }
            
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    result['classes'].append(
                        PythonCodeParser._extract_class(node, filepath)
                    )
                elif isinstance(node, ast.FunctionDef):
                    result['functions'].append(
                        PythonCodeParser._extract_function(node, filepath)
                    )
            
            return result
        
        except Exception as e:
            logger.error(f"Error parsing {filepath}: {e}")
            return {}
    
    @staticmethod
    def _extract_function(node: ast.FunctionDef, filepath: Path) -> FunctionDoc:
        """Extrai info de função"""
        args = [arg.arg for arg in node.args.args]
        return FunctionDoc(
            name=node.name,
            module=str(filepath),
            docstring=ast.get_docstring(node),
            parameters=args,
            return_type=None
        )
    
    @staticmethod
    def _extract_class(node: ast.ClassDef, filepath: Path) -> ClassDoc:
        """Extrai info de classe"""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                methods.append(
                    PythonCodeParser._extract_function(item, filepath)
                )
        
        return ClassDoc(
            name=node.name,
            module=str(filepath),
            docstring=ast.get_docstring(node),
            methods=methods
        )


# ============================================================================
# PARTE 3: Gerador de OpenAPI/Swagger
# ============================================================================

class OpenAPIGenerator:
    """Gera especificação OpenAPI"""
    
    @staticmethod
    def generate_schema() -> Dict[str, Any]:
        """Gera schema OpenAPI básico"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Mundo Virtual Villa Canabrava - API",
                "version": "1.0.0",
                "description": "API para gerenciamento de geometrias e rastreabilidade",
                "contact": {
                    "name": "API Support",
                    "url": "https://github.com/villa-canabrava"
                }
            },
            "paths": {
                "/catalogo/{id}/bounds": {
                    "get": {
                        "summary": "Get bounds para um catálogo",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string"}
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Bounds encontrados",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "min_lat": {"type": "number"},
                                                "max_lat": {"type": "number"},
                                                "min_lon": {"type": "number"},
                                                "max_lon": {"type": "number"}
                                            }
                                        }
                                    }
                                }
                            },
                            "404": {"description": "Bounds não encontrados"}
                        }
                    }
                },
                "/pipeline/refresh-mv": {
                    "post": {
                        "summary": "Dispara refresh de Materialized Views",
                        "responses": {
                            "200": {
                                "description": "Refresh iniciado",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {"type": "string"},
                                                "duration_ms": {"type": "number"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "Bounds": {
                        "type": "object",
                        "properties": {
                            "min_lat": {"type": "number"},
                            "max_lat": {"type": "number"},
                            "min_lon": {"type": "number"},
                            "max_lon": {"type": "number"},
                            "area_km2": {"type": "number"}
                        },
                        "required": ["min_lat", "max_lat", "min_lon", "max_lon"]
                    }
                }
            }
        }


# ============================================================================
# PARTE 4: Gerador de Changelog
# ============================================================================

class ChangelogGenerator:
    """Gera changelog a partir de commits"""
    
    @staticmethod
    def generate_from_git(repo_path: str = ".") -> str:
        """Gera changelog from git log"""
        try:
            # Get commits since last tag
            result = subprocess.run(
                ["git", "log", "--oneline", "-20"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return "# Changelog\n\nNo git repository found."
            
            changelog = "# Changelog - Sprint 3\n\n"
            changelog += "## Recent Changes\n\n"
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    commit_hash, message = line.split(' ', 1)
                    changelog += f"- [{commit_hash[:7]}] {message}\n"
            
            return changelog
        
        except Exception as e:
            logger.error(f"Error generating changelog: {e}")
            return "# Changelog\n\nError generating changelog."


# ============================================================================
# PARTE 5: Documentação Pipeline Completa
# ============================================================================

class DocumentationPipeline:
    """Pipeline completo de geração de documentação"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.docs = {
            'generated_at': datetime.now().isoformat(),
            'api_spec': None,
            'code_docs': [],
            'changelog': None
        }
    
    def generate_all(self) -> Dict[str, Any]:
        """Gera toda documentação"""
        logger.info("Starting documentation generation...")
        
        # 1. Gerar OpenAPI spec
        logger.info("Generating OpenAPI specification...")
        self.docs['api_spec'] = OpenAPIGenerator.generate_schema()
        
        # 2. Extrair documentação de código Python
        logger.info("Scanning Python files...")
        self._extract_python_docs()
        
        # 3. Gerar changelog
        logger.info("Generating changelog...")
        self.docs['changelog'] = ChangelogGenerator.generate_from_git(self.repo_path)
        
        return self.docs
    
    def _extract_python_docs(self):
        """Extrai docs de arquivos Python"""
        python_files = list(Path(self.repo_path).glob('**/*.py'))
        logger.info(f"Found {len(python_files)} Python files")
        
        for pyfile in python_files[:10]:  # Limit to first 10 for demo
            parsed = PythonCodeParser.parse_file(pyfile)
            if parsed:
                self.docs['code_docs'].append(parsed)
    
    def save_api_docs(self, output_path: str = "api_docs.json"):
        """Salva API docs em JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.docs['api_spec'], f, indent=2)
        logger.info(f"API docs saved to {output_path}")
    
    def save_changelog(self, output_path: str = "CHANGELOG.md"):
        """Salva changelog em Markdown"""
        with open(output_path, 'w') as f:
            f.write(self.docs['changelog'])
        logger.info(f"Changelog saved to {output_path}")
    
    def save_code_docs(self, output_dir: str = "docs"):
        """Salva documentação de código"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Gerar README
        readme = "# Code Documentation - Sprint 3\n\n"
        readme += f"Generated: {self.docs['generated_at']}\n\n"
        
        for doc in self.docs['code_docs']:
            readme += f"## {Path(doc['file']).name}\n"
            if doc.get('module_docstring'):
                readme += f"{doc['module_docstring']}\n\n"
            
            # Classes
            for cls in doc.get('classes', []):
                readme += f"### Class: {cls.name}\n"
                if cls.docstring:
                    readme += f"{cls.docstring}\n\n"
        
        readme_path = os.path.join(output_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(readme)
        
        logger.info(f"Code docs saved to {output_dir}/")
    
    def generate_metrics_summary(self) -> Dict[str, Any]:
        """Gera sumário de métricas da documentação"""
        api_paths = len(self.docs['api_spec'].get('paths', {}))
        python_files = len(self.docs['code_docs'])
        total_classes = sum(
            len(doc.get('classes', [])) for doc in self.docs['code_docs']
        )
        total_functions = sum(
            len(doc.get('functions', [])) for doc in self.docs['code_docs']
        )
        
        return {
            'api_endpoints': api_paths,
            'python_modules': python_files,
            'classes_documented': total_classes,
            'functions_documented': total_functions,
            'generated_at': self.docs['generated_at']
        }


# ============================================================================
# PARTE 6: Main
# ============================================================================

def main():
    """Executa geração de documentação"""
    logger.info("=" * 80)
    logger.info("Sprint 3 OPT5 - Documentação Viva")
    logger.info("=" * 80)
    
    # Inicializar pipeline
    pipeline = DocumentationPipeline(repo_path=".")
    
    # Gerar toda documentação
    docs = pipeline.generate_all()
    
    # Salvar outputs
    pipeline.save_api_docs("docs/api_openapi.json")
    pipeline.save_changelog("CHANGELOG_AUTO.md")
    pipeline.save_code_docs("docs/auto_generated")
    
    # Mostrar sumário
    summary = pipeline.generate_metrics_summary()
    logger.info("=" * 80)
    logger.info("Documentation Generation Summary:")
    logger.info("=" * 80)
    for key, value in summary.items():
        logger.info(f"{key}: {value}")
    
    logger.info("=" * 80)
    logger.info("Documentation generation complete!")
    logger.info("=" * 80)
    
    return docs


if __name__ == '__main__':
    main()
