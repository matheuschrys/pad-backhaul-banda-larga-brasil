"""Ferramentas para analisar backhaul de banda larga fixa no Brasil."""

from .pipeline import (
    AnalysisPaths,
    aggregate_capacity_by_region_year,
    calculate_occupation_by_region,
    clean_backhaul_data,
    load_backhaul_data,
    load_complete_dataset,
)

__all__ = [
    "AnalysisPaths",
    "aggregate_capacity_by_region_year",
    "calculate_occupation_by_region",
    "clean_backhaul_data",
    "load_backhaul_data",
    "load_complete_dataset",
]
