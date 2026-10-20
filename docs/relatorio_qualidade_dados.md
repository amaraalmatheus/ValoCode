# Relatório de qualidade dos dados

## Resumo

| Item | Valor |
|---|---|
| arquivos lidos | 336 |
| arquivos descartados | 0 |
| partidas | 336 |
| partidas com atencao | 9 |
| rounds | 6618 |
| kills | 46753 |
| times | 68 |
| observadores removidos | 22 |
| rounds codigo vazio | 150 |
| aliases aplicados | 68 |

## Checagens de integridade

- ✅ Cada round tem 2 linhas e exatamente 1 vencedor (6618 rounds)
- ✅ Cada round tem 1 atacante e 1 defensor
- ✅ match_id único (336 partidas)
- ✅ 10 jogadores por partida (sem observadores) (0 partidas fora do padrão)
- ✅ Todo killer/victim está em players (46753 kills)
- ✅ Rounds vencidos batem com o placar (336/336 partidas)

## Problemas encontrados e tratamento

| Severidade | Campo | Ação | Ocorrências |
|---|---|---|---|
| info | `roundResultCode` | resultado_derivado_do_texto | 150 |
| info | `victim` | mantido | 59 |
| info | `isObserver` | removido_de_players | 22 |
| info | `economy.weapon` | arma_id_nulo | 16 |
| aviso | `plantSite` | mantido_com_flag | 9 |

Detalhe linha a linha em `issues.csv`.

## Possíveis aliases de time (jogadores em comum)

Pares de nomes de arquivo com ≥3 jogadores em comum. **Sugestão, não regra**: a equipe decide em `data/team_aliases.csv`.

- `fei_darkowls` ↔ `fei_whiteowls`: 6 jogadores
- `unicamp_tritons_black` ↔ `unicamp_tritons_red`: 4 jogadores
- `caap_malditos` ↔ `caap_momentum`: 3 jogadores

## Cobertura por time (top 15 por rounds)

| time                  |   partidas |   rounds |   rounds_ataque |   rounds_defesa |   pistols |   pistols_perdidos |   winrate_rounds |
|:----------------------|-----------:|---------:|----------------:|----------------:|----------:|-------------------:|-----------------:|
| ufmt_turuna           |         36 |      705 |             326 |             379 |        72 |                 28 |            0.557 |
| azure_bears_black     |         33 |      663 |             327 |             336 |        66 |                 32 |            0.519 |
| azure_bears_golden    |         32 |      618 |             313 |             305 |        64 |                 25 |            0.641 |
| ceub_octopus_vulgaris |         30 |      577 |             310 |             267 |        60 |                 30 |            0.494 |
| uscs_hawks            |         25 |      526 |             286 |             240 |        50 |                 24 |            0.529 |
| totale_umc            |         24 |      478 |             279 |             199 |        48 |                 19 |            0.536 |
| fei_darkowls          |         22 |      430 |             245 |             185 |        44 |                 19 |            0.519 |
| ufu_saints            |         18 |      362 |             200 |             162 |        36 |                 15 |            0.591 |
| a2e_uff               |         18 |      355 |             175 |             180 |        36 |                 22 |            0.513 |
| wolf_gaming           |         16 |      350 |             170 |             180 |        32 |                 14 |            0.557 |
| caap_hellhounds       |         18 |      345 |             175 |             170 |        36 |                 16 |            0.594 |
| ufpr_bbn              |         17 |      342 |             152 |             190 |        34 |                 22 |            0.453 |
| minerva_thunders      |         14 |      291 |             159 |             132 |        28 |                 18 |            0.505 |
| axis_anteaters        |         13 |      280 |             143 |             137 |        26 |                 14 |            0.554 |
| inatel_legacy         |         14 |      268 |             114 |             154 |        28 |                 16 |            0.478 |
