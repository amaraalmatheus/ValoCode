"""Testes do pipeline com partidas sintéticas mínimas (rodar: pytest -q)."""
import json
from pathlib import Path


from valocoach.pipeline import Issues, parse_filename, processar_arquivo

PU = {c: [f"{c}{i}" for i in range(5)] for c in ("R", "B")}


def _players(com_observador=True):
    ps = [dict(puuid=u, gameName=u, tagLine="X", teamId="Red" if c == "R" else "Blue", characterId="ag",
               partyId="p", competitiveTier=0, isObserver=False, accountLevel=1,
               stats=dict(score=1, kills=1, deaths=1, assists=0, roundsPlayed=3, playtimeMillis=1,
                          abilityCasts={})) for c in PU for u in PU[c]]
    if com_observador:
        ps.append(dict(puuid="OBS", gameName="obs", tagLine="X", teamId="Neutral", characterId=None,
                       isObserver=True, stats=None))
    return ps


def _round(n, vencedor, resultado, codigo, role="Defender"):
    stats = [dict(puuid=u, kills=[], damage=[], score=0,
                  economy=dict(loadoutValue=4000, weapon="w", armor="a", remaining=100, spent=3900))
             for c in PU for u in PU[c]]
    return dict(roundNum=n, roundResult=resultado, roundResultCode=codigo, winningTeam=vencedor,
                winningTeamRole=role, bombPlanter=None, bombDefuser=None, plantSite="",
                plantRoundTime=0, plantLocation=dict(x=0, y=0), playerStats=stats)


def _escreve(tmp, nome, rounds, red, blue):
    d = dict(matchInfo=dict(matchId="m1", mapId="/Game/Maps/Ascent/Ascent", gameStartMillis=1781979191606,
                            gameLengthMillis=1000, gameVersion="v"),
             players=_players(), coaches=[],
             teams=[dict(teamId="Red", roundsWon=red, roundsPlayed=len(rounds), won=red > blue),
                    dict(teamId="Blue", roundsWon=blue, roundsPlayed=len(rounds), won=blue > red)],
             roundResults=rounds)
    p = tmp / nome
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def test_nome_com_underscores_no_time():
    g = parse_filename(Path("RUSHE_005_06-06-26_unicamp_tritons_black_7_x_13_uscs_hawks_pearl.json"))
    assert (g["time1"], g["time2"], g["s1"], g["s2"], g["mapa"]) == \
           ("unicamp_tritons_black", "uscs_hawks", 7, 13, "pearl")
    assert g["data_iso"] == "2026-06-06"


def test_timer_expirado_codigo_vazio_e_observador(tmp_path):
    p = _escreve(tmp_path, "T_001_01-01-26_alfa_1_x_0_beta_ascent.json",
                 [_round(0, "Red", "Round timer expired", "")], red=1, blue=0)
    iss = Issues()
    res = processar_arquivo(p, tmp_path, {}, iss)
    assert res is not None
    assert {r["resultado"] for r in res["rounds"]} == {"tempo_esgotado"}
    assert all(r["codigo_resultado_vazio"] for r in res["rounds"])
    assert len(res["players"]) == 10 and res["match"]["observadores"] == 1
    assert res["match"]["time_a"] == "alfa"          # Red venceu 1 => time1 do arquivo
    assert {r["time"] for r in res["rounds"] if r["venceu"]} == {"alfa"}


def test_round_sem_resultado_e_descartado_e_registrado(tmp_path):
    rounds = [_round(0, "Red", "Eliminated", "Elimination"), _round(1, "Red", "Eliminated", "Elimination"),
              _round(2, "Blue", "", "")]
    p = _escreve(tmp_path, "T_002_01-01-26_alfa_2_x_1_beta_ascent.json", rounds, red=2, blue=1)
    iss = Issues()
    res = processar_arquivo(p, tmp_path, {}, iss)
    assert res["match"]["rounds_jogados"] == 2
    acoes = {(i["acao"], i["severidade"]) for i in iss.rows}
    assert ("round_descartado", "critico") in acoes
    assert ("mantido", "aviso") in acoes             # placar não bate mais: sinalizado


def test_placar_do_nome_diferente_do_json_descarta_arquivo(tmp_path):
    p = _escreve(tmp_path, "T_003_01-01-26_alfa_5_x_1_beta_ascent.json",
                 [_round(0, "Red", "Eliminated", "Elimination")], red=1, blue=0)
    iss = Issues()
    assert processar_arquivo(p, tmp_path, {}, iss) is None
    assert iss.rows[-1]["acao"] == "arquivo_descartado"


def test_alias_de_time(tmp_path):
    p = _escreve(tmp_path, "T_004_01-01-26_alfa_1_x_0_beta_ascent.json",
                 [_round(0, "Red", "Eliminated", "Elimination")], red=1, blue=0)
    res = processar_arquivo(p, tmp_path, {"alfa": "ALFA_ORG"}, Issues())
    assert res["match"]["time_a"] == "ALFA_ORG" and res["match"]["time_a_bruto"] == "alfa"
