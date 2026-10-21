# Inventário de viabilidade

Gerado por `python -m valocoach.baseline`. **68 times** na base. Amostra mínima: **15**. Rounds seguintes ao pistol: **2**.

Unidade da amostra: rounds (D1 a D4) e first bloods (D5). 'Times viáveis' = times com amostra ≥ corte no recorte indicado.

| # | Diagnóstico | Campos necessários | Dados sustentam? | Times viáveis (corte atual) | Observações |
|---|---|---|---|---|---|
| 1 | Recuperação após perder o pistol | `rounds`: pistol, venceu, lado, round | Sim | 35 geral · 12 ataque · 15 defesa | Amostra = 2 rounds por pistol perdido. O recorte por mapa fica ralo demais. |
| 2 | Ataque vs. defesa por mapa | `rounds`: lado, venceu; `matches`: mapa | Sim | 51 com ≥1 mapa viável | Corte vale por mapa **e** por lado. Média de 2.6 mapas viáveis por time (entre os viáveis). |
| 3 | Conversão após ganhar o pistol | `rounds`: pistol, venceu, lado, round | Sim | 33 geral · 13 ataque · 11 defesa | Mesma definição do D1, espelhada. |
| 4 | Force buy sem resultado | `rounds`: tipo_economia, venceu, lado | Sim, com ressalva | 49 geral · 29 ataque · 39 defesa | `tipo_economia` é **provisório** (cortes de loadout); validar com a frente de Economia. |
| 5 | Dependência de um jogador | `player_rounds`: first_blood, puuid, time | Sim | 60 | Compare com o **acaso** (abaixo), não com 20%: o maior de 5 sempre passa disso. |

## Sensibilidade ao corte de amostra

Quantos times sobram em cada recorte se o corte mudar. Ajuda a confirmar o número final.

| Diagnóstico / recorte | ≥10 | ≥15 | ≥20 | ≥30 |
|---|---|---|---|---|
| D1 recuperação | 48 | 35 | 26 | 16 |
| D1 recuperação · Attacker | 28 | 12 | 7 | 4 |
| D1 recuperação · Defender | 31 | 15 | 8 | 2 |
| D2 ataque vs defesa (≥1 mapa) | 58 | 51 | 47 | 33 |
| D3 conversão | 45 | 33 | 28 | 10 |
| D3 conversão · Attacker | 30 | 13 | 8 | 3 |
| D3 conversão · Defender | 29 | 11 | 8 | 5 |
| D4 force buy | 56 | 49 | 46 | 33 |
| D4 force buy · Attacker | 42 | 29 | 27 | 10 |
| D4 force buy · Defender | 45 | 39 | 25 | 12 |
| D5 first bloods | 63 | 60 | 59 | 54 |

## Média da base (referência para os cards)

Taxa de vitória agregada da liga (todos os rounds, ambos os lados). Tabela completa por mapa e lado em `data/processed/baseline_liga.csv`.

| Situação | Taxa da liga |
|---|---|
| Pistol, ataque | 50.9% |
| Pistol, defesa | 49.1% |
| Rounds de ataque (geral) | 51.8% |
| Rounds de defesa (geral) | 48.2% |
| Após perder o pistol (geral) | 37.1% |
| Após perder o pistol, ataque | 40.8% |
| Após perder o pistol, defesa | 33.4% |
| Após ganhar o pistol (geral) | 62.9% |
| Force buy (geral) | 44.9% |
| Force buy contra adversário full | 30.3% |
| Full buy (geral) | 56.6% |
| Eco (geral) | 15.7% |

### Concentração de first bloods (diagnóstico 5)

Fatia dos first bloods feitos pelo jogador que mais faz, em times com ≥15 first bloods: média da liga **34.4%**; esperado só por acaso **26.4%**; 75% dos times ficam abaixo de 38.2% e 90% abaixo de 44.8%. Um time só merece alerta bem acima desses valores.

## Decisões em aberto

- **Aliases de time** (`data/team_aliases.csv`): agrupar sub-times muda estes números.
- **Rounds após o pistol** (2): ajustar `N_APOS_PISTOL` em `baseline.py` e rodar de novo.
- **`tipo_economia`**: cortes provisórios em `pipeline.py` (afetam D4 e a tabela de economia).
