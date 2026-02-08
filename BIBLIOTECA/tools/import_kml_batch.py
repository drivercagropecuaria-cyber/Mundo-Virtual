#!/usr/bin/env python3
"""
Importação em Lote de Dados KML para PostgreSQL+PostGIS
========================================================

Importa dados geoespaciais de arquivos KML para PostgreSQL com PostGIS,
seguindo padrões de qualidade do projeto Mundo Virtual Villa Canabrava.

Dependências:
  pip install geopandas shapely sqlalchemy psycopg2-binary lxml

Autor: Roo | Projeto: Mundo Virtual Villa Canabrava
"""

import os
import json
import logging
import sys
import argparse
import zipfile
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import warnings
import xml.etree.ElementTree as ET

import geopandas as gpd
import pandas as pd
import fiona
from shapely.geometry import mapping, Point, LineString, Polygon, GeometryCollection
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

try:
    from fastkml import kml as fastkml
except ImportError:
    fastkml = None

# Suprimir avisos desnecessários
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Habilitar suporte KML no Fiona (se disponivel)
fiona.drvsupport.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# Setup de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mapeamento de camadas para categorias (conforme documento oficial)
LAYER_MAPPING = {
    'PIVO': {'category': 'Infraestrutura', 'subcategory': 'Irrigação'},
    'POCO': {'category': 'Infraestrutura', 'subcategory': 'Abastecimento'},
    'CERCA': {'category': 'Limite', 'subcategory': 'Divisão'},
    'MATA': {'category': 'Ambiental', 'subcategory': 'Mata Nativa'},
    'APP': {'category': 'Ambiental', 'subcategory': 'Preservação'},
    'RESERVA_LEGAL': {'category': 'Ambiental', 'subcategory': 'Reserva Legal'},
    'CASA_COLONO': {'category': 'Edificação', 'subcategory': 'Residencial'},
    'SEDE': {'category': 'Edificação', 'subcategory': 'Administrativo'},
    'PISTA_VAQUEIJADA': {'category': 'Lazer', 'subcategory': 'Eventos'},
    'CONFINAMENTO': {'category': 'Infraestrutura', 'subcategory': 'Produtiva'},
    'CURRAL': {'category': 'Infraestrutura', 'subcategory': 'Produtiva'},
    'SILO': {'category': 'Infraestrutura', 'subcategory': 'Armazenamento'},
    'FABRICA_RACAO': {'category': 'Infraestrutura', 'subcategory': 'Produtiva'},
    'BREJO': {'category': 'Ambiental', 'subcategory': 'Hídrico'},
    'LAGOA': {'category': 'Ambiental', 'subcategory': 'Hídrico'},
    'CORREGO': {'category': 'Ambiental', 'subcategory': 'Hídrico'},
    'ESTRADA': {'category': 'Transporte', 'subcategory': 'Rodoviário'},
    'FERROVIA': {'category': 'Transporte', 'subcategory': 'Ferroviário'},
    'AERODROMO': {'category': 'Transporte', 'subcategory': 'Aéreo'},
    'TALHAO': {'category': 'Produtiva', 'subcategory': 'Manejo'},
}

@dataclass
class ImportMetrics:
    """Métricas de importação"""
    file_name: str
    features_imported: int
    features_skipped: int
    total_area_ha: float
    errors: list
    status: str

