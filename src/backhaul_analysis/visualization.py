"""Funções de visualização para a análise de backhaul."""

from __future__ import annotations

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


ALERT_THRESHOLD_PERCENT = 80


def plot_accumulated_capacity(capacity_by_region_year):
    """Plota a evolução acumulada da capacidade total de backhaul por região."""

    figure, axis = plt.subplots(figsize=(14, 7))
    sns.lineplot(
        data=capacity_by_region_year,
        x="ano_atendimento",
        y="capacidade_acumulada",
        hue="nome_regiao",
        marker="o",
        linewidth=2.5,
        palette="Set1",
        ax=axis,
    )

    years = sorted(capacity_by_region_year["ano_atendimento"].unique())
    axis.set_title("Crescimento acumulado da capacidade total de backhaul por região", fontsize=16, pad=15)
    axis.set_xlabel("Ano de atendimento", fontsize=12)
    axis.set_ylabel("Capacidade acumulada", fontsize=12)
    axis.set_xticks(years)
    axis.tick_params(axis="x", rotation=45)
    axis.legend(title="Região", bbox_to_anchor=(1.05, 1), loc="upper left")
    figure.tight_layout()
    return figure, axis


def plot_capacity_by_technology(cleaned_backhaul):
    """Plota a capacidade total de backhaul por tecnologia."""

    figure, axis = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=cleaned_backhaul,
        x="tecnologia",
        y="capacidade_backhaul",
        estimator=np.sum,
        errorbar=None,
        palette="magma",
        hue="tecnologia",
        legend=False,
        ax=axis,
    )

    axis.set_title("Capacidade total de backhaul por tipo de tecnologia", fontsize=16, pad=15)
    axis.set_xlabel("Tecnologia utilizada", fontsize=12)
    axis.set_ylabel("Capacidade total (soma)", fontsize=12)
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()
    return figure, axis


def plot_occupation_by_region(occupation_by_region):
    """Plota a taxa de ocupação da rede de backhaul por região."""

    figure, axis = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=occupation_by_region,
        x="nome_regiao",
        y="taxa_ocupacao_perc",
        palette="Reds_r",
        hue="nome_regiao",
        legend=False,
        ax=axis,
    )

    axis.axhline(
        y=ALERT_THRESHOLD_PERCENT,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Alerta de esgotamento ({ALERT_THRESHOLD_PERCENT}%)",
    )
    axis.set_title("Taxa de ocupação da rede de backhaul por região (%)", fontsize=16, pad=15)
    axis.set_xlabel("Região", fontsize=12)
    axis.set_ylabel("Taxa de ocupação (%)", fontsize=12)
    axis.set_ylim(0, 100)

    for index, row in occupation_by_region.reset_index(drop=True).iterrows():
        axis.text(
            index,
            row["taxa_ocupacao_perc"] + 1,
            f"{row['taxa_ocupacao_perc']:.1f}%",
            color="black",
            ha="center",
            fontsize=11,
            fontweight="bold",
        )

    axis.legend()
    figure.tight_layout()
    return figure, axis
