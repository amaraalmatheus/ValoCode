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
- [Funcionalidades](#-funcionalidades)
- [Os 5 diagnósticos do MVP](#-os-5-diagnósticos-do-mvp)
- [Rigor estatístico](#-rigor-estatístico)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Como rodar](#-como-rodar)
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

> A lista é a proposta inicial e será ajustada ao que os JSONs realmente permitirem (ver `docs/inventario_viabilidade.md`).

## 📐 Rigor estatístico

- **Amostra mínima:** um diagnóstico só aparece com volume suficiente de rounds (valor inicial: 15, a confirmar após análise dos dados).
- **Baseline da liga:** todo número é comparado com a média de todos os times da base.
- **Ranking por prioridade:** score de impacto × confiança.
- **Linguagem honesta:** usamos "investigar" e "ponto de atenção", nunca "o motivo é X". Os dados não provam causa.
- **Rounds com resultado vazio:** tratamento documentado, com contagem de quantos foram descartados.

## 📁 Estrutura do repositório

```
valocoach/
├── app/                    # Interface (Streamlit)
├── src/valocoach/
│   ├── loader.py           # Carga e limpeza dos JSONs
│   ├── metrics.py          # Métricas e média da base
│   ├── diagnostics/        # Os 5 diagnósticos + ranking de prioridade
│   ├── maps.py             # Mapas de calor
│   └── report.py           # Relatório de 1 página em PDF
├── data/
│   ├── raw/                # JSONs da organização (NÃO versionados)
│   └── processed/          # Dados tratados (NÃO versionados)
├── docs/                   # Plano da equipe, inventário de viabilidade, decisões
├── reports/                # PDFs gerados
├── tests/
├── requirements.txt
└── README.md
```

## 🚀 Como rodar

**Pré-requisitos:** Python 3.10+ e Git.

```bash
# 1. Clonar
git clone https://github.com/<ORG-OU-USUARIO>/valocoach.git
cd valocoach

# 2. Ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Colocar os JSONs da organização em data/raw/

# 5. Executar
streamlit run app/main.py
```

## 🗂️ Dados

- Usamos **exclusivamente** os JSONs fornecidos pela organização do hackathon.
- Os arquivos **não são versionados** neste repositório (`data/raw/` está no `.gitignore`).
- O nome do time é extraído do nome do arquivo ao carregar.
- Agentes e armas vêm como ID; o uso de tabela de nomes depende de confirmação da organização.

## ✅ Conformidade com o edital

- ✔️ Somente dados dos JSONs da organização (sem scraping, sem APIs externas).
- ✔️ 100% **pós-partida**: nada interfere em partida em andamento nem dá vantagem em tempo real.
- ✔️ Sem interação com serviços da Riot ou com o cliente do jogo.
- ✔️ Bibliotecas, imagens e fontes usadas respeitam suas licenças (ver `THIRD_PARTY.md`).

## 👥 Equipe

| Nome | Frente |
|---|---|
| @Nicoli | _preencher_ |
| _nome_ | Dados |
| _nome_ | Economia e diagnósticos |
| _nome_ | Mapas |
| _nome_ | Interface |
| _nome_ | Pitch |

**Hackathon SEMCOMP/VALORANT · 2026**

## 📄 Licença

Definir com a equipe (sugestão: MIT). Dados de partida pertencem à organização do hackathon.

---

*VALOCOACH não é endossado pela Riot Games e não reflete as opiniões da Riot Games ou de qualquer pessoa oficialmente envolvida na produção ou gestão de propriedades da Riot Games. VALORANT é marca registrada da Riot Games, Inc.*
