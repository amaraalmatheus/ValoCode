# Dicionário de dados

Gerado por `valocoach.pipeline`. Não edite à mão: mude `SCHEMA` no pipeline.

Convenções: ids são strings; `lado` é sempre **Attacker** ou **Defender**; campos vazios são nulos (nunca string vazia).

## matches

| Coluna | Descrição |
|---|---|
| `match_id` | ID único da partida |
| `campeonato` | Pasta de 1º nível (ex.: Univavá, Rush Series Esquenta) |
| `fase` | Subpasta (ex.: Classificatória 3, Fase de Grupos); vazio se não houver |
| `classificatoria` | Nº da classificatória (1 a 4) quando a fase é uma; senão vazio |
| `jogo_num` | Número do jogo no nome do arquivo |
| `data` | Data da partida (AAAA-MM-DD), do nome do arquivo |
| `inicio_utc` | Início da partida em UTC (gameStartMillis) |
| `mapa` | Nome do mapa |
| `versao_jogo` | Versão do jogo |
| `duracao_s` | Duração em segundos |
| `time_a` | 1º time do nome do arquivo (nome canônico, após aliases) |
| `time_b` | 2º time do nome do arquivo (nome canônico, após aliases) |
| `time_a_bruto` | time_a como escrito no arquivo |
| `time_b_bruto` | time_b como escrito no arquivo |
| `rounds_a` | Rounds vencidos por time_a |
| `rounds_b` | Rounds vencidos por time_b |
| `vencedor` | Time vencedor (nome canônico) |
| `rounds_jogados` | Rounds mantidos na tabela rounds |
| `overtime` | True se passou de 24 rounds |
| `tem_coach` | True se o JSON lista coach |
| `observadores` | Qtd. de observadores removidos de players |
| `qualidade` | 'ok' ou 'atencao' (há aviso/crítico em issues.csv para a partida) |
| `arquivo` | Caminho do JSON de origem, relativo a data/raw |

## players

| Coluna | Descrição |
|---|---|
| `match_id` | ID da partida |
| `puuid` | ID do jogador |
| `jogador` | gameName#tagLine |
| `time` | Time (nome canônico) |
| `time_bruto` | Time como escrito no arquivo |
| `cor` | Red ou Blue (lado de spawn no JSON; NÃO é ataque/defesa) |
| `agente_id` | ID do agente (tabela de nomes depende da organização) |
| `party_id` | ID do grupo |
| `tier` | competitiveTier |
| `nivel_conta` | accountLevel |
| `score` | Score total |
| `kills` | Kills totais |
| `deaths` | Mortes totais |
| `assists` | Assistências totais |
| `rounds_jogados` | roundsPlayed do jogador |
| `tempo_ms` | playtimeMillis |
| `casts_granada` | Usos da habilidade de granada |
| `casts_hab1` | Usos da habilidade 1 |
| `casts_hab2` | Usos da habilidade 2 |
| `casts_ultimate` | Usos da ultimate |

## rounds

| Coluna | Descrição |
|---|---|
| `match_id` | ID da partida |
| `round` | Número do round (começa em 0) |
| `periodo` | H1 (0-11), H2 (12-23) ou OT (24+) |
| `time` | Time da linha (nome canônico) |
| `adversario` | Time adversário |
| `lado` | Attacker ou Defender, DESTE time neste round |
| `venceu` | True se o time venceu o round |
| `resultado` | eliminacao, defuse, detonacao ou tempo_esgotado |
| `codigo_resultado_vazio` | True se roundResultCode veio vazio (resultado derivado do texto) |
| `pistol` | True nos rounds 0 e 12 |
| `plant` | True se houve plant |
| `plant_site` | A, B, C ou vazio |
| `plant_t_ms` | Tempo do plant desde o início do round (ms) |
| `plant_x` | Coordenada X do plant |
| `plant_y` | Coordenada Y do plant |
| `plantador_puuid` | Quem plantou |
| `defusador_puuid` | Quem defusou |
| `loadout_total` | Soma do loadoutValue dos 5 jogadores do time |
| `loadout_medio` | Média do loadoutValue por jogador |
| `loadout_adversario_medio` | Idem, para o adversário |
| `gasto_total` | Soma de economy.spent do time |
| `creditos_antes_medio` | Média de (remaining + spent) por jogador |
| `tipo_economia` | PROVISÓRIO. pistol; eco (<1800); force (<3700); full |

## player_rounds

| Coluna | Descrição |
|---|---|
| `match_id` | ID da partida |
| `round` | Número do round |
| `puuid` | ID do jogador |
| `time` | Time (nome canônico) |
| `lado` | Attacker ou Defender neste round |
| `loadout` | loadoutValue do jogador |
| `arma_id` | ID da arma (vazio se não registrada) |
| `armadura_id` | ID do colete (vazio = sem colete) |
| `gasto` | Créditos gastos |
| `restante` | Créditos restantes |
| `score_round` | Score no round |
| `kills_round` | Kills no round (exclui mortes autoinfligidas) |
| `morreu` | True se morreu no round |
| `dano` | Dano causado no round |
| `headshots` | Tiros na cabeça |
| `bodyshots` | Tiros no corpo |
| `legshots` | Tiros nas pernas |
| `first_blood` | True se fez a 1ª kill do round |
| `first_death` | True se sofreu a 1ª morte do round |

## kills

| Coluna | Descrição |
|---|---|
| `match_id` | ID da partida |
| `round` | Número do round |
| `ordem` | Ordem da kill no round (1 = primeira) |
| `t_round_ms` | Tempo desde o início do round (ms) |
| `t_jogo_ms` | Tempo desde o início da partida (ms) |
| `killer_puuid` | Quem matou (igual a victim_puuid em morte por bomba/queda) |
| `victim_puuid` | Quem morreu |
| `time_killer` | Time de quem matou |
| `time_victim` | Time de quem morreu |
| `lado_killer` | Attacker/Defender de quem matou |
| `lado_victim` | Attacker/Defender de quem morreu |
| `vx` | Coordenada X da vítima |
| `vy` | Coordenada Y da vítima |
| `assistentes` | puuids dos assistentes separados por | |
| `tipo_dano` | Weapon, Ability, Bomb, Fall, Melee, Crush |
| `item_dano` | ID da arma/item que finalizou |
| `autoinfligido` | True se killer == victim (bomba, queda...) |
| `first_blood` | True se é a 1ª kill do round sobre um adversário |
