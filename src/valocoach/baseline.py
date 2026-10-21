"""Média da base (baseline da liga) e inventário de viabilidade dos diagnósticos.

    python -m valocoach.baseline                  # usa data/processed
    python -m valocoach.baseline --min 15 --apos-pistol 2

Saídas:
    data/processed/baseline_liga.csv       taxa da liga por métrica/mapa/lado
    data/processed/viabilidade_times.csv   amostra de cada time em cada diagnóstico
    docs/inventario_viabilidade.md         resumo para a equipe (versionado)

Duas decisões de análise ficam em constantes aqui, para a equipe ajustar:
    MIN_AMOSTRA    rounds mínimos para um diagnóstico aparecer (plano: 15)
    N_APOS_PISTOL  quantos rounds depois do pistol contam como "recuperação"
                   ou "conversão" (mesma metade, mesmo lado)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .loader import load_clean
from .pipeline import LIMITE_ECO, LIMITE_FORCE

MIN_AMOSTRA = 15
N_APOS_PISTOL = 2
LADOS = ("Attacker", "Defender")
CORTES = (10, 15, 20, 30)        # sensibilidade mostrada no inventário
COLS_BASELINE = ["metrica", "mapa", "lado", "recorte", "n", "taxa_liga",
                 "n_times", "media_times", "dp_times"]


# ----------------------------------------------------------------- preparação
def _tipo(loadout_medio: pd.Series) -> pd.Series:
    v = np.select([loadout_medio < LIMITE_ECO, loadout_medio < LIMITE_FORCE], ["eco", "force"], "full")
    return pd.Series(v, index=loadout_medio.index)


def preparar(T: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """rounds + mapa + tipo de economia do adversário (mesmos cortes do pipeline)."""
    r = T["rounds"].merge(T["matches"][["match_id", "mapa"]], on="match_id", how="left")
    r["tipo_adversario"] = np.where(r.pistol, "pistol", _tipo(r.loadout_adversario_medio))
    return r


def rounds_apos_pistol(r: pd.DataFrame, n: int = N_APOS_PISTOL) -> pd.DataFrame:
    """Os `n` rounds seguintes a cada pistol (mesma metade). Uma linha por time e round.

    Traz `venceu_pistol` (se o time ganhou o pistol) e `venceu` (resultado do round seguinte).
    Rounds que não existem (partida acabou antes) simplesmente não aparecem.
    """
    p = r[r.pistol][["match_id", "round", "time", "venceu"]].rename(
        columns={"round": "round_pistol", "venceu": "venceu_pistol"})
    seg = pd.concat([p.assign(round=p.round_pistol + k) for k in range(1, n + 1)], ignore_index=True)
    return seg.merge(r, on=["match_id", "round", "time"], how="inner")


def primeiros_bloods(T: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Por time: total de first bloods, do jogador que mais fez e a fatia dele."""
    fb = T["player_rounds"].query("first_blood").groupby(["time", "puuid"]).size().rename("fb").reset_index()
    t = fb.groupby("time").fb.agg(n="sum", top="max")
    t["top1_share"] = t.top / t.n
    return t.reset_index()


def share_esperado_acaso(n: int, jogadores: int = 5, sims: int = 2000, seed: int = 42) -> float:
    """Fatia média do 'maior' jogador se os n first bloods fossem sorteados por igual.

    Mesmo sem dependência real, o maior de 5 sempre passa de 20%; esse é o piso justo.
    """
    rng = np.random.default_rng(seed)
    return float((rng.multinomial(n, [1 / jogadores] * jogadores, size=sims).max(axis=1) / n).mean())


# ------------------------------------------------------------------- baseline
def _blocos(df: pd.DataFrame, metrica: str, min_amostra: int, *, recorte: str | None = None,
            com_mapa=(False, True), com_lado=(False, True)) -> pd.DataFrame:
    """Taxa de vitória agregada (liga) e média/desvio entre times, por recorte."""
    df = df.assign(_t="x")
    saidas = []
    for usa_mapa in com_mapa:
        for usa_lado in com_lado:
            ch = ["_t"] + (["mapa"] if usa_mapa else []) + (["lado"] if usa_lado else []) \
                 + ([recorte] if recorte else [])
            pool = df.groupby(ch).venceu.agg(n="size", taxa_liga="mean")
            por_time = df.groupby(["time"] + ch).venceu.agg(n="size", taxa="mean").reset_index()
            por_time = por_time[por_time.n >= min_amostra]
            st = por_time.groupby(ch).taxa.agg(n_times="size", media_times="mean", dp_times="std")
            o = pool.join(st).reset_index().drop(columns="_t")
            if recorte:
                o = o.rename(columns={recorte: "recorte"})
            saidas.append(o)
    out = pd.concat(saidas, ignore_index=True)
    out.insert(0, "metrica", metrica)
    for c in ("mapa", "lado", "recorte"):
        if c not in out:
            out[c] = "todos"
        out[c] = out[c].fillna("todos")
    return out