class KMLImporter:
    """Importador de dados KML para PostgreSQL"""
    
    def __init__(self, db_url: str, schema_name: str = 'gis_data'):
        """
        Inicializa importador
        
        Args:
            db_url: String de conexão PostgreSQL (psycopg2://user:pass@host:port/db)
            schema_name: Nome do schema para dados GIS
        """
        self.db_url = db_url
        self.schema_name = schema_name
        self.engine = None
        self.metrics = []
        self._connect()
    
    def _connect(self) -> bool:
        """Conecta ao banco de dados e cria schema se necessário"""
        try:
            self.engine = create_engine(self.db_url, echo=False)
            with self.engine.connect() as conn:
                # Verificar conexão
                result = conn.execute(text("SELECT 1"))
                logger.info("✅ Conexão com PostgreSQL estabelecida")
                
                # Criar schema se não existir
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"))
                
                # Habilitar extensões PostGIS
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
                conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
                
                conn.commit()
                logger.info(f"✅ Schema '{self.schema_name}' e extensões criados")
                
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao conectar: {e}")
            return False

    def _read_kml_with_etree(self, kml_file: Path) -> gpd.GeoDataFrame:
        data = None
        if kml_file.suffix.lower() == '.kmz':
            with zipfile.ZipFile(kml_file, 'r') as zf:
                kml_names = [name for name in zf.namelist() if name.lower().endswith('.kml')]
                if not kml_names:
                    return gpd.GeoDataFrame(columns=['name', 'description', 'geometry'], geometry='geometry', crs='EPSG:4326')
                data = zf.read(kml_names[0])
        else:
            data = kml_file.read_bytes()

        root = ET.fromstring(data)
        ns_uri = root.tag.split('}')[0].strip('{') if '}' in root.tag else ''
        ns = {'k': ns_uri} if ns_uri else {}

        def find_text(node, path, default=''):
            if ns:
                return node.findtext(path, default=default, namespaces=ns)
            return node.findtext(path, default=default)

        def parse_coords(text):
            coords = []
            for part in text.strip().split():
                pieces = part.split(',')
                if len(pieces) < 2:
                    continue
                lon = float(pieces[0])
                lat = float(pieces[1])
                coords.append((lon, lat))
            return coords

        def extract_geoms(placemark):
            geoms = []
            point_nodes = placemark.findall('.//k:Point', ns) if ns else placemark.findall('.//Point')
            for pt in point_nodes:
                coord_text = find_text(pt, 'k:coordinates' if ns else 'coordinates')
                if coord_text:
                    coords = parse_coords(coord_text)
                    if coords:
                        geoms.append(Point(coords[0]))

            line_nodes = placemark.findall('.//k:LineString', ns) if ns else placemark.findall('.//LineString')
            for line in line_nodes:
                coord_text = find_text(line, 'k:coordinates' if ns else 'coordinates')
                if coord_text:
                    coords = parse_coords(coord_text)
                    if len(coords) >= 2:
                        geoms.append(LineString(coords))

            poly_nodes = placemark.findall('.//k:Polygon', ns) if ns else placemark.findall('.//Polygon')
            for poly in poly_nodes:
                outer = None
                outer_text = find_text(poly, './/k:outerBoundaryIs/k:LinearRing/k:coordinates' if ns else './/outerBoundaryIs/LinearRing/coordinates')
                if outer_text:
                    outer = parse_coords(outer_text)
                inner_coords = []
                inner_nodes = poly.findall('.//k:innerBoundaryIs/k:LinearRing/k:coordinates', ns) if ns else poly.findall('.//innerBoundaryIs/LinearRing/coordinates')
                for inner in inner_nodes:
                    if inner.text:
                        inner_coords.append(parse_coords(inner.text))
                if outer and len(outer) >= 3:
                    geoms.append(Polygon(outer, inner_coords if inner_coords else None))

            if not geoms:
                return None
            if len(geoms) == 1:
                return geoms[0]
            return GeometryCollection(geoms)

        placemarks = root.findall('.//k:Placemark', ns) if ns else root.findall('.//Placemark')
        features = []
        for pm in placemarks:
            geom = extract_geoms(pm)
            if geom is None:
                continue
            features.append({
                'name': find_text(pm, 'k:name' if ns else 'name', default='Unnamed') or 'Unnamed',
                'description': find_text(pm, 'k:description' if ns else 'description', default='') or '',
                'geometry': geom
            })

        if not features:
            return gpd.GeoDataFrame(columns=['name', 'description', 'geometry'], geometry='geometry', crs='EPSG:4326')

        return gpd.GeoDataFrame(features, geometry='geometry', crs='EPSG:4326')
    
    def _create_tables_if_needed(self) -> bool:
        """Cria tabelas necessárias se não existirem"""
        try:
            with self.engine.connect() as conn:
                # Tabela de camadas
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema_name}.layers (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        name VARCHAR(100) NOT NULL UNIQUE,
                        display_name VARCHAR(255),
                        description TEXT,
                        category VARCHAR(100),
                        style_config JSONB,
                        is_visible BOOLEAN DEFAULT true,
                        z_index INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """))
                
                # Tabela principal de features
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema_name}.features (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        name VARCHAR(255) NOT NULL,
                        category VARCHAR(100) NOT NULL,
                        subcategory VARCHAR(100),
                        layer_name VARCHAR(100) NOT NULL,
                        geometry GEOMETRY(GEOMETRY, 4326),
                        area_ha DECIMAL(10, 4),
                        perimeter_km DECIMAL(10, 4),
                        attributes JSONB,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW(),
                        source_kml VARCHAR(255),
                        CONSTRAINT fk_layer FOREIGN KEY (layer_name)
                            REFERENCES {self.schema_name}.layers(name)
                    )
                """))
                
                # Índices espaciais
                try:
                    conn.execute(text(f"""
                        CREATE INDEX IF NOT EXISTS idx_features_geometry 
                        ON {self.schema_name}.features USING GIST(geometry)
                    """))
                except:
                    pass
                
                try:
                    conn.execute(text(f"""
                        CREATE INDEX IF NOT EXISTS idx_features_category 
                        ON {self.schema_name}.features(category)
                    """))
                except:
                    pass
                
                try:
                    conn.execute(text(f"""
                        CREATE INDEX IF NOT EXISTS idx_features_name 
                        ON {self.schema_name}.features USING gin(name gin_trgm_ops)
                    """))
                except:
                    pass
                
                conn.commit()
                logger.info("✅ Tabelas criadas com sucesso")
                return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao criar tabelas: {e}")
            return False
    
    def _get_category_info(self, layer_name: str) -> Dict[str, str]:
        """Determina categoria e subcategoria para um layer"""
        layer_upper = layer_name.upper()
        
        for key, value in LAYER_MAPPING.items():
            if key in layer_upper:
                return value
        
        return {'category': 'Outros', 'subcategory': 'Geral'}
    
    def import_kml(self, kml_file: Path) -> ImportMetrics:
        """
        Importa um arquivo KML individual
        
        Returns:
            ImportMetrics com resultado da importação
        """
        metrics = ImportMetrics(
            file_name=kml_file.name,
            features_imported=0,
            features_skipped=0,
            total_area_ha=0,
            errors=[],
            status='PROCESSING'
        )
        
        try:
            logger.info(f"📖 Importando: {kml_file.name}")
            
            # Ler arquivo KML
            try:
                if kml_file.suffix.lower() == '.kmz':
                    gdf = self._read_kml_with_etree(kml_file)
                else:
                    driver = 'KML'
                    gdf = gpd.read_file(kml_file, driver=driver)
            except Exception as e:
                if 'unsupported driver' in str(e).lower():
                    try:
                        logger.warning("  ⚠️  Driver KML indisponivel, usando parser XML")
                        gdf = self._read_kml_with_etree(kml_file)
                    except Exception as fallback_error:
                        metrics.errors.append(f"Erro ao ler KML (fallback): {fallback_error}")
                        metrics.status = 'ERROR'
                        logger.error(f"  ❌ Erro ao ler KML (fallback): {fallback_error}")
                        return metrics
                else:
                    metrics.errors.append(f"Erro ao ler KML: {e}")
                    metrics.status = 'ERROR'
                    logger.error(f"  ❌ Erro ao ler KML: {e}")
                    return metrics
            
            if gdf.empty:
                metrics.status = 'SKIPPED'
                logger.warning(f"  ⚠️  Arquivo vazio")
                return metrics
            
            # Extrair nome da camada do nome do arquivo
            layer_name = kml_file.stem  # Nome sem extensão
            category_info = self._get_category_info(layer_name)
            
            # Preparar dados
            gdf = gdf.rename(columns={'Name': 'name', 'Description': 'description'})
            gdf['name'] = gdf.get('name', 'Unnamed')
            gdf['layer_name'] = layer_name
            gdf['category'] = category_info['category']
            gdf['subcategory'] = category_info['subcategory']
            gdf['source_kml'] = kml_file.name
            
            # Calcular área e perímetro
            gdf['area_ha'] = 0.0
            gdf['perimeter_km'] = 0.0
            
            for idx, row in gdf.iterrows():
                geom = row.geometry
                if geom.geom_type in ['Polygon', 'MultiPolygon']:
                    gdf.at[idx, 'area_ha'] = geom.area / 10000
                    gdf.at[idx, 'perimeter_km'] = geom.length / 1000
                elif geom.geom_type == 'LineString':
                    gdf.at[idx, 'perimeter_km'] = geom.length / 1000
            
            # Converter atributos para JSONB
            columns_to_exclude = ['geometry', 'layer_name', 'category', 'subcategory',
                                 'area_ha', 'perimeter_km', 'name', 'description', 'source_kml']
            attribute_columns = [col for col in gdf.columns if col not in columns_to_exclude]
            
            def make_attributes(row):
                attrs = {}
                for col in attribute_columns:
                    val = row[col]
                    if pd.notna(val):
                        attrs[col] = str(val)
                return json.dumps(attrs) if attrs else '{}'
            
            gdf['attributes'] = gdf.apply(make_attributes, axis=1)
            
            # Selecionar colunas finais
            final_columns = ['name', 'category', 'subcategory', 'layer_name', 'geometry',
                           'area_ha', 'perimeter_km', 'attributes', 'source_kml']
            gdf = gdf[final_columns]
            
            # Importar para PostgreSQL
            with self.engine.connect() as conn:
                # Registrar ou atualizar layer
                try:
                    conn.execute(text(f"""
                        INSERT INTO {self.schema_name}.layers (name, display_name, category)
                        VALUES (:name, :display, :category)
                        ON CONFLICT (name) DO NOTHING
                    """), {
                        'name': layer_name,
                        'display': layer_name.replace('_', ' '),
                        'category': category_info['category']
                    })
                except:
                    pass
                
                # Importar features
                error_count = 0
                for idx, row in gdf.iterrows():
                    try:
                        geom_wkt = row.geometry.wkt
                        
                        conn.execute(text(f"""
                            INSERT INTO {self.schema_name}.features 
                            (name, category, subcategory, layer_name, geometry, 
                             area_ha, perimeter_km, attributes, source_kml)
                            VALUES (
                                :name, :category, :subcategory, :layer_name,
                                ST_Force2D(ST_GeomFromText(:geom, 4326)),
                                :area_ha, :perimeter_km, CAST(:attributes AS jsonb), :source_kml
                            )
                        """), {
                            'name': row['name'],
                            'category': row['category'],
                            'subcategory': row['subcategory'],
                            'layer_name': row['layer_name'],
                            'geom': geom_wkt,
                            'area_ha': float(row['area_ha']),
                            'perimeter_km': float(row['perimeter_km']),
                            'attributes': row['attributes'],
                            'source_kml': row['source_kml']
                        })
                        
                        metrics.features_imported += 1
                        metrics.total_area_ha += float(row['area_ha'])
                    
                    except Exception as e:
                        error_count += 1
                        metrics.features_skipped += 1
                        metrics.errors.append(f"Feature '{row['name']}': {str(e)}")
                        if error_count <= 3:
                            logger.error(
                                f"  ❌ Falha ao inserir feature '{row['name']}' ({kml_file.name}): {e}"
                            )
                
                conn.commit()
            
            metrics.status = 'SUCCESS'
            logger.info(f"  ✅ {metrics.features_imported} features importados ({metrics.total_area_ha:.2f} ha)")
            
        except Exception as e:
            metrics.status = 'ERROR'
            metrics.errors.append(str(e))
            logger.error(f"  ❌ Erro geral: {e}")
        
        return metrics
    
    def import_batch(self, kml_directory: Path) -> Dict:
        """
        Importa todos os KML de um diretório
        
        Returns:
            Dicionário com resumo da importação
        """
        kml_files = list(kml_directory.glob('**/*.kml')) + list(kml_directory.glob('**/*.kmz'))
        
        if not kml_files:
            logger.error(f"❌ Nenhum arquivo KML encontrado em {kml_directory}")
            return {}
        
        logger.info(f"🚀 Iniciando importação em lote de {len(kml_files)} arquivos...")
        logger.info("-" * 80)
        
        # Criar tabelas
        if not self._create_tables_if_needed():
            return {}
        
        summary = {
            'total_files': len(kml_files),
            'successful': 0,
            'skipped': 0,
            'failed': 0,
            'total_features': 0,
            'total_area_ha': 0.0,
            'files': []
        }
        
        for i, kml_file in enumerate(sorted(kml_files), 1):
            metrics = self.import_kml(kml_file)
            self.metrics.append(metrics)
            
            summary['files'].append({
                'name': metrics.file_name,
                'status': metrics.status,
                'features': metrics.features_imported
            })
            
            if metrics.status == 'SUCCESS':
                summary['successful'] += 1
                summary['total_features'] += metrics.features_imported
                summary['total_area_ha'] += metrics.total_area_ha
            elif metrics.status == 'SKIPPED':
                summary['skipped'] += 1
            else:
                summary['failed'] += 1
        
        logger.info("-" * 80)
        logger.info(f"\n📊 RESUMO DA IMPORTAÇÃO:")
        logger.info(f"  ✅ Sucesso:     {summary['successful']:3d}")
        logger.info(f"  ⏭️  Pulados:      {summary['skipped']:3d}")
        logger.info(f"  ❌ Falhas:       {summary['failed']:3d}")
        logger.info(f"  📦 Total:       {summary['total_files']:3d}")
        logger.info(f"  🌍 Features:    {summary['total_features']:,d}")
        logger.info(f"  📏 Área total:  {summary['total_area_ha']:,.2f} ha")
        
        return summary


