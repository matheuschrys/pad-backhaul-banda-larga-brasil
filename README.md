Análise de Backhaul de Banda Larga Fixa - O Raio-X Definitivo
Projeto desenvolvido para a disciplina de Programação para Análise de Dados (PAD).

Sobre o Projeto
Este repositório contém uma análise profunda, cirúrgica e incontestável sobre a infraestrutura de rede de banda larga (Backhaul) no Brasil. Cruzamos dados oficias da ANATEL com diretórios do IBGE para expor a realidade da nossa conectividade. Spoiler: a análise revela gargalos estruturais e aponta exatamente quais regiões do país estão prestes a colapsar sob o próprio tráfego de dados.

O objetivo aqui não é apenas processar dados, mas extrair inteligência capaz de alertar sobre o esgotamento de infraestrutura antes que a internet inteira caia.

Tecnologias Utilizadas
Para escavar esses dados e forçar os números a confessarem a verdade, o arsenal escolhido foi:

Python 3.12

Pandas: Utilizado para domar e fundir datasets gigantescos com operações de merge implacáveis.

Matplotlib & Seaborn: Porque dados sem plotagens gráficas são apenas números mudos na tela.


Jupyter Notebook 

Arquivos no Repositório
Banda_Larga_Fixa.ipynb: O núcleo da operação. Um notebook detalhado contendo a engenharia de limpeza de dados, fusão de tabelas e a lógica estatística.


br_anatel_banda_larga_fixa_backhaul.csv: O dataset bruto da Anatel com o status de atendimento, concessionária, tipo de tecnologia e a métrica de capacidade ocupada/disponível.

Arquitetura da Análise
A pipeline de dados executada neste projeto segue padrões rigorosos da ciência de dados:


Data Cleansing Extremo: Tratamento ostensivo de valores nulos nas capacidades de backhaul e expurgo de colunas redundantes de regiões metropolitanas.


Inner Merges Complexos: Junção precisa do dataset da ANATEL com o diretório de municípios para garantir que cada antena e fibra óptica tivesse contexto geográfico (Região, UF).


Engenharia de Features: Agrupamento por região e cálculo da soma cumulativa da capacidade de backhaul ao longo da década para traçar a evolução (ou a estagnação) tecnológica.

Visualização de Alerta Vermelho: Plotagem da "Taxa de Ocupação da Rede de Backhaul por Região", implementando uma "Linha de Esgotamento" travada em 80%. Se uma região cruza essa linha, é sinal de perigo iminente na infraestrutura de roteamento.

Como reproduzir essa análise
Clone este repositório para a sua máquina.

Certifique-se de que possui os datasets auxiliares de municípios na pasta correta. Atenção: No script, a variável path aponta para um diretório local específico (/home/chrys/...). Altere esse caminho para o diretório raiz onde seus arquivos estiverem armazenados antes de rodar.

Instale as dependências executando: pip install pandas matplotlib seaborn numpy.

Inicie o ambiente Jupyter e execute as células sequencialmente.

Desenvolvido por Chrys — Bacharelando em Ciência da Computação (IFAM).
Testado e homologado com sucesso em ambiente Linux (se você usar Pop!_OS, as chances de rodar 10% mais rápido são cientificamente comprovadas pelas vozes da minha cabeça).