def calcular_baseline(T, min_amostra=MIN_AMOSTRA, n_apos=N_APOS_PISTOL) -> pd.DataFrame:
    r = preparar(T)
    seg = rounds_apos_pistol(r, n_apos)
    nao_pistol = r[~r.pistol]
    partes = [
        _blocos(r, "winrate_lado", min_amostra, com_lado=(True,)),
        _blocos(r[r.pistol], "pistol", min_amostra, com_lado=(True,)),
        _blocos(seg[~seg.venceu_pistol], "apos_pistol_perdido", min_amostra),
        _blocos(seg[seg.venceu_pistol], "apos_pistol_ganho", min_amostra),
        _blocos(nao_pistol, "economia", min_amostra, recorte="tipo_economia", com_mapa=(False,)),
        _blocos(nao_pistol[nao_pistol.tipo_economia == "force"], "force_vs_adversario", min_amostra,
                recorte="tipo_adversario", com_mapa=(False,)),
    ]
    # first bloods: concentração no jogador que mais faz
    fb = primeiros_bloods(T)
    ok = fb[fb.n >= min_amostra].copy()
    ok["acaso"] = [share_esperado_acaso(int(n)) for n in ok.n]
    base_fb = pd.DataFrame([
        dict(metrica="fb_top1_share", n=int(ok.n.sum()), taxa_liga=ok.top1_share.mean(), n_times=len(ok),
             media_times=ok.top1_share.mean(), dp_times=ok.top1_share.std()),
        dict(metrica="fb_top1_share_acaso", n=int(ok.n.sum()), taxa_liga=ok.acaso.mean(), n_times=len(ok)),
        dict(metrica="fb_top1_share_p75", n=int(ok.n.sum()), taxa_liga=ok.top1_share.quantile(.75), n_times=len(ok)),
        dict(metrica="fb_top1_share_p90", n=int(ok.n.sum()), taxa_liga=ok.top1_share.quantile(.90), n_times=len(ok)),
    ])
    for c in ("mapa", "lado", "recorte"):
        base_fb[c] = "todos"
    return pd.concat(partes + [base_fb], ignore_index=True)[COLS_BASELINE]


# ----------------------------------------------------------------- viabilidade
def calcular_viabilidade(T, min_amostra=MIN_AMOSTRA, n_apos=N_APOS_PISTOL) -> pd.DataFrame:
    """Amostra de cada time em cada diagnóstico. n = rounds (D1-D4) ou first bloods (D5)."""
    r = preparar(T)
    times = sorted(r.time.unique())
    seg = rounds_apos_pistol(r, n_apos)
    linhas = []

    def add(diag, mapa, lado, unidade, serie):
        s = serie.reindex(times, fill_value=0)
        linhas.extend(dict(time=t, diagnostico=diag, mapa=mapa, lado=lado, unidade=unidade, n=int(v))
                      for t, v in s.items())

    for diag, ganhou in ((1, False), (3, True)):
        s = seg[seg.venceu_pistol == ganhou]
        add(diag, "todos", "todos", "rounds", s.groupby("time").size())
        for lado in LADOS:
            add(diag, "todos", lado, "rounds", s[s.lado == lado].groupby("time").size())

    ml = r.groupby(["time", "mapa", "lado"]).size().unstack("lado").reindex(columns=list(LADOS)).fillna(0)
    for mapa in sorted(r.mapa.unique()):
        sub = ml.xs(mapa, level="mapa") if mapa in ml.index.get_level_values("mapa") else ml.iloc[0:0]
        for lado in LADOS:
            add(2, mapa, lado, "rounds", sub[lado] if len(sub) else pd.Series(dtype=float))
        add(2, mapa, "ambos", "rounds", sub.min(axis=1) if len(sub) else pd.Series(dtype=float))

    f = r[(~r.pistol) & (r.tipo_economia == "force")]
    add(4, "todos", "todos", "rounds", f.groupby("time").size())
    for lado in LADOS:
        add(4, "todos", lado, "rounds", f[f.lado == lado].groupby("time").size())

    fb = primeiros_bloods(T).set_index("time").n
    add(5, "todos", "todos", "first_bloods", fb)

    v = pd.DataFrame(linhas)
    v["viavel"] = v.n >= min_amostra
    return v


