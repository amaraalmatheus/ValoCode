# 🎯 VALOCOACH

> **Os dados mostram o que aconteceu. O VALOCOACH mostra onde investigar e o que pode ser melhorado.**

Coach de análise **pós-partida** para VALORANT, desenvolvido para o **Hackathon SEMCOMP/VALORANT**.
O VALOCOACH lê os JSONs de partidas fornecidos pela organização, detecta padrões de um time e entrega **diagnósticos com evidência**, em vez de uma parede de gráficos.

```
JSON → métricas → detecção de padrões → diagnóstico → evidência → ponto de atenção
```

---

## 📌 Sumário

- [Visão geral](#-visão-geral)
- [Status do projeto](#-status-do-projeto)
- [Funcionalidades](#-funcionalidades)
- [Os 5 diagnósticos do MVP](#-os-5-diagnósticos-do-mvp)
- [Rigor estatístico](#-rigor-estatístico)
- [Como rodar](#-como-rodar)
- [Pipeline de dados](#-pipeline-de-dados)
- [Média da base e viabilidade](#-média-da-base-e-viabilidade)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Dados](#-dados)
- [Conformidade com o edital](#-conformidade-com-o-edital)
- [Equipe](#-equipe)
- [Licença](#-licença)

---

## 🔎 Visão geral

O usuário escolhe um time e recebe um relatório com os **3 a 5 achados mais importantes**, cada um com:

| Elemento | Descrição |
|---|---|
| **Problema detectado** | A frase curta do diagnóstico |
| **Evidência** | O número que sustenta, comparado com a média de todos os times da base |
| **Contexto** | Onde o padrão é mais forte (mapa, lado, tipo de round) |
| **Ponto de atenção** | O que investigar, sem afirmar a causa |

**Exemplo de card:**

> **Problema detectado:** Baixa recuperação após perder o pistol no ataque.
> **Evidência:** 38% de vitórias nos rounds seguintes quando perde o pistol.
> **Contexto:** O padrão é mais forte no Mapa X.
> **Ponto de atenção:** Investigar as decisões econômicas e a execução dos rounds de recuperação.

## 🚧 Status do projeto

| Frente | Situação |
|---|---|
| Dados: carga, limpeza e padronização dos JSONs | ✅ Pronto (`valocoach.pipeline`) |
| Dados: média da base e inventário de viabilidade | ✅ Pronto (`valocoach.baseline`) |
| Economia e os 5 diagnósticos | 🔄 Em andamento |
| Mapas de calor | 🔄 Em andamento |
| Interface (diagnóstico, drill-down, modos, PDF) | 🔄 Em andamento |
| Pitch (roteiro, slides, vídeo) | ⏳ A fazer |

## ✨ Funcionalidades

- **Diagnóstico** (tela principal): cards ordenados por prioridade (impacto × confiança).
- **Economy Lab**: pistol, eco, force buy, full buy, conversão após o pistol e recuperação após rounds perdidos.
- **Tactical Map**: mapas de calor de kills, mortes e plants por mapa e por lado, usados como evidência dos diagnósticos.
- **Drill-down**: do diagnóstico até os rounds e partidas que o sustentam.
- **Dois modos, um motor**: *Meu time* (o que melhorar) e *Adversário* (onde explorar).
- **Relatório de 1 página em PDF** para levar à reunião técnica.
- *(Se sobrar tempo)* Jogadores (first bloods, trades, clutches, multikills) e evolução entre as classificatórias 1 a 4.

## 🧪 Os 5 diagnósticos do MVP

| # | Diagnóstico | Pergunta que responde |
|---|---|---|
| 1 | Recuperação após perder o pistol | O time se recupera depois de perder o pistol, e em que lado? |
| 2 | Ataque vs. defesa por mapa | Em quais mapas o rendimento muda muito entre os lados? |
| 3 | Conversão após ganhar o pistol | O time converte a vantagem ou a desperdiça? |
| 4 | Force buy sem resultado | Quando o time força a compra e não ganha o round? |
| 5 | Dependência de um jogador | Os first bloods estão concentrados em uma só pessoa? |

> A viabilidade de cada um, com o número de times que passam da amostra mínima, está em [`docs/inventario_viabilidade.md`](docs/inventario_viabilidade.md).

## 📐 Rigor estatístico

- **Amostra mínima:** um diagnóstico só aparece com volume suficiente de rounds (padrão: 15, constante `MIN_AMOSTRA` em `baseline.py`).
- **Baseline da liga:** todo número é comparado com a média de todos os times da base (`data/processed/baseline_liga.csv`).
- **Ranking por prioridade:** score de impacto × confiança.
- **Linguagem honesta:** usamos "investigar" e "ponto de atenção", nunca "o motivo é X". Os dados não provam causa.
- **Rounds com resultado vazio:** tratados e contabilizados (ver [Pipeline de dados](#-pipeline-de-dados)). Nada é descartado em silêncio.
- **First bloods:** a concentração em um jogador é comparada com o esperado por acaso, não com 20%, porque o maior de 5 jogadores sempre passa disso.

## 🚀 Como rodar

**Pré-requisitos:** Python 3.10+ (testado em 3.12 e 3.15) e Git.

```bash
# 1. Clonar
git clone https://github.com/amaraalmatheus/ValoCode.git
cd ValoCode

# 2. Ambiente virtual
python -m venv .venv
source .venv/Scripts/activate    # Git Bash (Windows)
# source .venv/bin/activate      # Mac / Linux
# .venv\Scripts\activate         # Prompt de Comando (Windows)

# 3. Instalar o projeto (instala o pandas e deixa `import valocoach` disponível)
python -m pip install -e .

# 4. Colocar os JSONs da organização em data/raw/ (as pastas dos campeonatos direto lá dentro)

# 5. Gerar os dados limpos e a média da base
python -m valocoach.pipeline
python -m valocoach.baseline
```

Para a interface e os gráficos (quando a equipe for usá-los):

```bash
python -m pip install -r requirements.txt
streamlit run app/main.py        # em desenvolvimento
```

> Se alguma biblioteca do `requirements.txt` não instalar no Python 3.15, use o Python 3.12 (`py -3.12 -m venv .venv`).
> Sempre que abrir um terminal novo, ative o ambiente (passo 2) antes de usar o projeto.

**Testes:** `python -m pip install pytest` e depois `python -m pytest -q`.

## 🔧 Pipeline de dados

Ninguém na equipe precisa interpretar os JSONs brutos. O pipeline lê todos eles, padroniza a estrutura, identifica campos ausentes, trata rounds com resultado vazio e grava tabelas limpas em `data/processed/`:

```bash
python -m valocoach.pipeline --raw data/raw --out data/processed
```

Em qualquer módulo do projeto:

```python
from valocoach.loader import load_clean

T = load_clean()   # dict de DataFrames
T["rounds"]        # uma linha por round e por time (lado, vitória, economia, pistol)
T["kills"]         # uma linha por kill (times, coordenadas, first blood)
```

| Tabela | Conteúdo |
|---|---|
| `matches` | 1 linha por partida: times, placar, mapa, campeonato, fase, classificatória |
| `players` | 1 linha por jogador e partida (sem observadores) |
| `rounds` | 1 linha por round e time: lado, vitória, resultado, economia, plant |
| `player_rounds` | 1 linha por jogador e round: loadout, kills, dano, first blood |
| `kills` | 1 linha por kill: coordenadas, tipo de dano, first blood |

Todas as colunas estão explicadas em [`docs/dicionario_de_dados.md`](docs/dicionario_de_dados.md).

**O que o pipeline trata** (detalhes no relatório [`docs/relatorio_qualidade_dados.md`](docs/relatorio_qualidade_dados.md)):

- **Nome do time:** só existe no nome do arquivo; o pipeline o extrai e liga ao lado Red/Blue pelo placar. Para agrupar nomes (ex.: sub-times da mesma instituição), edite `data/team_aliases.csv` e rode o pipeline de novo.
- **Rounds com resultado vazio:** os rounds por tempo esgotado vêm com `roundResultCode` vazio. São mantidos como `tempo_esgotado`, com a flag `codigo_resultado_vazio`. Um round sem nenhum resultado utilizável é descartado e registrado.
- **Observadores:** removidos da tabela de jogadores.
- **Incoerências:** plant em round encerrado por tempo, placar que não bate etc. são sinalizados em `issues.csv` e a partida fica marcada como `atencao`.
- **Auditoria:** todo problema encontrado vira uma linha em `data/processed/issues.csv`, com a ação tomada.

## 📊 Média da base e viabilidade

```bash
python -m valocoach.baseline            # padrão: corte 15, 2 rounds após o pistol
python -m valocoach.baseline --min 20 --apos-pistol 3
```

Gera `data/processed/baseline_liga.csv` (taxa de vitória da liga por situação, mapa e lado, com média e desvio entre os times), `viabilidade_times.csv` (amostra de cada time em cada diagnóstico) e atualiza [`docs/inventario_viabilidade.md`](docs/inventario_viabilidade.md).

Duas decisões de análise ficam em constantes no topo de `src/valocoach/baseline.py`: `MIN_AMOSTRA` e `N_APOS_PISTOL` (quantos rounds depois do pistol contam como recuperação ou conversão).

## 📁 Estrutura do repositório

```
ValoCode/
├── app/                        # Interface (Streamlit)
├── src/valocoach/
│   ├── pipeline.py             # JSONs brutos → tabelas limpas + relatório de qualidade
│   ├── loader.py               # load_clean(): lê as tabelas limpas
│   ├── baseline.py             # média da base + inventário de viabilidade
│   ├── diagnostics/            # Os 5 diagnósticos + ranking de prioridade
│   ├── metrics.py
│   ├── maps.py                 # Mapas de calor
│   └── report.py               # Relatório de 1 página em PDF
├── data/
│   ├── raw/                    # JSONs da organização (NÃO versionados)
│   ├── processed/              # Tabelas geradas (NÃO versionadas)
│   └── team_aliases.csv        # Agrupamento de nomes de time (versionado)
├── docs/
│   ├── dicionario_de_dados.md
│   ├── inventario_viabilidade.md
│   └── relatorio_qualidade_dados.md
├── reports/                    # PDFs gerados
├── tests/
├── pyproject.toml
├── requirements.txt
├── THIRD_PARTY.md
└── README.md
```

## 🗂️ Dados

- Usamos **exclusivamente** os JSONs fornecidos pela organização do hackathon.
- Os arquivos **não são versionados** neste repositório (`data/raw/` e `data/processed/` estão no `.gitignore`).
- A base atual tem **336 partidas**, **6.618 rounds**, **46.753 kills** e **68 nomes de time**, de 8 campeonatos e fases (Rush Series e Univavá).
- Agentes e armas vêm como ID; o uso de uma tabela de nomes depende de confirmação da organização.

## ✅ Conformidade com o edital

- ✔️ Somente dados dos JSONs da organização (sem scraping, sem APIs externas).
- ✔️ 100% **pós-partida**: nada interfere em partida em andamento nem dá vantagem em tempo real.
- ✔️ Sem interação com serviços da Riot ou com o cliente do jogo.
- ✔️ Bibliotecas, imagens e fontes usadas respeitam suas licenças (ver [`THIRD_PARTY.md`](THIRD_PARTY.md)).

## 👥 Equipe

| Nome | Frente |
|---|---|
| Matheus ([@amaraalmatheus](https://github.com/amaraalmatheus)) | Dados |
| @Nicoli | _preencher_ |
| _nome_ | Economia e diagnósticos |
| _nome_ | Mapas |
| _nome_ | Interface |
| _nome_ | Pitch |

**Hackathon SEMCOMP/VALORANT · 2026**

## 📄 Licença

Definir com a equipe (sugestão: MIT). Dados de partida pertencem à organização do hackathon.

---

*VALOCOACH não é endossado pela Riot Games e não reflete as opiniões da Riot Games ou de qualquer pessoa oficialmente envolvida na produção ou gestão de propriedades da Riot Games. VALORANT é marca registrada da Riot Games, Inc.*
