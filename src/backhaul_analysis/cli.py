"""Interface de linha de comando para executar a análise fora do notebook."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import (
    AnalysisPaths,
    aggregate_capacity_by_region_year,
    calculate_occupation_by_region,
    clean_backhaul_data,
    load_complete_dataset,
)


def parse_args() -> argparse.Namespace:
    """Processa argumentos da CLI."""

    parser = argparse.ArgumentParser(description="Executa a análise de backhaul de banda larga fixa.")
    parser.add_argument("--backhaul", type=Path, default=AnalysisPaths().backhaul, help="CSV de backhaul da Anatel.")
    parser.add_argument(
        "--municipios",
        type=Path,
        default=AnalysisPaths().municipios,
        help="CSV do diretório de municípios do Brasil.",
    )
    return parser.parse_args()


def main() -> None:
    """Executa carga, limpeza e agregações principais."""

    args = parse_args()
    paths = AnalysisPaths(backhaul=args.backhaul, municipios=args.municipios)
    complete = load_complete_dataset(paths)
    cleaned = clean_backhaul_data(complete)
    capacity_by_region_year = aggregate_capacity_by_region_year(cleaned)
    occupation_by_region = calculate_occupation_by_region(cleaned)

    print("Resumo da capacidade acumulada por região/ano:")
    print(capacity_by_region_year.to_string(index=False))
    print("\nTaxa de ocupação por região:")
    print(occupation_by_region.to_string(index=False))


if __name__ == "__main__":
    main()