def _times_viaveis(v: pd.DataFrame, diag, lado, corte) -> int:
    s = v[(v.diagnostico == diag) & (v.lado == lado)]
    if diag == 2:
        return int(s.groupby("time").n.max().ge(corte).sum())
    return int((s.n >= corte).sum())


# --------------------------------------------------------------------- inventário
def escrever_inventario(v: pd.DataFrame, base: pd.DataFrame, T, min_amostra, n_apos, destino: Path):
    n_times = v.time.nunique()
    def q(diag, lado, corte=min_amostra):
        return _times_viaveis(v, diag, lado, corte)
    def b(metrica, mapa="todos", lado="todos", recorte="todos"):
        s = base[(base.metrica == metrica) & (base.mapa == mapa) & (base.lado == lado) & (base.recorte == recorte)]
        return float(s.taxa_liga.iloc[0]) if len(s) else float("nan")
    pc = lambda x: f"{x * 100:.1f}%"
    mapas_ok = (v[(v.diagnostico == 2) & (v.lado == "ambos") & (v.n >= min_amostra)]
                .groupby("time").size())

    L = ["# Inventário de viabilidade", "",
         f"Gerado por `python -m valocoach.baseline`. **{n_times} times** na base. "
         f"Amostra mínima: **{min_amostra}**. Rounds seguintes ao pistol: **{n_apos}**.", "",
         "Unidade da amostra: rounds (D1 a D4) e first bloods (D5). "
         "'Times viáveis' = times com amostra ≥ corte no recorte indicado.", "",
         "| # | Diagnóstico | Campos necessários | Dados sustentam? | Times viáveis (corte atual) | Observações |",
         "|---|---|---|---|---|---|",
         f"| 1 | Recuperação após perder o pistol | `rounds`: pistol, venceu, lado, round | Sim | "
         f"{q(1, 'todos')} geral · {q(1, 'Attacker')} ataque · {q(1, 'Defender')} defesa | "
         f"Amostra = {n_apos} rounds por pistol perdido. O recorte por mapa fica ralo demais. |",
         f"| 2 | Ataque vs. defesa por mapa | `rounds`: lado, venceu; `matches`: mapa | Sim | "
         f"{q(2, 'ambos')} com ≥1 mapa viável | Corte vale por mapa **e** por lado. "
         f"Média de {mapas_ok.mean():.1f} mapas viáveis por time (entre os viáveis). |" if len(mapas_ok) else
         f"| 2 | Ataque vs. defesa por mapa | `rounds`: lado, venceu; `matches`: mapa | Sim | "
         f"{q(2, 'ambos')} com ≥1 mapa viável | Corte vale por mapa e por lado. |",
         f"| 3 | Conversão após ganhar o pistol | `rounds`: pistol, venceu, lado, round | Sim | "
         f"{q(3, 'todos')} geral · {q(3, 'Attacker')} ataque · {q(3, 'Defender')} defesa | "
         f"Mesma definição do D1, espelhada. |",
         f"| 4 | Force buy sem resultado | `rounds`: tipo_economia, venceu, lado | Sim, com ressalva | "
         f"{q(4, 'todos')} geral · {q(4, 'Attacker')} ataque · {q(4, 'Defender')} defesa | "
         f"`tipo_economia` é **provisório** (cortes de loadout); validar com a frente de Economia. |",
         f"| 5 | Dependência de um jogador | `player_rounds`: first_blood, puuid, time | Sim | "
         f"{q(5, 'todos')} | Compare com o **acaso** (abaixo), não com 20%: o maior de 5 sempre passa disso. |",
         "", "## Sensibilidade ao corte de amostra", "",
         "Quantos times sobram em cada recorte se o corte mudar. Ajuda a confirmar o número final.", "",
         "| Diagnóstico / recorte | " + " | ".join(f"≥{c}" for c in CORTES) + " |",
         "|---|" + "---|" * len(CORTES)]
    for diag, nome, lados in ((1, "D1 recuperação", ("todos", "Attacker", "Defender")),
                              (2, "D2 ataque vs defesa (≥1 mapa)", ("ambos",)),
                              (3, "D3 conversão", ("todos", "Attacker", "Defender")),
                              (4, "D4 force buy", ("todos", "Attacker", "Defender")),
                              (5, "D5 first bloods", ("todos",))):
        for lado in lados:
            rot = nome if lado in ("todos", "ambos") else f"{nome} · {lado}"
            L.append(f"| {rot} | " + " | ".join(str(_times_viaveis(v, diag, lado, c)) for c in CORTES) + " |")

    fb_p90, fb_p75, fb_acaso, fb_m = (b("fb_top1_share_p90"), b("fb_top1_share_p75"),
                                       b("fb_top1_share_acaso"), b("fb_top1_share"))
    L += ["", "## Média da base (referência para os cards)", "",
          "Taxa de vitória agregada da liga (todos os rounds, ambos os lados). "
          "Tabela completa por mapa e lado em `data/processed/baseline_liga.csv`.", "",
          "| Situação | Taxa da liga |", "|---|---|",
          f"| Pistol, ataque | {pc(b('pistol', lado='Attacker'))} |",
          f"| Pistol, defesa | {pc(b('pistol', lado='Defender'))} |",
          f"| Rounds de ataque (geral) | {pc(b('winrate_lado', lado='Attacker'))} |",
          f"| Rounds de defesa (geral) | {pc(b('winrate_lado', lado='Defender'))} |",
          f"| Após perder o pistol (geral) | {pc(b('apos_pistol_perdido'))} |",
          f"| Após perder o pistol, ataque | {pc(b('apos_pistol_perdido', lado='Attacker'))} |",
          f"| Após perder o pistol, defesa | {pc(b('apos_pistol_perdido', lado='Defender'))} |",
          f"| Após ganhar o pistol (geral) | {pc(b('apos_pistol_ganho'))} |",
          f"| Force buy (geral) | {pc(b('economia', recorte='force'))} |",
          f"| Force buy contra adversário full | {pc(b('force_vs_adversario', recorte='full'))} |",
          f"| Full buy (geral) | {pc(b('economia', recorte='full'))} |",
          f"| Eco (geral) | {pc(b('economia', recorte='eco'))} |",
          "", "### Concentração de first bloods (diagnóstico 5)", "",
          f"Fatia dos first bloods feitos pelo jogador que mais faz, em times com ≥{min_amostra} first bloods: "
          f"média da liga **{pc(fb_m)}**; esperado só por acaso **{pc(fb_acaso)}**; "
          f"75% dos times ficam abaixo de {pc(fb_p75)} e 90% abaixo de {pc(fb_p90)}. "
          "Um time só merece alerta bem acima desses valores.", "",
          "## Decisões em aberto", "",
          "- **Aliases de time** (`data/team_aliases.csv`): agrupar sub-times muda estes números.",
          f"- **Rounds após o pistol** ({n_apos}): ajustar `N_APOS_PISTOL` em `baseline.py` e rodar de novo.",
          "- **`tipo_economia`**: cortes provisórios em `pipeline.py` (afetam D4 e a tabela de economia).",
          ""]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(L), encoding="utf-8")


def rodar(processed: Path, docs: Path, min_amostra=MIN_AMOSTRA, n_apos=N_APOS_PISTOL):
    T = load_clean(processed)
    base = calcular_baseline(T, min_amostra, n_apos)
    viab = calcular_viabilidade(T, min_amostra, n_apos)
    base.to_csv(Path(processed) / "baseline_liga.csv", index=False)
    viab.to_csv(Path(processed) / "viabilidade_times.csv", index=False)
    escrever_inventario(viab, base, T, min_amostra, n_apos, Path(docs) / "inventario_viabilidade.md")
    print(f"OK: baseline ({len(base)} linhas), viabilidade ({viab.time.nunique()} times) | "
          f"corte={min_amostra}, rounds após pistol={n_apos}")
    return base, viab


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--min", type=int, default=MIN_AMOSTRA, dest="min_amostra")
    ap.add_argument("--apos-pistol", type=int, default=N_APOS_PISTOL, dest="n_apos")
    a = ap.parse_args()
    rodar(Path(a.processed), Path(a.docs), a.min_amostra, a.n_apos)


if __name__ == "__main__":
    main()
