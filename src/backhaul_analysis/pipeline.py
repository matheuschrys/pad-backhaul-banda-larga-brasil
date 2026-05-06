"""Pipeline de carga, limpeza e agregação dos dados de backhaul."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
EXTERNAL_DATA_DIR = DATA_DIR / "external"


@dataclass(frozen=True)
class AnalysisPaths:
    """Caminhos utilizados na análise.

    Os diretórios `data/raw` e `data/external` deixam explícita a origem dos
    arquivos: o CSV da Anatel versionado no repositório fica em `raw`, enquanto
    bases auxiliares baixadas separadamente ficam em `external`.
    """

    backhaul: Path = RAW_DATA_DIR / "br_anatel_banda_larga_fixa_backhaul.csv"
    municipios: Path = EXTERNAL_DATA_DIR / "br_bd_diretorios_brasil_municipio.csv"


CAPACITY_COLUMNS = [
    "capacidade_backhaul",
    "capacidade_ocupada",
    "capacidade_disponivel",
]
COLUMNS_TO_DROP = ["nome_regiao_metropolitana", "id_regiao_metropolitana"]
REQUIRED_BACKHAUL_COLUMNS = [
    "id_municipio",
    "situacao",
    "ano_atendimento",
    "concessionaria",
    "tecnologia",
    *CAPACITY_COLUMNS,
]
REQUIRED_MUNICIPALITY_COLUMNS = ["id_municipio", "nome_uf", "nome_regiao"]


def _read_csv(path: Path) -> pd.DataFrame:
    """Lê um CSV validando a existência do arquivo."""

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}. "
            "Confira o README para posicionar as bases em data/raw ou data/external."
        )

    return pd.read_csv(path)


def _validate_columns(dataframe: pd.DataFrame, required_columns: list[str], dataset_name: str) -> None:
    """Garante que as colunas necessárias existam antes de seguir no pipeline."""

    missing_columns = sorted(set(required_columns) - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Colunas ausentes em {dataset_name}: {missing}")


def load_backhaul_data(path: Path | None = None) -> pd.DataFrame:
    """Carrega a base de backhaul da Anatel."""

    backhaul_path = path or AnalysisPaths().backhaul
    backhaul = _read_csv(backhaul_path)
    _validate_columns(backhaul, REQUIRED_BACKHAUL_COLUMNS, "backhaul")
    return backhaul


def load_complete_dataset(paths: AnalysisPaths | None = None) -> pd.DataFrame:
    """Carrega e cruza a base da Anatel com o diretório de municípios."""

    analysis_paths = paths or AnalysisPaths()
    backhaul = load_backhaul_data(analysis_paths.backhaul)
    municipalities = _read_csv(analysis_paths.municipios)
    _validate_columns(municipalities, REQUIRED_MUNICIPALITY_COLUMNS, "municípios")

    return backhaul.merge(municipalities, how="inner", on="id_municipio")


def clean_backhaul_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Padroniza tipos, trata nulos e remove colunas redundantes."""

    cleaned = dataframe.copy()

    for column in CAPACITY_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").fillna(0)

    cleaned["ano_atendimento"] = pd.to_numeric(cleaned["ano_atendimento"], errors="coerce")
    cleaned = cleaned.dropna(subset=["ano_atendimento"])
    cleaned["ano_atendimento"] = cleaned["ano_atendimento"].astype(int)

    columns_to_drop = [column for column in COLUMNS_TO_DROP if column in cleaned.columns]
    return cleaned.drop(columns=columns_to_drop)


def aggregate_capacity_by_region_year(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Calcula a capacidade anual e acumulada por região."""

    grouped = (
        dataframe.groupby(["nome_regiao", "ano_atendimento"], as_index=False)["capacidade_backhaul"]
        .sum()
        .sort_values(by=["nome_regiao", "ano_atendimento"])
    )
    grouped["capacidade_acumulada"] = grouped.groupby("nome_regiao")["capacidade_backhaul"].cumsum()
    return grouped


def calculate_occupation_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Calcula a taxa percentual de ocupação de backhaul por região."""

    occupation = (
        dataframe.groupby("nome_regiao", as_index=False)[["capacidade_ocupada", "capacidade_backhaul"]]
        .sum()
        .sort_values("nome_regiao")
    )
    occupation["taxa_ocupacao_perc"] = (
        occupation["capacidade_ocupada"].div(occupation["capacidade_backhaul"]).fillna(0) * 100
    )
    return occupation