def main():
    """Ponto de entrada principal"""

    def build_db_url() -> str:
        env_url = os.getenv("DB_URL")
        if env_url:
            return env_url
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "biblioteca")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"

    parser = argparse.ArgumentParser(
        description="Importacao em lote de KML para PostgreSQL/PostGIS"
    )
    parser.add_argument(
        "--kml-dir",
        default=os.getenv("KML_DIR", r"C:\Users\rober\Downloads\KML\KML"),
        help="Diretorio com arquivos KML/KMZ"
    )
    parser.add_argument(
        "--db-url",
        default=build_db_url(),
        help="URL de conexao PostgreSQL"
    )
    parser.add_argument(
        "--schema",
        default=os.getenv("KML_SCHEMA", "gis_data"),
        help="Schema de destino"
    )
    parser.add_argument(
        "--summary-out",
        default=os.getenv("KML_SUMMARY_OUT", ""),
        help="Caminho para salvar resumo JSON"
    )

    args = parser.parse_args()

    kml_dir = Path(args.kml_dir)
    if not kml_dir.exists():
        logger.error(f"❌ Diretório KML não encontrado: {kml_dir}")
        sys.exit(1)

    # Executar importação
    importer = KMLImporter(args.db_url, schema_name=args.schema)
    summary = importer.import_batch(kml_dir)

    # Salvar resumo em JSON
    output_file = Path(args.summary_out) if args.summary_out else \
        Path(__file__).parent.parent / "reports" / "KML_IMPORT_SUMMARY.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✅ Resumo salvo em: {output_file}")


if __name__ == '__main__':
    main()
