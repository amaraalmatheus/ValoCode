"""Testes do baseline e da viabilidade com tabelas sintéticas mínimas."""
import pandas as pd

from valocoach.baseline import rounds_apos_pistol, share_esperado_acaso


def _rounds(venceu_por_round, lados=None):
    """Um time, uma partida: lista de vitórias por round (round 0..n-1)."""
    n = len(venceu_por_round)
    return pd.DataFrame(dict(
        match_id="m", round=range(n), time="A", venceu=venceu_por_round,
        pistol=[i in (0, 12) for i in range(n)],
        lado=["Attacker" if i < 12 else "Defender" for i in range(n)]))


def test_apos_pistol_pega_n_rounds_da_mesma_metade():
    seg = rounds_apos_pistol(_rounds([False] * 24), n=2)
    assert sorted(seg["round"]) == [1, 2, 13, 14]
    assert seg.venceu_pistol.eq(False).all()


def test_apos_pistol_ignora_rounds_que_nao_existem():
    # partida de 13 rounds (13x0): só existe o pistol do round 12, sem rounds depois
    seg = rounds_apos_pistol(_rounds([True] * 13), n=2)
    assert sorted(seg["round"]) == [1, 2]


def test_apos_pistol_marca_resultado_do_pistol_da_metade():
    v = [True] + [False] * 11 + [False] + [True] * 11      # ganha o 1º pistol, perde o 2º
    seg = rounds_apos_pistol(_rounds(v), n=2)
    assert seg[seg["round"].isin([1, 2])].venceu_pistol.all()
    assert not seg[seg["round"].isin([13, 14])].venceu_pistol.any()


def test_share_esperado_acaso_fica_acima_de_20_por_cento():
    s = share_esperado_acaso(30)
    assert 0.2 < s < 0.5
    assert share_esperado_acaso(300) < s                     # mais amostra, mais perto de 20%
