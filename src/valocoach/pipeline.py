"""Pipeline de dados do VALOCOACH.

Lê todos os JSONs brutos da organização, padroniza a estrutura, identifica
campos ausentes, trata rounds com resultado vazio e grava tabelas limpas.
O restante da equipe usa `valocoach.loader.load_clean()` e nunca toca nos JSONs.

    python -m valocoach.pipeline --raw data/raw --out data/processed

Saídas em --out:
    matches, players, rounds, player_rounds, kills   (.csv)
    cobertura_times.csv        volume de rounds/pistols por time (amostra mínima)
    qualidade_campos.csv       % de nulos por coluna
    issues.csv                 TODO problema encontrado, com a ação tomada
    relatorio_qualidade.md/.json
Regra de ouro: nada é descartado em silêncio. Tudo vira uma linha em issues.csv.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------------- parâmetros
PISTOL_ROUNDS = (0, 12)          # 1º round de cada metade
ROUNDS_REGULARES = 24            # depois disso é overtime
# Classificação provisória de economia (média do loadout por jogador no round).
# A frente de Economia deve validar/ajustar estes cortes.
LIMITE_ECO = 1800
LIMITE_FORCE = 3700

RESULTADO = {                    # texto cru -> categoria padronizada
    "Eliminated": "eliminacao",
    "Bomb defused": "defuse",
    "Bomb detonated": "detonacao",
    "Round timer expired": "tempo_esgotado",
}
CODIGO = {"Elimination": "eliminacao", "Defuse": "defuse", "Detonate": "detonacao"}
ROLE_ESPERADO = {"defuse": "Defender", "detonacao": "Attacker", "tempo_esgotado": "Defender"}

# Campos que o pipeline exige (ausente/None => problema). Vazio ('') é tratado à parte.
REQ_MATCHINFO = ["matchId", "mapId", "gameStartMillis", "gameLengthMillis"]
REQ_PLAYER = ["puuid", "gameName", "teamId", "characterId", "stats"]
REQ_TEAM = ["teamId", "roundsWon", "roundsPlayed"]
REQ_ROUND = ["roundNum", "roundResult", "winningTeam", "winningTeamRole", "playerStats"]
REQ_PSTAT = ["puuid", "kills", "damage", "score", "economy"]
REQ_ECO = ["loadoutValue", "weapon", "armor", "remaining", "spent"]
REQ_KILL = ["timeSinceRoundStartMillis", "killer", "victim", "victimLocation"]

_NOME = re.compile(
    r"^(?P<prefixo>.+?)_(?P<num>\d+[a-z]?)_(?P<data>\d{2}-\d{2}-\d{2})_"
    r"(?P<time1>.+)_(?P<s1>\d+)_x_(?P<s2>\d+)_(?P<time2>.+)_(?P<mapa>[a-z]+)$"
)

# ------------------------------------------------------------ dicionário (fonte única)
SCHEMA: dict[str, list[tuple[str, str]]] = {
    "matches": [
        ("match_id", "ID único da partida"),
        ("campeonato", "Pasta de 1º nível (ex.: Univavá, Rush Series Esquenta)"),
        ("fase", "Subpasta (ex.: Classificatória 3, Fase de Grupos); vazio se não houver"),
        ("classificatoria", "Nº da classificatória (1 a 4) quando a fase é uma; senão vazio"),
        ("jogo_num", "Número do jogo no nome do arquivo"),
        ("data", "Data da partida (AAAA-MM-DD), do nome do arquivo"),
        ("inicio_utc", "Início da partida em UTC (gameStartMillis)"),
        ("mapa", "Nome do mapa"),
        ("versao_jogo", "Versão do jogo"),
        ("duracao_s", "Duração em segundos"),
        ("time_a", "1º time do nome do arquivo (nome canônico, após aliases)"),
        ("time_b", "2º time do nome do arquivo (nome canônico, após aliases)"),
        ("time_a_bruto", "time_a como escrito no arquivo"),
        ("time_b_bruto", "time_b como escrito no arquivo"),
        ("rounds_a", "Rounds vencidos por time_a"),
        ("rounds_b", "Rounds vencidos por time_b"),
        ("vencedor", "Time vencedor (nome canônico)"),
        ("rounds_jogados", "Rounds mantidos na tabela rounds"),
        ("overtime", "True se passou de 24 rounds"),
        ("tem_coach", "True se o JSON lista coach"),
        ("observadores", "Qtd. de observadores removidos de players"),
        ("qualidade", "'ok' ou 'atencao' (há aviso/crítico em issues.csv para a partida)"),
        ("arquivo", "Caminho do JSON de origem, relativo a data/raw"),
    ],
    "players": [
        ("match_id", "ID da partida"),
        ("puuid", "ID do jogador"),
        ("jogador", "gameName#tagLine"),
        ("time", "Time (nome canônico)"),
        ("time_bruto", "Time como escrito no arquivo"),
        ("cor", "Red ou Blue (lado de spawn no JSON; NÃO é ataque/defesa)"),
        ("agente_id", "ID do agente (tabela de nomes depende da organização)"),
        ("party_id", "ID do grupo"),
        ("tier", "competitiveTier"),
        ("nivel_conta", "accountLevel"),
        ("score", "Score total"),
        ("kills", "Kills totais"),
        ("deaths", "Mortes totais"),
        ("assists", "Assistências totais"),
        ("rounds_jogados", "roundsPlayed do jogador"),
        ("tempo_ms", "playtimeMillis"),
        ("casts_granada", "Usos da habilidade de granada"),
        ("casts_hab1", "Usos da habilidade 1"),
        ("casts_hab2", "Usos da habilidade 2"),
        ("casts_ultimate", "Usos da ultimate"),
    ],
    "rounds": [
        ("match_id", "ID da partida"),
        ("round", "Número do round (começa em 0)"),
        ("periodo", "H1 (0-11), H2 (12-23) ou OT (24+)"),
        ("time", "Time da linha (nome canônico)"),
        ("adversario", "Time adversário"),
        ("lado", "Attacker ou Defender, DESTE time neste round"),
        ("venceu", "True se o time venceu o round"),
        ("resultado", "eliminacao, defuse, detonacao ou tempo_esgotado"),
        ("codigo_resultado_vazio", "True se roundResultCode veio vazio (resultado derivado do texto)"),
        ("pistol", "True nos rounds 0 e 12"),
        ("plant", "True se houve plant"),
        ("plant_site", "A, B, C ou vazio"),
        ("plant_t_ms", "Tempo do plant desde o início do round (ms)"),
        ("plant_x", "Coordenada X do plant"),
        ("plant_y", "Coordenada Y do plant"),
        ("plantador_puuid", "Quem plantou"),
        ("defusador_puuid", "Quem defusou"),
        ("loadout_total", "Soma do loadoutValue dos 5 jogadores do time"),
        ("loadout_medio", "Média do loadoutValue por jogador"),
        ("loadout_adversario_medio", "Idem, para o adversário"),
        ("gasto_total", "Soma de economy.spent do time"),
        ("creditos_antes_medio", "Média de (remaining + spent) por jogador"),
        ("tipo_economia", f"PROVISÓRIO. pistol; eco (<{LIMITE_ECO}); force (<{LIMITE_FORCE}); full"),
    ],
    "player_rounds": [
        ("match_id", "ID da partida"),
        ("round", "Número do round"),
        ("puuid", "ID do jogador"),
        ("time", "Time (nome canônico)"),
        ("lado", "Attacker ou Defender neste round"),
        ("loadout", "loadoutValue do jogador"),
        ("arma_id", "ID da arma (vazio se não registrada)"),
        ("armadura_id", "ID do colete (vazio = sem colete)"),
        ("gasto", "Créditos gastos"),
        ("restante", "Créditos restantes"),
        ("score_round", "Score no round"),
        ("kills_round", "Kills no round (exclui mortes autoinfligidas)"),
        ("morreu", "True se morreu no round"),
        ("dano", "Dano causado no round"),
        ("headshots", "Tiros na cabeça"),
        ("bodyshots", "Tiros no corpo"),
        ("legshots", "Tiros nas pernas"),
        ("first_blood", "True se fez a 1ª kill do round"),
        ("first_death", "True se sofreu a 1ª morte do round"),
    ],
    "kills": [
        ("match_id", "ID da partida"),
        ("round", "Número do round"),
        ("ordem", "Ordem da kill no round (1 = primeira)"),
        ("t_round_ms", "Tempo desde o início do round (ms)"),
        ("t_jogo_ms", "Tempo desde o início da partida (ms)"),
        ("killer_puuid", "Quem matou (igual a victim_puuid em morte por bomba/queda)"),
        ("victim_puuid", "Quem morreu"),
        ("time_killer", "Time de quem matou"),
        ("time_victim", "Time de quem morreu"),
        ("lado_killer", "Attacker/Defender de quem matou"),
        ("lado_victim", "Attacker/Defender de quem morreu"),
        ("vx", "Coordenada X da vítima"),
        ("vy", "Coordenada Y da vítima"),
        ("assistentes", "puuids dos assistentes separados por |"),
        ("tipo_dano", "Weapon, Ability, Bomb, Fall, Melee, Crush"),
        ("item_dano", "ID da arma/item que finalizou"),
        ("autoinfligido", "True se killer == victim (bomba, queda...)"),
        ("first_blood", "True se é a 1ª kill do round sobre um adversário"),
    ],
}


# --------------------------------------------------------------------- issues
class Issues:
    def __init__(self):
        self.rows: list[dict] = []
        self.por_arquivo: Counter = Counter()

    def add(self, arquivo, match_id, rnd, nivel, campo, problema, acao, sev):
        self.rows.append(dict(arquivo=arquivo, match_id=match_id, round=rnd, nivel=nivel,
                              campo=campo, problema=problema, acao=acao, severidade=sev))
        if sev in ("aviso", "critico"):
            self.por_arquivo[arquivo] += 1


# --------------------------------------------------------------------- helpers
def _pasta(s: str) -> str:
    """Corrige nomes de pasta com acentos mal codificados ('#U00e1' -> 'á')."""
    return re.sub(r"#U([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)


def parse_filename(path: Path) -> dict:
    m = _NOME.match(path.stem)
    if not m:
        raise ValueError(f"nome de arquivo fora do padrão: {path.name}")
    g = m.groupdict()
    g["s1"], g["s2"] = int(g["s1"]), int(g["s2"])
    d, mth, y = g["data"].split("-")
    g["data_iso"] = f"20{y}-{mth}-{d}"
    return g


def _faltando(obj, campos) -> list[str]:
    if not isinstance(obj, dict):
        return list(campos)
    return [c for c in campos if obj.get(c) is None]


def _tipo_economia(pistol: bool, loadout_medio: float) -> str:
    if pistol:
        return "pistol"
    if loadout_medio < LIMITE_ECO:
        return "eco"
    return "force" if loadout_medio < LIMITE_FORCE else "full"


def carregar_aliases(path: Path | None) -> dict[str, str]:
    if path is None or not Path(path).exists():
        return {}
    df = pd.read_csv(path, dtype=str).fillna("")
    return {r.nome_bruto: (r.time_canonico or r.nome_bruto) for r in df.itertuples()}


# ------------------------------------------------------- processa um arquivo
def processar_arquivo(path: Path, raw_root: Path, aliases: dict, issues: Issues):
    arq = path.relative_to(raw_root).as_posix()
    arq = _pasta(arq)
    try:
        return _processar(path, raw_root, arq, aliases, issues)
    except Exception as e:  # um arquivo ruim nunca derruba o pipeline
        issues.add(arq, None, None, "arquivo", "-", f"erro inesperado: {type(e).__name__}: {e}",
                   "arquivo_descartado", "critico")
        return None


def _processar(path, raw_root, arq, aliases, issues):
    try:
        info = parse_filename(path)
    except ValueError as e:
        issues.add(arq, None, None, "arquivo", "nome_arquivo", str(e), "arquivo_descartado", "critico")
        return None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        issues.add(arq, None, None, "arquivo", "json", f"ilegível: {e}", "arquivo_descartado", "critico")
        return None

    falt = _faltando(d, ["matchInfo", "players", "teams", "roundResults"])
    if falt or not d["roundResults"]:
        issues.add(arq, None, None, "arquivo", ",".join(falt) or "roundResults",
                   "campo de topo ausente ou vazio", "arquivo_descartado", "critico")
        return None
    mi = d["matchInfo"]
    falt = _faltando(mi, REQ_MATCHINFO)
    if falt:
        issues.add(arq, None, None, "partida", ",".join(falt), "campo ausente", "arquivo_descartado", "critico")
        return None
    mid = mi["matchId"]

    # ---- jogadores (observadores saem)
    observers = [p for p in d["players"] if p.get("isObserver")]
    players = [p for p in d["players"] if not p.get("isObserver")]
    for p in observers:
        issues.add(arq, mid, None, "jogador", "isObserver", "observador (teamId Neutral, sem stats)",
                   "removido_de_players", "info")
    for p in players:
        falt = _faltando(p, REQ_PLAYER)
        if falt:
            issues.add(arq, mid, None, "jogador", ",".join(falt), "campo ausente", "arquivo_descartado", "critico")
            return None
    if len(players) != 10:
        issues.add(arq, mid, None, "partida", "players", f"{len(players)} jogadores (esperado 10)",
                   "mantido", "aviso")

    # ---- times (nome vem do arquivo; lado Red/Blue é ligado pelo placar)
    teams = {t.get("teamId"): t for t in d["teams"]}
    for t in teams.values():
        falt = _faltando(t, REQ_TEAM)
        if falt:
            issues.add(arq, mid, None, "partida", ",".join(falt), "campo ausente em teams",
                       "arquivo_descartado", "critico")
            return None
    if sorted(t["roundsWon"] for t in teams.values()) != sorted([info["s1"], info["s2"]]) \
            or info["s1"] == info["s2"]:
        issues.add(arq, mid, None, "partida", "placar", "placar do nome do arquivo não bate com teams[]",
                   "arquivo_descartado", "critico")
        return None
    bruto = {s: (info["time1"] if t["roundsWon"] == info["s1"] else info["time2"]) for s, t in teams.items()}
    nome = {s: aliases.get(b, b) for s, b in bruto.items()}
    side_of = {p["puuid"]: p["teamId"] for p in players}
    pinfo = {p["puuid"]: p for p in players}

    # ---- rounds
    rounds, prounds, kills = [], [], []
    wins = Counter()
    for r in d["roundResults"]:
        rn = r.get("roundNum")
        falt = _faltando(r, REQ_ROUND)
        if falt or r["winningTeam"] not in nome:
            issues.add(arq, mid, rn, "round", ",".join(falt) or "winningTeam", "campo ausente/inválido",
                       "round_descartado", "critico")
            continue
        res = RESULTADO.get(r["roundResult"])
        codigo_vazio = not r.get("roundResultCode")
        if res is None:  # resultado vazio ou desconhecido: tenta o código
            res = CODIGO.get(r.get("roundResultCode"))
            if res is None:
                issues.add(arq, mid, rn, "round", "roundResult",
                           f"resultado vazio/desconhecido ({r['roundResult']!r}) e sem código", 
                           "round_descartado", "critico")
                continue
            issues.add(arq, mid, rn, "round", "roundResult", "texto do resultado vazio",
                       "inferido_pelo_codigo", "aviso")
        elif codigo_vazio:
            issues.add(arq, mid, rn, "round", "roundResultCode",
                       f"código vazio em round '{r['roundResult']}'", "resultado_derivado_do_texto", "info")

        win_side, win_role = r["winningTeam"], r["winningTeamRole"]
        lose_side = next(s for s in nome if s != win_side)
        role = {win_side: win_role, lose_side: "Defender" if win_role == "Attacker" else "Attacker"}
        plant = bool(r.get("plantSite"))
        if res in ROLE_ESPERADO and win_role != ROLE_ESPERADO[res]:
            issues.add(arq, mid, rn, "round", "winningTeamRole",
                       f"{res} com vencedor {win_role}", "mantido", "aviso")
        if res == "tempo_esgotado" and plant:
            issues.add(arq, mid, rn, "round", "plantSite",
                       "plant registrado em round encerrado por tempo", "mantido_com_flag", "aviso")
        if res in ("defuse", "detonacao") and not plant:
            issues.add(arq, mid, rn, "round", "plantSite", f"{res} sem plant", "mantido", "aviso")
        wins[win_side] += 1

        # economia e estatísticas por jogador
        eco = defaultdict(lambda: dict(l=[], g=[], c=[]))
        for ps in r["playerStats"]:
            falt = _faltando(ps, REQ_PSTAT)
            if falt or ps["puuid"] not in side_of:
                issues.add(arq, mid, rn, "jogador_round", ",".join(falt) or "puuid",
                           "campo ausente ou jogador desconhecido", "linha_descartada", "aviso")
                continue
            e = ps["economy"]
            falt_e = _faltando(e, REQ_ECO)
            if falt_e:
                issues.add(arq, mid, rn, "jogador_round", "economy." + ",".join(falt_e),
                           "campo ausente", "preenchido_com_nulo", "aviso")
            if e.get("weapon") == "":
                issues.add(arq, mid, rn, "jogador_round", "economy.weapon", "arma não registrada",
                           "arma_id_nulo", "info")
            s = side_of[ps["puuid"]]
            lo = e.get("loadoutValue") or 0
            eco[s]["l"].append(lo)
            eco[s]["g"].append(e.get("spent") or 0)
            eco[s]["c"].append((e.get("remaining") or 0) + (e.get("spent") or 0))

            ks = ps["kills"]
            dm = ps["damage"]
            prounds.append(dict(
                match_id=mid, round=rn, puuid=ps["puuid"], time=nome[s], lado=role[s], loadout=lo,
                arma_id=e.get("weapon") or None, armadura_id=e.get("armor") or None,
                gasto=e.get("spent"), restante=e.get("remaining"), score_round=ps["score"],
                kills_round=sum(1 for k in ks if k.get("victim") != ps["puuid"]),
                dano=sum(x.get("damage", 0) for x in dm),
                headshots=sum(x.get("headshots", 0) for x in dm),
                bodyshots=sum(x.get("bodyshots", 0) for x in dm),
                legshots=sum(x.get("legshots", 0) for x in dm)))

        # kills do round em ordem de tempo
        todas = []
        for ps in r["playerStats"]:
            for k in ps.get("kills") or []:
                falt = _faltando(k, REQ_KILL)
                if falt:
                    issues.add(arq, mid, rn, "kill", ",".join(falt), "campo ausente", "kill_descartada", "aviso")
                    continue
                if k["killer"] not in side_of or k["victim"] not in side_of:
                    issues.add(arq, mid, rn, "kill", "killer/victim", "puuid fora da lista de jogadores",
                               "kill_descartada", "aviso")
                    continue
                todas.append(k)
        todas.sort(key=lambda k: k["timeSinceRoundStartMillis"])
        for v, c in Counter(k["victim"] for k in todas).items():
            if c > 1:
                issues.add(arq, mid, rn, "kill", "victim",
                           f"jogador morreu {c}x no round (provável revive)", "mantido", "info")
        fb_done = False
        for i, k in enumerate(todas, 1):
            auto = k["killer"] == k["victim"]
            fb = (not auto) and (not fb_done)
            fb_done = fb_done or fb
            sk, sv = side_of[k["killer"]], side_of[k["victim"]]
            fd = k.get("finishingDamage") or {}
            ass = [a if isinstance(a, str) else (a.get("assistantPuuid") or a.get("puuid") or "")
                   for a in k.get("assistants") or []]
            kills.append(dict(
                match_id=mid, round=rn, ordem=i, t_round_ms=k["timeSinceRoundStartMillis"],
                t_jogo_ms=k.get("timeSinceGameStartMillis"), killer_puuid=k["killer"],
                victim_puuid=k["victim"], time_killer=nome[sk], time_victim=nome[sv],
                lado_killer=role[sk], lado_victim=role[sv],
                vx=k["victimLocation"]["x"], vy=k["victimLocation"]["y"],
                assistentes="|".join(a for a in ass if a), tipo_dano=fd.get("damageType"),
                item_dano=fd.get("damageItem") or None, autoinfligido=auto, first_blood=fb))
        fb_k = next((k for k in kills if k["match_id"] == mid and k["round"] == rn and k["first_blood"]), None)
        for pr in prounds:
            if pr["match_id"] == mid and pr["round"] == rn:
                pr["first_blood"] = bool(fb_k and fb_k["killer_puuid"] == pr["puuid"])
                pr["first_death"] = bool(fb_k and fb_k["victim_puuid"] == pr["puuid"])
                pr["morreu"] = any(x["victim_puuid"] == pr["puuid"] for x in kills
                                   if x["match_id"] == mid and x["round"] == rn)

        pistol = rn in PISTOL_ROUNDS
        periodo = "H1" if rn < 12 else ("H2" if rn < ROUNDS_REGULARES else "OT")
        med = {s: (sum(v["l"]) / len(v["l"]) if v["l"] else 0.0) for s, v in eco.items()}
        for s in nome:
            v = eco[s]
            n = len(v["l"]) or 1
            rounds.append(dict(
                match_id=mid, round=rn, periodo=periodo, time=nome[s], adversario=nome[next(x for x in nome if x != s)],
                lado=role[s], venceu=(s == win_side), resultado=res, codigo_resultado_vazio=codigo_vazio,
                pistol=pistol, plant=plant, plant_site=r.get("plantSite") or None,
                plant_t_ms=r.get("plantRoundTime") if plant else None,
                plant_x=(r.get("plantLocation") or {}).get("x") if plant else None,
                plant_y=(r.get("plantLocation") or {}).get("y") if plant else None,
                plantador_puuid=r.get("bombPlanter"), defusador_puuid=r.get("bombDefuser"),
                loadout_total=sum(v["l"]), loadout_medio=round(med[s], 1),
                loadout_adversario_medio=round(med[next(x for x in nome if x != s)], 1),
                gasto_total=sum(v["g"]), creditos_antes_medio=round(sum(v["c"]) / n, 1),
                tipo_economia=_tipo_economia(pistol, med[s])))

    if not rounds:
        issues.add(arq, mid, None, "partida", "roundResults", "nenhum round aproveitável",
                   "arquivo_descartado", "critico")
        return None
    for s, t in teams.items():  # placar x rounds mantidos
        if wins[s] != t["roundsWon"]:
            issues.add(arq, mid, None, "partida", "roundsWon",
                       f"{nome[s]}: {wins[s]} rounds mantidos vs placar {t['roundsWon']}",
                       "mantido", "aviso")

    # ---- tabelas de partida e jogadores
    partes = Path(arq).parts[:-1]
    fase = partes[1] if len(partes) > 1 else None
    cl = re.search(r"Classificat\w+\s+(\d)", fase or "")
    a_side = next(s for s, t in teams.items() if t["roundsWon"] == info["s1"])
    n_rounds = len({x["round"] for x in rounds})
    match = dict(
        match_id=mid, campeonato=partes[0] if partes else None, fase=fase,
        classificatoria=int(cl.group(1)) if cl else None, jogo_num=info["num"], data=info["data_iso"],
        inicio_utc=datetime.fromtimestamp(mi["gameStartMillis"] / 1000, tz=timezone.utc).isoformat(),
        mapa=mi["mapId"].split("/")[-1], versao_jogo=mi.get("gameVersion"),
        duracao_s=round(mi["gameLengthMillis"] / 1000), time_a=nome[a_side],
        time_b=next(v for s, v in nome.items() if s != a_side),
        time_a_bruto=bruto[a_side], time_b_bruto=next(v for s, v in bruto.items() if s != a_side),
        rounds_a=info["s1"], rounds_b=info["s2"],
        vencedor=nome[max(teams, key=lambda s: teams[s]["roundsWon"])],
        rounds_jogados=n_rounds, overtime=n_rounds > ROUNDS_REGULARES, tem_coach=bool(d.get("coaches")),
        observadores=len(observers), arquivo=arq)
    plist = []
    for p in players:
        st = p["stats"]
        ac = st.get("abilityCasts") or {}
        plist.append(dict(
            match_id=mid, puuid=p["puuid"], jogador=f"{p['gameName']}#{p.get('tagLine', '')}",
            time=nome[p["teamId"]], time_bruto=bruto[p["teamId"]], cor=p["teamId"],
            agente_id=p["characterId"], party_id=p.get("partyId"), tier=p.get("competitiveTier"),
            nivel_conta=p.get("accountLevel"), score=st.get("score"), kills=st.get("kills"),
            deaths=st.get("deaths"), assists=st.get("assists"), rounds_jogados=st.get("roundsPlayed"),
            tempo_ms=st.get("playtimeMillis"), casts_granada=ac.get("grenadeCasts"),
            casts_hab1=ac.get("ability1Casts"), casts_hab2=ac.get("ability2Casts"),
            casts_ultimate=ac.get("ultimateCasts")))
    return dict(match=match, players=plist, rounds=rounds, player_rounds=prounds, kills=kills)


# ------------------------------------------------------------------ pipeline
def _checagens(T: dict[str, pd.DataFrame]) -> list[tuple[str, bool, str]]:
    r, m, p, k = T["rounds"], T["matches"], T["players"], T["kills"]
    out = []
    g = r.groupby(["match_id", "round"])
    out.append(("Cada round tem 2 linhas e exatamente 1 vencedor",
                bool((g.size() == 2).all() and (g.venceu.sum() == 1).all()), f"{len(g)} rounds"))
    out.append(("Cada round tem 1 atacante e 1 defensor",
                bool((r.assign(a=r.lado == "Attacker").groupby(["match_id", "round"]).a.sum() == 1).all()), ""))
    out.append(("match_id único", bool(m.match_id.is_unique), f"{len(m)} partidas"))
    npl = p.groupby("match_id").size()
    out.append(("10 jogadores por partida (sem observadores)", bool((npl == 10).all()),
                f"{int((npl != 10).sum())} partidas fora do padrão"))
    puu = set(p.puuid)
    out.append(("Todo killer/victim está em players",
                bool(k.killer_puuid.isin(puu).all() and k.victim_puuid.isin(puu).all()), f"{len(k)} kills"))
    w = r[r.venceu].groupby(["match_id", "time"]).size().rename("w").reset_index()
    a = m.merge(w, left_on=["match_id", "time_a"], right_on=["match_id", "time"], how="left").w.fillna(0)
    b = m.merge(w, left_on=["match_id", "time_b"], right_on=["match_id", "time"], how="left").w.fillna(0)
    ok = int(((a == m.rounds_a) & (b == m.rounds_b)).sum())
    out.append(("Rounds vencidos batem com o placar", ok == len(m), f"{ok}/{len(m)} partidas"))
    return out


def _sugestoes_alias(players: pd.DataFrame, minimo: int = 3) -> list[tuple[str, str, int]]:
    por = players.groupby("time_bruto").puuid.apply(set)
    pares = []
    for a, b in combinations(por.index, 2):
        n = len(por[a] & por[b])
        if n >= minimo:
            pares.append((a, b, n))
    return sorted(pares, key=lambda x: -x[2])


def _cobertura(r: pd.DataFrame) -> pd.DataFrame:
    g = r.groupby("time")
    cob = pd.DataFrame({
        "partidas": g.match_id.nunique(), "rounds": g.size(),
        "rounds_ataque": g.apply(lambda x: (x.lado == "Attacker").sum(), include_groups=False),
        "rounds_defesa": g.apply(lambda x: (x.lado == "Defender").sum(), include_groups=False),
        "pistols": g.apply(lambda x: x.pistol.sum(), include_groups=False),
        "pistols_perdidos": g.apply(lambda x: (x.pistol & ~x.venceu).sum(), include_groups=False),
        "winrate_rounds": g.venceu.mean().round(3)})
    return cob.sort_values("rounds", ascending=False).reset_index()


def escrever_dicionario(docs_dir: Path):
    docs_dir.mkdir(parents=True, exist_ok=True)
    L = ["# Dicionário de dados", "",
         "Gerado por `valocoach.pipeline`. Não edite à mão: mude `SCHEMA` no pipeline.", "",
         "Convenções: ids são strings; `lado` é sempre **Attacker** ou **Defender**; "
         "campos vazios são nulos (nunca string vazia).", ""]
    for t, cols in SCHEMA.items():
        L += [f"## {t}", "", "| Coluna | Descrição |", "|---|---|"]
        L += [f"| `{c}` | {d} |" for c, d in cols] + [""]
    (docs_dir / "dicionario_de_dados.md").write_text("\n".join(L), encoding="utf-8")


def rodar(raw: Path, out: Path, aliases_path: Path | None, docs: Path | None, formato: str = "csv"):
    raw, out = Path(raw), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    aliases = carregar_aliases(aliases_path)
    issues = Issues()
    arquivos = sorted(raw.rglob("*.json"))
    if not arquivos:
        raise SystemExit(f"Nenhum JSON encontrado em {raw}")

    acc = {k: [] for k in ("matches", "players", "rounds", "player_rounds", "kills")}
    vistos, descartados = set(), 0
    for p in arquivos:
        res = processar_arquivo(p, raw, aliases, issues)
        if res is None:
            descartados += 1
            continue
        mid = res["match"]["match_id"]
        if mid in vistos:
            issues.add(res["match"]["arquivo"], mid, None, "partida", "matchId", "matchId duplicado",
                       "arquivo_descartado", "critico")
            descartados += 1
            continue
        vistos.add(mid)
        res["match"]["qualidade"] = "atencao" if issues.por_arquivo[res["match"]["arquivo"]] else "ok"
        acc["matches"].append(res["match"])
        for k in ("players", "rounds", "player_rounds", "kills"):
            acc[k] += res[k]

    T = {}
    for nome, linhas in acc.items():
        cols = [c for c, _ in SCHEMA[nome]]
        df = pd.DataFrame(linhas)
        faltam = set(cols) - set(df.columns)
        extras = set(df.columns) - set(cols)
        assert not faltam and not extras, f"{nome}: schema diverge (faltam {faltam}, extras {extras})"
        T[nome] = df[cols]

    # --- escrita
    for nome, df in T.items():
        if formato == "parquet":
            df.to_parquet(out / f"{nome}.parquet", index=False)
        else:
            df.to_csv(out / f"{nome}.csv", index=False)
    iss = pd.DataFrame(issues.rows, columns=["arquivo", "match_id", "round", "nivel", "campo",
                                              "problema", "acao", "severidade"])
    iss.to_csv(out / "issues.csv", index=False)
    cob = _cobertura(T["rounds"])
    cob.to_csv(out / "cobertura_times.csv", index=False)
    nulos = pd.concat([(df.isna().mean() * 100).round(2).rename("pct_nulos").to_frame().assign(tabela=n)
                       for n, df in T.items()]).reset_index(names="coluna")
    nulos[["tabela", "coluna", "pct_nulos"]].to_csv(out / "qualidade_campos.csv", index=False)

    checks = _checagens(T)
    sug = _sugestoes_alias(T["players"])
    if aliases_path is not None and not Path(aliases_path).exists():
        brutos = sorted(set(T["matches"].time_a_bruto) | set(T["matches"].time_b_bruto))
        Path(aliases_path).parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({"nome_bruto": brutos, "time_canonico": brutos}).to_csv(aliases_path, index=False)

    resumo = {
        "arquivos_lidos": len(arquivos), "arquivos_descartados": descartados,
        "partidas": len(T["matches"]), "partidas_com_atencao": int((T["matches"].qualidade == "atencao").sum()),
        "rounds": int(len(T["rounds"]) // 2), "kills": len(T["kills"]),
        "observadores_removidos": int(T["matches"].observadores.sum()),
        "rounds_codigo_vazio": int(T["rounds"].codigo_resultado_vazio.sum() // 2),
        "times": int(T["rounds"].time.nunique()),
        "issues_por_tipo": iss.groupby(["severidade", "campo", "acao"]).size().reset_index(name="n")
                              .sort_values("n", ascending=False).to_dict("records"),
        "checagens": [dict(nome=n, ok=o, detalhe=d) for n, o, d in checks],
        "aliases_aplicados": len(aliases),
    }
    (out / "relatorio_qualidade.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2),
                                                  encoding="utf-8")
    (out / "relatorio_qualidade.md").write_text(_md(resumo, cob, sug), encoding="utf-8")
    if docs is not None:
        escrever_dicionario(Path(docs))
    print(f"OK: {resumo['partidas']} partidas, {resumo['rounds']} rounds, {resumo['kills']} kills | "
          f"{descartados} arquivos descartados | {len(iss)} issues | saída em {out}")
    return T, resumo


def _md(r, cob, sug) -> str:
    L = ["# Relatório de qualidade dos dados", "", "## Resumo", "", "| Item | Valor |", "|---|---|"]
    for k in ("arquivos_lidos", "arquivos_descartados", "partidas", "partidas_com_atencao", "rounds", "kills",
              "times", "observadores_removidos", "rounds_codigo_vazio", "aliases_aplicados"):
        L.append(f"| {k.replace('_', ' ')} | {r[k]} |")
    L += ["", "## Checagens de integridade", ""]
    L += [f"- {'✅' if c['ok'] else '❌'} {c['nome']} ({c['detalhe']})" if c["detalhe"]
          else f"- {'✅' if c['ok'] else '❌'} {c['nome']}" for c in r["checagens"]]
    L += ["", "## Problemas encontrados e tratamento", "",
          "| Severidade | Campo | Ação | Ocorrências |", "|---|---|---|---|"]
    L += [f"| {i['severidade']} | `{i['campo']}` | {i['acao']} | {i['n']} |" for i in r["issues_por_tipo"]]
    L += ["", "Detalhe linha a linha em `issues.csv`.", "",
          "## Possíveis aliases de time (jogadores em comum)", "",
          "Pares de nomes de arquivo com ≥3 jogadores em comum. **Sugestão, não regra**: "
          "a equipe decide em `data/team_aliases.csv`.", ""]
    L += [f"- `{a}` ↔ `{b}`: {n} jogadores" for a, b, n in sug[:40]] or ["- nenhum"]
    L += ["", "## Cobertura por time (top 15 por rounds)", "",
          cob.head(15).to_markdown(index=False) if _tem_tabulate() else cob.head(15).to_string(index=False), ""]
    return "\n".join(L)


def _tem_tabulate() -> bool:
    try:
        import tabulate  # noqa: F401
        return True
    except ImportError:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--out", default="data/processed")
    ap.add_argument("--aliases", default="data/team_aliases.csv",
                    help="CSV nome_bruto,time_canonico (criado se não existir)")
    ap.add_argument("--docs", default="docs", help="onde gravar dicionario_de_dados.md ('' para pular)")
    ap.add_argument("--formato", choices=["csv", "parquet"], default="csv")
    a = ap.parse_args()
    rodar(Path(a.raw), Path(a.out), Path(a.aliases) if a.aliases else None,
          Path(a.docs) if a.docs else None, a.formato)


if __name__ == "__main__":
    main()
