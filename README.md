# Análise de backhaul de banda larga fixa no Brasil

Projeto desenvolvido para a disciplina de **Programação para Análise de Dados (PAD)**.

O objetivo é analisar a infraestrutura de backhaul de banda larga fixa no Brasil a partir de dados da Anatel, enriquecendo a base com diretórios geográficos para comparar capacidade, tecnologia e ocupação por região.

## Estrutura do projeto

```text
.
├── data/
│   ├── raw/                         # Dados brutos versionados no repositório
│   │   └── br_anatel_banda_larga_fixa_backhaul.csv
│   └── external/                    # Bases auxiliares baixadas separadamente
│       └── .gitkeep
├── notebooks/
│   └── backhaul_banda_larga_fixa.ipynb
├── src/
│   └── backhaul_analysis/
│       ├── __init__.py
│       ├── cli.py
│       ├── pipeline.py
│       └── visualization.py
├── requirements.txt
└── README.md
```

## O que mudou na organização

- O notebook foi movido para `notebooks/` e agora funciona como uma camada narrativa da análise.
- O CSV da Anatel foi movido para `data/raw/`, separando dados brutos de código e documentação.
- A lógica de carga, validação, limpeza e agregação foi extraída para `src/backhaul_analysis/pipeline.py`.
- A criação dos gráficos foi extraída para `src/backhaul_analysis/visualization.py`.
- Foi criada uma CLI simples em `src/backhaul_analysis/cli.py` para executar a análise fora do Jupyter.

## Bases de dados

### Base versionada

- `data/raw/br_anatel_banda_larga_fixa_backhaul.csv`: dados da Anatel com município, situação de atendimento, ano, concessionária, tecnologia e capacidades de backhaul.

### Base auxiliar necessária

Para reproduzir o notebook completo, baixe ou disponibilize o diretório de municípios no caminho abaixo:

```text
data/external/br_bd_diretorios_brasil_municipio.csv
```

A base auxiliar precisa conter, no mínimo, as colunas:

- `id_municipio`
- `nome_uf`
- `nome_regiao`

## Tecnologias utilizadas

- Python 3.12+
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Como reproduzir a análise

1. Clone o repositório.
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Coloque a base auxiliar de municípios em `data/external/br_bd_diretorios_brasil_municipio.csv`.
5. Execute o notebook:

   ```bash
   jupyter notebook notebooks/backhaul_banda_larga_fixa.ipynb
   ```

## Execução via linha de comando

Também é possível executar as agregações principais sem abrir o notebook:

```bash
PYTHONPATH=src python -m backhaul_analysis.cli
```

Se os arquivos estiverem em outros caminhos, informe-os explicitamente:

```bash
PYTHONPATH=src python -m backhaul_analysis.cli \
  --backhaul data/raw/br_anatel_banda_larga_fixa_backhaul.csv \
  --municipios data/external/br_bd_diretorios_brasil_municipio.csv
```

## Pipeline da análise

1. **Carga e validação**: leitura dos CSVs e verificação das colunas obrigatórias.
2. **Integração geográfica**: junção da base da Anatel com o diretório de municípios por `id_municipio`.
3. **Limpeza**: tratamento de capacidades nulas, conversão do ano de atendimento e remoção de colunas redundantes quando existirem.
4. **Agregação**: cálculo da capacidade anual, capacidade acumulada e taxa de ocupação por região.
5. **Visualização**: gráficos para evolução acumulada, capacidade por tecnologia e ocupação regional com linha de alerta em 80%.

## Autoria

Desenvolvido por Chrys — Bacharelando em Ciência da Computação (IFAM).
