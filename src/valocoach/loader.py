"""Interface para o resto da equipe: lê as tabelas já limpas.

    from valocoach.loader import load_clean
    T = load_clean()                 # lê data/processed
    rounds, kills = T["rounds"], T["kills"]

Para gerar/atualizar os dados:  python -m valocoach.pipeline
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

TABELAS = ("matches", "players", "rounds", "player_rounds", "kills")


def load_clean(processed_dir: str | Path = "data/processed") -> dict[str, pd.DataFrame]:
    d = Path(processed_dir)
    out = {}
    for t in TABELAS:
        f_csv, f_pq = d / f"{t}.csv", d / f"{t}.parquet"
        if f_pq.exists():
            out[t] = pd.read_parquet(f_pq)
        elif f_csv.exists():
            out[t] = pd.read_csv(f_csv, dtype={"match_id": str, "puuid": str, "jogo_num": str})
        else:
            raise FileNotFoundError(f"{t} não encontrado em {d}. Rode: python -m valocoach.pipeline")
    return out
