import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="VALOCOACH — Post-Match Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.html("""
<style>

.stApp {
    background:
        radial-gradient(circle at 80% 0%, rgba(124,58,237,.16), transparent 28%),
        radial-gradient(circle at 5% 35%, rgba(168,85,247,.07), transparent 23%),
        linear-gradient(180deg, #07070b 0%, #0a0a10 48%, #08080d 100%);
    color: #f4f4f5;
}

.main {
    background: transparent;
}

.block-container {
    max-width: 1480px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: #fff !important;
}

h1 {
    font-size: 2.25rem !important;
    font-weight: 850 !important;
    letter-spacing: -1.5px;
}

h2 {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -.8px;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 750 !important;
}

p {
    color: #a1a1aa;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0b11 0%, #08080d 100%);
    border-right: 1px solid rgba(168,85,247,.14);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}

.sidebar-logo {
    font-size: 1.55rem;
    font-weight: 900;
    letter-spacing: -1px;
    color: white;
}

.sidebar-logo span {
    color: #a855f7;
}

.sidebar-tag {
    margin-top: 5px;
    color: #71717a;
    font-size: .68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 700;
}

.sidebar-section {
    margin-top: 28px;
    margin-bottom: 8px;
    color: #52525b;
    font-size: .65rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 800;
}

.sidebar-status {
    margin-top: 22px;
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(168,85,247,.06);
    border: 1px solid rgba(168,85,247,.14);
}

.sidebar-status-title {
    color: #c084fc;
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 800;
}

.sidebar-status-text {
    color: #71717a;
    font-size: .72rem;
    margin-top: 5px;
    line-height: 1.45;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.topbar-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.topbar-brand {
    font-size: 1.05rem;
    font-weight: 900;
    color: #fff;
}

.topbar-brand span {
    color: #a855f7;
}

.topbar-badge,
.data-badge {
    padding: 5px 9px;
    border-radius: 999px;
    border: 1px solid rgba(168,85,247,.25);
    background: rgba(168,85,247,.07);
    color: #c084fc;
    font-size: .58rem;
    font-weight: 800;
    letter-spacing: 1px;
}

.data-badge {
    border-color: rgba(74,222,128,.22);
    background: rgba(74,222,128,.06);
    color: #86efac;
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 205px;
    padding: 34px 38px;
    margin-bottom: 22px;
    border-radius: 24px;
    background:
        linear-gradient(
            120deg,
            rgba(124,58,237,.23),
            rgba(20,17,29,.94) 45%,
            rgba(8,8,13,.98)
        );
    border: 1px solid rgba(168,85,247,.25);
    box-shadow:
        0 25px 70px rgba(0,0,0,.35),
        inset 0 1px 0 rgba(255,255,255,.03);
}

.hero::before {
    content: "";
    position: absolute;
    width: 400px;
    height: 400px;
    right: -130px;
    top: -210px;
    border-radius: 50%;
    background: rgba(168,85,247,.13);
    filter: blur(15px);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-eyebrow {
    color: #c084fc;
    font-size: .68rem;
    font-weight: 850;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    margin-top: 9px;
    font-size: 3rem;
    line-height: .98;
    font-weight: 950;
    letter-spacing: -2px;
    color: white;
}

.hero-title span {
    color: #a855f7;
}

.hero-subtitle {
    margin-top: 12px;
    max-width: 700px;
    color: #a1a1aa;
    font-size: .93rem;
    line-height: 1.6;
}

.hero-pills {
    display: flex;
    gap: 8px;
    margin-top: 18px;
}

.hero-pill {
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.07);
    color: #71717a;
    font-size: .62rem;
    font-weight: 700;
}

.section-kicker {
    margin-bottom: 7px;
    color: #71717a;
    font-size: .63rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 1.7px;
}

.control-bar {
    padding: 14px 16px;
    margin-bottom: 20px;
    background: rgba(17,17,24,.72);
    border: 1px solid #242432;
    border-radius: 15px;
}

.kpi-card {
    position: relative;
    overflow: hidden;
    padding: 20px;
    min-height: 125px;
    background:
        linear-gradient(
            145deg,
            rgba(24,24,34,.94),
            rgba(13,13,19,.98)
        );
    border: 1px solid #27272f;
    border-radius: 17px;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
    transition: .2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(168,85,247,.4);
}

.kpi-label {
    color: #71717a;
    font-size: .64rem;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.kpi-value {
    margin-top: 7px;
    color: #fff;
    font-size: 2.25rem;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -1.5px;
}

.kpi-description {
    margin-top: 8px;
    color: #52525b;
    font-size: .68rem;
}

.diagnosis-hero {
    position: relative;
    overflow: hidden;
    padding: 25px 28px;
    margin: 10px 0 18px;
    border-radius: 20px;
    background:
        linear-gradient(
            120deg,
            rgba(168,85,247,.14),
            rgba(17,17,24,.96) 52%
        );
    border: 1px solid rgba(168,85,247,.28);
}

.diagnosis-hero::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg,#c084fc,#7c3aed);
}

.diagnosis-kicker {
    color: #c084fc;
    font-size: .64rem;
    font-weight: 900;
    letter-spacing: 1.7px;
    text-transform: uppercase;
}

.diagnosis-title-big {
    margin-top: 8px;
    color: white;
    font-size: 1.5rem;
    font-weight: 900;
}

.diagnosis-description {
    margin-top: 7px;
    color: #71717a;
    font-size: .82rem;
    line-height: 1.5;
}

.diagnosis-number-card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(7,7,11,.48);
    border: 1px solid rgba(255,255,255,.06);
}

.diagnosis-number-label {
    color: #52525b;
    font-size: .61rem;
    font-weight: 800;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.diagnosis-number {
    margin-top: 5px;
    color: white;
    font-size: 2.15rem;
    font-weight: 900;
}

.danger {
    color: #f87171 !important;
}

.reference {
    color: #a78bfa !important;
}

.diff {
    color: #fb7185 !important;
}

.action-card {
    padding: 20px 22px;
    border-radius: 16px;
    background:
        linear-gradient(
            135deg,
            rgba(251,146,60,.08),
            rgba(17,17,24,.96)
        );
    border: 1px solid rgba(251,146,60,.18);
}

.action-label {
    color: #fb923c;
    font-size: .62rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.action-title {
    margin-top: 7px;
    color: #f4f4f5;
    font-size: 1rem;
    font-weight: 750;
}

.action-text {
    margin-top: 6px;
    color: #71717a;
    font-size: .76rem;
    line-height: 1.5;
}

.evidence-card {
    padding: 20px 22px;
    border-radius: 16px;
    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,.05),
            rgba(17,17,24,.96)
        );
    border: 1px solid rgba(34,197,94,.13);
}

.evidence-label {
    color: #86efac;
    font-size: .62rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.evidence-text {
    margin-top: 8px;
    color: #a1a1aa;
    font-size: .8rem;
    line-height: 1.55;
}

.diagnostic-card {
    padding: 22px;
    margin-bottom: 13px;
    background:
        linear-gradient(
            145deg,
            rgba(19,19,27,.98),
            rgba(11,11,16,.98)
        );
    border: 1px solid #27272f;
    border-radius: 17px;
}

.diagnostic-card-title {
    color: #f4f4f5;
    font-size: 1rem;
    font-weight: 800;
}

.priority-high {
    color: #f87171;
}

.priority-medium {
    color: #fbbf24;
}

.priority-low {
    color: #4ade80;
}

.map-hero {
    padding: 25px;
    border-radius: 20px;
    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,.13),
            rgba(17,17,24,.96)
        );
    border: 1px solid rgba(168,85,247,.20);
}

.map-name {
    color: white;
    font-size: 1.9rem;
    font-weight: 900;
}

.map-subtitle {
    margin-top: 5px;
    color: #71717a;
    font-size: .76rem;
}

.insight-strip {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 15px 17px;
    margin: 15px 0;
    background: rgba(168,85,247,.055);
    border: 1px solid rgba(168,85,247,.13);
    border-radius: 13px;
}

.insight-icon {
    font-size: 1.25rem;
}

.insight-text {
    color: #a1a1aa;
    font-size: .77rem;
    line-height: 1.45;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17,17,24,.75);
    border-color: #27272f !important;
    border-radius: 16px;
}

div[data-baseweb="select"] > div {
    background: #111118;
    border-color: #2f2f3a;
    border-radius: 10px;
}

button[data-baseweb="tab"] {
    color: #71717a !important;
    font-weight: 750 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #c084fc !important;
}

div[data-baseweb="tab-highlight"] {
    background: #a855f7 !important;
}

details {
    background: #111118 !important;
    border: 1px solid #27272f !important;
    border-radius: 12px !important;
}

hr {
    border-color: #20202a !important;
}

.footer {
    margin-top: 55px;
    padding: 25px 0 5px;
    border-top: 1px solid #20202a;
    text-align: center;
    color: #3f3f46;
    font-size: .68rem;
    letter-spacing: .5px;
}

.footer strong {
    color: #71717a;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""")


# ============================================================
# CAMINHOS / DADOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "processed"


# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================

def safe_pct(numerator, denominator):
    """Percentual seguro."""
    if denominator is None or denominator == 0:
        return None
    return float(numerator) / float(denominator) * 100


def fmt_pct(value, decimals=0):
    if value is None or pd.isna(value):
        return "—"
    return f"{value:.{decimals}f}%"


def fmt_pp(value, decimals=1):
    if value is None or pd.isna(value):
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{decimals}f} pp"


def fmt_int(value):
    """Inteiro com separador de milhar brasileiro (ponto)."""
    return f"{int(value):,}".replace(",", ".")


def pretty_name(value):
    if value is None:
        return "—"

    text = str(value).strip()

    if not text:
        return "—"

    replacements = {
        "azure_bears_black": "Azure Bears Black",
        "ufmt_turuna": "UFMT Turuna",
    }

    if text in replacements:
        return replacements[text]

    return text.replace("_", " ").replace("-", " ").title()


def normalize_bool(series):
    """
    Normaliza booleanos vindos dos CSVs.
    Aceita True/False, 1/0, sim/não etc.
    """
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)

    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "1.0": True,
        "0.0": False,
        "sim": True,
        "não": False,
        "nao": False,
        "yes": True,
        "no": False,
    }

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
        .fillna(False)
    )


def first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def html_escape(value):
    return html.escape(str(value))


def clean_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# ============================================================
# CARREGAMENTO
# ============================================================

@st.cache_data(show_spinner=False)
def load_data():
    required = [
        "matches.csv",
        "rounds.csv",
        "players.csv",
        "player_rounds.csv",
        "kills.csv",
    ]

    missing = [
        filename
        for filename in required
        if not (PROCESSED_DIR / filename).exists()
    ]

    if missing:
        raise FileNotFoundError(
            "Arquivos ausentes em processed/: "
            + ", ".join(missing)
        )

    matches = pd.read_csv(
        PROCESSED_DIR / "matches.csv",
        dtype={"match_id": str},
    )

    rounds = pd.read_csv(
        PROCESSED_DIR / "rounds.csv",
        dtype={"match_id": str},
    )

    players = pd.read_csv(
        PROCESSED_DIR / "players.csv",
        dtype={"match_id": str, "puuid": str},
    )

    player_rounds = pd.read_csv(
        PROCESSED_DIR / "player_rounds.csv",
        dtype={"match_id": str, "puuid": str},
    )

    kills = pd.read_csv(
        PROCESSED_DIR / "kills.csv",
        dtype={"match_id": str},
    )

    return matches, rounds, players, player_rounds, kills


try:
    matches, rounds, players, player_rounds, kills = load_data()
    data_error = None
except Exception as exc:
    data_error = str(exc)
    matches = pd.DataFrame()
    rounds = pd.DataFrame()
    players = pd.DataFrame()
    player_rounds = pd.DataFrame()
    kills = pd.DataFrame()


# ============================================================
# PREPARAÇÃO
# ============================================================

if data_error:
    st.error("Não foi possível carregar os dados reais.")
    st.code(data_error)
    st.info(
        "Verifique se os arquivos CSV estão em "
        "`processed/` dentro do projeto."
    )
    st.stop()


# Normalização básica
for df in [matches, rounds, players, player_rounds, kills]:
    if "match_id" in df.columns:
        df["match_id"] = df["match_id"].astype(str)


if "venceu" in rounds.columns:
    rounds["venceu"] = normalize_bool(rounds["venceu"])

if "pistol" in rounds.columns:
    rounds["pistol"] = normalize_bool(rounds["pistol"])

if "plant" in rounds.columns:
    rounds["plant"] = normalize_bool(rounds["plant"])

if "overtime" in matches.columns:
    matches["overtime"] = normalize_bool(matches["overtime"])

# Numeric columns
clean_numeric(
    matches,
    [
        "rounds_a",
        "rounds_b",
        "rounds_jogados",
        "duracao_s",
        "jogo_num",
    ],
)

clean_numeric(
    rounds,
    [
        "round",
        "plant_t_ms",
        "plant_x",
        "plant_y",
        "loadout_total",
        "loadout_medio",
        "loadout_adversario_medio",
        "gasto_total",
        "creditos_antes_medio",
    ],
)


# Junta mapa/campeonato aos rounds
match_context_cols = [
    col
    for col in [
        "match_id",
        "mapa",
        "campeonato",
        "fase",
        "data",
        "time_a",
        "time_b",
    ]
    if col in matches.columns
]

rounds_full = rounds.merge(
    matches[match_context_cols].drop_duplicates("match_id"),
    on="match_id",
    how="left",
    suffixes=("", "_match"),
)


# ============================================================
# EQUIPES E MAPAS
# ============================================================

teams = set()

if "time_a" in matches.columns:
    teams.update(matches["time_a"].dropna().astype(str))

if "time_b" in matches.columns:
    teams.update(matches["time_b"].dropna().astype(str))

if "time" in rounds_full.columns:
    teams.update(rounds_full["time"].dropna().astype(str))

teams = sorted(
    team
    for team in teams
    if team and team.lower() != "nan"
)

maps = sorted(
    matches["mapa"]
    .dropna()
    .astype(str)
    .unique()
) if "mapa" in matches.columns else []


if not teams:
    st.error("Nenhuma equipe foi encontrada nos dados reais.")
    st.stop()


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

# Traduz o rótulo da interface para o valor da coluna "lado"
CONTEXTO_PARA_LADO = {
    "ataque": "attacker",
    "defesa": "defender",
    "attacker": "attacker",
    "defender": "defender",
}


def team_rounds(team, contexto="Todos", mapa="Todos"):
    df = rounds_full.copy()

    if "time" not in df.columns:
        return df.iloc[0:0].copy()

    df = df[df["time"].astype(str) == str(team)]

    if contexto != "Todos" and "lado" in df.columns:
        lado = CONTEXTO_PARA_LADO.get(
            str(contexto).lower(),
            str(contexto).lower(),
        )
        df = df[df["lado"].astype(str).str.lower() == lado]

    if mapa != "Todos" and "mapa" in df.columns:
        df = df[df["mapa"].astype(str) == str(mapa)]

    return df.copy()


def team_match_count(team):
    if "time_a" not in matches.columns or "time_b" not in matches.columns:
        return 0

    return int(
        (
            (matches["time_a"].astype(str) == str(team))
            | (matches["time_b"].astype(str) == str(team))
        ).sum()
    )


def team_win_rate(team):
    if not {"time_a", "time_b", "vencedor"}.issubset(matches.columns):
        return None

    relevant = matches[
        (matches["time_a"].astype(str) == str(team))
        | (matches["time_b"].astype(str) == str(team))
    ].copy()

    if relevant.empty:
        return None

    wins = (relevant["vencedor"].astype(str) == str(team)).sum()
    return safe_pct(wins, len(relevant))


def side_win_rate(team, side, mapa="Todos"):
    df = team_rounds(team, side, mapa)

    if df.empty or "venceu" not in df.columns:
        return None, 0

    return safe_pct(df["venceu"].sum(), len(df)), len(df)


def pistol_rate(team, mapa="Todos"):
    df = team_rounds(team, "Todos", mapa)

    if df.empty or "pistol" not in df.columns:
        return None, 0

    df = df[df["pistol"]]

    if df.empty:
        return None, 0

    return safe_pct(df["venceu"].sum(), len(df)), len(df)


def economy_rates(team, mapa="Todos"):
    df = team_rounds(team, "Todos", mapa)

    if df.empty or "tipo_economia" not in df.columns:
        return {}

    df = df.copy()
    df["tipo_economia"] = (
        df["tipo_economia"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    result = {}

    for economy_type, group in df.groupby("tipo_economia"):
        if economy_type in {"nan", "", "none"}:
            continue

        result[economy_type] = {
            "rate": safe_pct(group["venceu"].sum(), len(group)),
            "n": len(group),
        }

    return result


def _after_pistol_values(df, pistol_won):
    """
    Resultados dos 2 rounds seguintes a cada pistol (ganho ou perdido),
    agrupando por partida (e por time, quando a coluna existe) para
    nunca atravessar partidas ou equipes.
    """
    required = {"match_id", "round", "pistol", "venceu"}

    if df.empty or not required.issubset(df.columns):
        return []

    group_cols = ["match_id"]
    if "time" in df.columns:
        group_cols.append("time")

    df = df.sort_values(group_cols + ["round"])

    values = []

    for _, group in df.groupby(group_cols, sort=False):
        group = group.reset_index(drop=True)

        pistol_indices = group.index[group["pistol"]].tolist()

        for idx in pistol_indices:
            if bool(group.loc[idx, "venceu"]) != pistol_won:
                continue

            next_rows = group.iloc[idx + 1: idx + 3]

            if next_rows.empty:
                continue

            values.extend(next_rows["venceu"].astype(bool).tolist())

    return values


def after_pistol_rate(team, pistol_won, mapa="Todos"):
    """
    Desempenho nas duas rodadas seguintes ao pistol.
    """
    df = team_rounds(team, "Todos", mapa)
    values = _after_pistol_values(df, pistol_won)

    if not values:
        return None, 0

    return safe_pct(sum(values), len(values)), len(values)


def league_side_rate(side, mapa="Todos"):
    df = rounds_full.copy()

    if mapa != "Todos" and "mapa" in df.columns:
        df = df[df["mapa"].astype(str) == str(mapa)]

    if "lado" in df.columns:
        df = df[
            df["lado"].astype(str).str.lower() == side.lower()
        ]

    if df.empty:
        return None, 0

    return safe_pct(df["venceu"].sum(), len(df)), len(df)


def league_pistol_rate(mapa="Todos"):
    df = rounds_full.copy()

    if mapa != "Todos" and "mapa" in df.columns:
        df = df[df["mapa"].astype(str) == str(mapa)]

    if "pistol" not in df.columns:
        return None, 0

    df = df[df["pistol"]]

    if df.empty:
        return None, 0

    return safe_pct(df["venceu"].sum(), len(df)), len(df)


def league_economy_rate(economy_type, mapa="Todos"):
    df = rounds_full.copy()

    if mapa != "Todos" and "mapa" in df.columns:
        df = df[df["mapa"].astype(str) == str(mapa)]

    if "tipo_economia" not in df.columns:
        return None, 0

    df["tipo_economia"] = (
        df["tipo_economia"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df = df[df["tipo_economia"] == str(economy_type).lower()]

    if df.empty:
        return None, 0

    return safe_pct(df["venceu"].sum(), len(df)), len(df)


def league_after_pistol_rate(pistol_won, mapa="Todos"):
    """
    Mesmo cálculo de recuperação/conversão,
    mas considerando todas as equipes da base.
    """
    df = rounds_full.copy()

    if mapa != "Todos" and "mapa" in df.columns:
        df = df[df["mapa"].astype(str) == str(mapa)]

    values = _after_pistol_values(df, pistol_won)

    if not values:
        return None, 0

    return safe_pct(sum(values), len(values)), len(values)


def map_metrics(team, mapa):
    df = team_rounds(team, "Todos", mapa)

    if df.empty:
        return {
            "win": None,
            "attack": None,
            "defense": None,
            "n": 0,
        }

    win = safe_pct(df["venceu"].sum(), len(df))

    attack = None
    defense = None

    if "lado" in df.columns:
        lado = df["lado"].astype(str).str.lower()

        attack = safe_pct(
            df.loc[lado == "attacker", "venceu"].sum(),
            (lado == "attacker").sum(),
        )

        defense = safe_pct(
            df.loc[lado == "defender", "venceu"].sum(),
            (lado == "defender").sum(),
        )

    return {
        "win": win,
        "attack": attack,
        "defense": defense,
        "n": len(df),
    }


# ============================================================
# DIAGNÓSTICOS REAIS
# ============================================================

def build_diagnostics(team, mapa="Todos"):
    diagnostics = []

    # --------------------------------------------------------
    # 1. Recuperação após perder pistol
    # --------------------------------------------------------

    recovery, recovery_n = after_pistol_rate(
        team,
        pistol_won=False,
        mapa=mapa,
    )

    recovery_ref, recovery_ref_n = league_after_pistol_rate(
        pistol_won=False,
        mapa=mapa,
    )

    if recovery is not None and recovery_ref is not None:
        gap = recovery - recovery_ref

        diagnostics.append({
            "titulo": "Recuperação após perder o pistol",
            "taxa": recovery,
            "referencia": recovery_ref,
            "gap": gap,
            "n": recovery_n,
            "ref_n": recovery_ref_n,
            "metrica": "Win Rate nos 2 rounds após perder pistol",
            "investigacao": (
                "Decisões econômicas e execução nos rounds "
                "seguintes ao pistol perdido"
            ),
            "evidencia": (
                f"{recovery:.1f}% de vitórias nos rounds seguintes, "
                f"contra {recovery_ref:.1f}% na base de referência."
            ),
        })

    # --------------------------------------------------------
    # 2. Conversão após ganhar pistol
    # --------------------------------------------------------

    conversion, conversion_n = after_pistol_rate(
        team,
        pistol_won=True,
        mapa=mapa,
    )

    conversion_ref, conversion_ref_n = league_after_pistol_rate(
        pistol_won=True,
        mapa=mapa,
    )

    if conversion is not None and conversion_ref is not None:
        gap = conversion - conversion_ref

        diagnostics.append({
            "titulo": "Conversão após ganhar o pistol",
            "taxa": conversion,
            "referencia": conversion_ref,
            "gap": gap,
            "n": conversion_n,
            "ref_n": conversion_ref_n,
            "metrica": "Win Rate nos 2 rounds após ganhar pistol",
            "investigacao": (
                "Conversão da vantagem econômica inicial "
                "nos rounds imediatamente seguintes"
            ),
            "evidencia": (
                f"{conversion:.1f}% de vitórias nos rounds seguintes, "
                f"contra {conversion_ref:.1f}% na referência."
            ),
        })

    # --------------------------------------------------------
    # 3. Ataque x Defesa
    # --------------------------------------------------------

    attack, attack_n = side_win_rate(team, "Attacker", mapa)
    defense, defense_n = side_win_rate(team, "Defender", mapa)

    league_attack, league_attack_n = league_side_rate("Attacker", mapa)
    league_defense, league_defense_n = league_side_rate("Defender", mapa)

    if defense is not None and league_defense is not None:
        gap = defense - league_defense

        diagnostics.append({
            "titulo": "Desempenho defensivo",
            "taxa": defense,
            "referencia": league_defense,
            "gap": gap,
            "n": defense_n,
            "ref_n": league_defense_n,
            "metrica": "Win Rate na defesa",
            "investigacao": (
                "Padrões de adaptação e resposta às entradas "
                "adversárias no lado defensor"
            ),
            "evidencia": (
                f"{defense:.1f}% de Win Rate na defesa, "
                f"contra {league_defense:.1f}% na referência."
            ),
        })

    if attack is not None and league_attack is not None:
        gap = attack - league_attack

        diagnostics.append({
            "titulo": "Desempenho ofensivo",
            "taxa": attack,
            "referencia": league_attack,
            "gap": gap,
            "n": attack_n,
            "ref_n": league_attack_n,
            "metrica": "Win Rate no ataque",
            "investigacao": (
                "Execução das entradas e conversão das vantagens "
                "criadas no lado atacante"
            ),
            "evidencia": (
                f"{attack:.1f}% de Win Rate no ataque, "
                f"contra {league_attack:.1f}% na referência."
            ),
        })

    # --------------------------------------------------------
    # 4. Force Buy
    # --------------------------------------------------------

    economy_local = economy_rates(team, mapa)

    force_key_local = None

    for key in economy_local:
        normalized = key.replace(" ", "_").replace("-", "_")

        if normalized in {"force", "force_buy", "forcebuy"}:
            force_key_local = key
            break

    if force_key_local is not None:
        force_rate = economy_local[force_key_local]["rate"]
        force_n = economy_local[force_key_local]["n"]

        force_ref, force_ref_n = league_economy_rate(
            force_key_local,
            mapa,
        )

        if force_ref is not None and force_rate is not None:
            gap = force_rate - force_ref

            diagnostics.append({
                "titulo": "Eficiência em Force Buy",
                "taxa": force_rate,
                "referencia": force_ref,
                "gap": gap,
                "n": force_n,
                "ref_n": force_ref_n,
                "metrica": "Win Rate em Force Buy",
                "investigacao": (
                    "Relação entre investimento antecipado "
                    "e capacidade de converter a rodada"
                ),
                "evidencia": (
                    f"{force_rate:.1f}% de vitórias em Force Buy, "
                    f"contra {force_ref:.1f}% na referência."
                ),
            })

    # --------------------------------------------------------
    # Prioridade
    # Só desvios ABAIXO da referência são pontos de atenção;
    # indicadores acima da referência ficam com prioridade baixa.
    # --------------------------------------------------------

    for d in diagnostics:
        shortfall = max(-d["gap"], 0)

        if d["n"] >= 80:
            confidence = 3
        elif d["n"] >= 30:
            confidence = 2
        else:
            confidence = 1

        if shortfall >= 12:
            impact = 3
        elif shortfall >= 6:
            impact = 2
        elif shortfall > 0:
            impact = 1
        else:
            impact = 0

        score = impact * confidence
        d["score"] = score

        if score >= 6:
            d["prioridade"] = "Alta"
        elif score >= 3:
            d["prioridade"] = "Média"
        else:
            d["prioridade"] = "Baixa"

    # Mais relevante primeiro (maior déficit em caso de empate)
    diagnostics.sort(
        key=lambda x: (
            -x["score"],
            x["gap"],
        )
    )

    return diagnostics


# ============================================================
# HEATMAP / COORDENADAS
# ============================================================

def find_coordinate_columns(df):
    x_candidates = [
        "victim_x",
        "kill_x",
        "x",
        "pos_x",
        "position_x",
        "killer_x",
        "plant_x",
    ]

    y_candidates = [
        "victim_y",
        "kill_y",
        "y",
        "pos_y",
        "position_y",
        "killer_y",
        "plant_y",
    ]

    x_col = first_existing_column(df, x_candidates)
    y_col = first_existing_column(df, y_candidates)

    return x_col, y_col


def find_kill_team_column(df):
    candidates = [
        "killer_team",
        "time_killer",
        "killer_time",
        "team_killer",
        "time",
        "team",
        "equipe",
    ]

    return first_existing_column(df, candidates)


def make_heatmap(team, mapa):
    if kills.empty:
        return None, "kills.csv está vazio."

    x_col, y_col = find_coordinate_columns(kills)

    if x_col is None or y_col is None:
        return None, (
            "As coordenadas espaciais não foram identificadas "
            "automaticamente no arquivo kills.csv."
        )

    df = kills.copy()

    if "match_id" in df.columns and mapa != "Todos":
        map_ids = set(
            matches.loc[
                matches["mapa"].astype(str) == str(mapa),
                "match_id",
            ].astype(str)
        )

        df = df[df["match_id"].astype(str).isin(map_ids)]

    team_col = find_kill_team_column(df)

    if team_col is not None:
        df = df[
            df[team_col].astype(str).str.lower()
            == str(team).lower()
        ]

    df = df.copy()
    df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")

    df = df.dropna(subset=[x_col, y_col])

    if df.empty:
        return None, (
            "Não foram encontrados eventos espaciais "
            "para a equipe e filtro selecionados."
        )

    return df, None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-logo">
        VALO<span>COACH</span>
    </div>
    <div class="sidebar-tag">
        Post-match intelligence
    </div>
    """)

    st.html("""
    <div class="sidebar-section">
        Análise
    </div>
    """)

    # Equipe com maior número de partidas como padrão
    team_counts = {
        team_value: team_match_count(team_value)
        for team_value in teams
    }

    default_team = max(
        teams,
        key=lambda x: team_counts.get(x, 0),
    )

    time = st.selectbox(
        "Equipe analisada",
        teams,
        index=teams.index(default_team),
        format_func=pretty_name,
    )

    contexto = st.selectbox(
        "Contexto",
        ["Todos", "Ataque", "Defesa"],
    )

    mapa_filtro_options = ["Todos"] + maps

    mapa_filtro = st.selectbox(
        "Mapa",
        mapa_filtro_options,
        format_func=pretty_name,
    )

    st.html(f"""
    <div class="sidebar-status">
        <div class="sidebar-status-title">
            ● Dados reais conectados
        </div>
        <div class="sidebar-status-text">
            {fmt_int(len(matches))} partidas ·
            {fmt_int(len(rounds))} registros de rounds ·
            {fmt_int(len(kills))} eventos de combate
        </div>
    </div>
    """)


# ============================================================
# MÉTRICAS DA EQUIPE SELECIONADA
# ============================================================

selected_rounds = team_rounds(
    time,
    contexto,
    mapa_filtro,
)

win_rate = team_win_rate(time)

if contexto == "Ataque":
    ataque, ataque_n = side_win_rate(time, "Attacker", mapa_filtro)
    defesa = None
    defesa_n = 0

elif contexto == "Defesa":
    ataque = None
    ataque_n = 0
    defesa, defesa_n = side_win_rate(time, "Defender", mapa_filtro)

else:
    ataque, ataque_n = side_win_rate(time, "Attacker", mapa_filtro)
    defesa, defesa_n = side_win_rate(time, "Defender", mapa_filtro)


pistol, pistol_n = pistol_rate(time, mapa_filtro)

economy = economy_rates(
    time,
    mapa_filtro,
)

recovery, recovery_n = after_pistol_rate(
    time,
    pistol_won=False,
    mapa=mapa_filtro,
)

recovery_ref, recovery_ref_n = league_after_pistol_rate(
    pistol_won=False,
    mapa=mapa_filtro,
)

conversion, conversion_n = after_pistol_rate(
    time,
    pistol_won=True,
    mapa=mapa_filtro,
)

conversion_ref, conversion_ref_n = league_after_pistol_rate(
    pistol_won=True,
    mapa=mapa_filtro,
)


# ============================================================
# PRINCIPAL DIAGNÓSTICO
# ============================================================

diagnosticos = build_diagnostics(
    time,
    mapa_filtro,
)

if diagnosticos:
    principal = diagnosticos[0]
else:
    principal = {
        "titulo": "Dados insuficientes para diagnóstico",
        "taxa": None,
        "referencia": None,
        "gap": None,
        "n": 0,
        "metrica": "—",
        "investigacao": "Aumentar a amostra disponível para análise.",
        "evidencia": (
            "Não há dados suficientes para gerar um diagnóstico "
            "comparativo confiável."
        ),
        "prioridade": "Baixa",
        "score": 0,
    }


problema = principal["titulo"]
taxa_problema = principal["taxa"]
referencia = principal["referencia"]
diferenca = principal["gap"]
investigacao = principal["investigacao"]
evidencia = principal["evidencia"]


if win_rate is None:
    status = "AMOSTRA INSUFICIENTE"
elif win_rate >= 60:
    status = "DESEMPENHO POSITIVO"
elif win_rate >= 50:
    status = "DESEMPENHO INTERMEDIÁRIO"
else:
    status = "PONTO DE ATENÇÃO"


# ============================================================
# TOP BAR
# ============================================================

st.html("""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-brand">
            VALO<span>COACH</span>
        </div>
        <div class="topbar-badge">
            ANALYTICS
        </div>
        <div class="data-badge">
            ● DADOS REAIS
        </div>
    </div>
</div>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">
    <div class="hero-content">

        <div class="hero-eyebrow">
            Competitive performance intelligence
        </div>

        <div class="hero-title">
            Entenda o jogo.<br>
            <span>Encontre o padrão.</span>
        </div>

        <div class="hero-subtitle">
            O VALOCOACH transforma dados de partidas em
            diagnósticos, evidências e pontos objetivos
            para investigação pós-jogo.
            Agora utilizando diretamente a base processada
            do hackathon.
        </div>

        <div class="hero-pills">
            <div class="hero-pill">POST-MATCH</div>
            <div class="hero-pill">DATA-DRIVEN</div>
            <div class="hero-pill">REAL DATA</div>
            <div class="hero-pill">COACHING INTELLIGENCE</div>
        </div>

    </div>
</div>
""")


# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3, aba4 = st.tabs([
    "COMMAND CENTER",
    "DIAGNÓSTICOS",
    "ECONOMIA",
    "MAPAS",
])


def style_bar_figure(fig, colors="#8b5cf6"):
    fig.update_traces(
        texttemplate="%{text:.0f}%",
        textposition="outside",
        marker_color=colors,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a1a1aa"),
        yaxis=dict(title="", gridcolor="#27272f"),
        xaxis=dict(title=""),
        showlegend=False,
        margin=dict(l=10, r=10, t=25, b=10),
    )

    return fig


# ============================================================
# COMMAND CENTER
# ============================================================

with aba1:

    st.html("""
    <div class="section-kicker">
        Visão executiva
    </div>
    """)

    st.header(
        f"{pretty_name(time)} · Command Center"
    )

    st.html(f"""
    <div class="control-bar">

        <b style="color:#e4e4e7;">
            Contexto analisado:
        </b>

        <span style="color:#a855f7;">
            {html_escape(contexto)}
        </span>

        <span style="color:#52525b; margin-left:12px;">
            •
        </span>

        <span style="color:#71717a; margin-left:12px;">
            Mapa: {html_escape(pretty_name(mapa_filtro))}
        </span>

        <span style="color:#52525b; margin-left:12px;">
            •
        </span>

        <span style="color:#71717a; margin-left:12px;">
            Status: {status}
        </span>

    </div>
    """)

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">Win Rate</div>
            <div class="kpi-value">{fmt_pct(win_rate)}</div>
            <div class="kpi-description">
                {team_match_count(time)} partidas analisadas
            </div>
        </div>
        """)

    with col2:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">Ataque</div>
            <div class="kpi-value">{fmt_pct(ataque)}</div>
            <div class="kpi-description">
                {fmt_int(ataque_n)} rounds
            </div>
        </div>
        """)

    with col3:
        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">Defesa</div>
            <div class="kpi-value">{fmt_pct(defesa)}</div>
            <div class="kpi-description">
                {fmt_int(defesa_n)} rounds
            </div>
        </div>
        """)

    with col4:
        gap_text = (
            fmt_pp(diferenca)
            if diferenca is not None
            else "—"
        )

        st.html(f"""
        <div class="kpi-card">
            <div class="kpi-label">Gap diagnóstico</div>
            <div class="kpi-value">{gap_text}</div>
            <div class="kpi-description">
                observado × referência
            </div>
        </div>
        """)

    st.html("<br>")

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if win_rate is None:
        st.info(
            "A amostra disponível não permite calcular um "
            "Win Rate confiável para a equipe."
        )

    elif win_rate >= 60:
        st.success(
            f"🟢 {pretty_name(time)} apresenta "
            f"{win_rate:.1f}% de Win Rate nas partidas disponíveis."
        )

    elif win_rate >= 50:
        st.info(
            f"🟡 {pretty_name(time)} apresenta "
            f"{win_rate:.1f}% de Win Rate nas partidas disponíveis."
        )

    else:
        st.warning(
            f"🔴 {pretty_name(time)} apresenta "
            f"{win_rate:.1f}% de Win Rate nas partidas disponíveis."
        )

    st.html("<br>")

    # --------------------------------------------------------
    # DIAGNÓSTICO PRINCIPAL
    # --------------------------------------------------------

    st.html("""
    <div class="section-kicker">
        Insight prioritário
    </div>
    """)

    st.html(f"""
    <div class="diagnosis-hero">

        <div class="diagnosis-kicker">
            ⚠ Principal ponto de atenção
        </div>

        <div class="diagnosis-title-big">
            {html_escape(problema)}
        </div>

        <div class="diagnosis-description">
            O indicador foi priorizado a partir do desvio
            observado e do tamanho da amostra.
            Ele representa um contexto para investigação,
            não uma causa comprovada.
        </div>

    </div>
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        classe = (
            "danger"
            if (
                taxa_problema is not None
                and referencia is not None
                and taxa_problema < referencia
            )
            else ""
        )

        st.html(f"""
        <div class="diagnosis-number-card">
            <div class="diagnosis-number-label">
                Resultado observado
            </div>
            <div class="diagnosis-number {classe}">
                {fmt_pct(taxa_problema, 1)}
            </div>
        </div>
        """)

    with col2:
        st.html(f"""
        <div class="diagnosis-number-card">
            <div class="diagnosis-number-label">
                Referência da base
            </div>
            <div class="diagnosis-number reference">
                {fmt_pct(referencia, 1)}
            </div>
        </div>
        """)

    with col3:
        st.html(f"""
        <div class="diagnosis-number-card">
            <div class="diagnosis-number-label">
                Gap identificado
            </div>
            <div class="diagnosis-number diff">
                {fmt_pp(diferenca)}
            </div>
        </div>
        """)

    st.html("<br>")

    # --------------------------------------------------------
    # EVIDÊNCIA / AÇÃO
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.html(f"""
        <div class="evidence-card">

            <div class="evidence-label">
                🔎 Evidência encontrada
            </div>

            <div class="evidence-text">
                {html_escape(evidencia)}
                <br><br>
                <span style="color:#52525b;">
                    Amostra da equipe: {principal["n"]} observações.
                </span>
            </div>

        </div>
        """)

    with col2:
        st.html(f"""
        <div class="action-card">

            <div class="action-label">
                🧭 Onde olhar primeiro
            </div>

            <div class="action-title">
                {html_escape(investigacao)}
            </div>

            <div class="action-text">
                O indicador não determina sozinho a causa.
                Ele aponta um contexto prioritário para
                investigação pelo coach ou jogador.
            </div>

        </div>
        """)

    st.html("<br>")

    # --------------------------------------------------------
    # GRÁFICO DE CONTEXTO
    # --------------------------------------------------------

    col1, col2 = st.columns([1.35, 1])

    with col1:

        st.html("""
        <div class="section-kicker">
            Performance
        </div>
        """)

        st.subheader("Desempenho por contexto")

        chart_data = pd.DataFrame({
            "Indicador": [
                "Win Rate",
                "Ataque",
                "Defesa",
            ],
            "Valor": [
                win_rate,
                ataque,
                defesa,
            ],
        }).dropna()

        if not chart_data.empty:

            fig = px.bar(
                chart_data,
                x="Indicador",
                y="Valor",
                range_y=[0, 100],
                text="Valor",
            )

            st.plotly_chart(
                style_bar_figure(fig),
                width="stretch",
            )

        else:
            st.info("Não há dados suficientes para este gráfico.")

    with col2:

        st.html("""
        <div class="section-kicker">
            Diagnóstico
        </div>
        """)

        st.subheader("Resultado × referência")

        if taxa_problema is not None and referencia is not None:

            comparison = pd.DataFrame({
                "Indicador": [
                    "Observado",
                    "Referência",
                ],
                "Valor": [
                    taxa_problema,
                    referencia,
                ],
            })

            fig2 = px.bar(
                comparison,
                x="Indicador",
                y="Valor",
                range_y=[0, 100],
                text="Valor",
            )

            st.plotly_chart(
                style_bar_figure(fig2, ["#ef4444", "#8b5cf6"]),
                width="stretch",
            )

        else:
            st.info(
                "Não há referência suficiente para comparar."
            )

    # --------------------------------------------------------
    # LEITURA EXECUTIVA
    # --------------------------------------------------------

    st.html("""
    <div class="insight-strip">

        <div class="insight-icon">
            🧠
        </div>

        <div class="insight-text">

            <strong style="color:#e4e4e7;">
                Leitura executiva:
            </strong>

            o VALOCOACH não apenas mostra percentuais.
            Ele compara o comportamento da equipe com a base,
            mede o desvio e transforma esse desvio em um
            ponto objetivo para investigação.

        </div>

    </div>
    """)


# ============================================================
# DIAGNÓSTICOS
# ============================================================

with aba2:

    st.html("""
    <div class="section-kicker">
        Pattern detection
    </div>
    """)

    st.header("Diagnósticos")

    st.write(
        "Pontos de atenção priorizados a partir dos padrões "
        "observados nas partidas reais."
    )

    if not diagnosticos:
        st.warning(
            "Não há amostra suficiente para gerar diagnósticos "
            "comparativos."
        )
    else:

        altas = sum(d["prioridade"] == "Alta" for d in diagnosticos)
        medias = sum(d["prioridade"] == "Média" for d in diagnosticos)
        baixas = sum(d["prioridade"] == "Baixa" for d in diagnosticos)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔴 Alta", altas)

        with col2:
            st.metric("🟡 Média", medias)

        with col3:
            st.metric("🟢 Baixa", baixas)

        st.html("<br>")

        filtro = st.selectbox(
            "Prioridade",
            ["Todos", "Alta", "Média", "Baixa"],
            key="diagnostico_filtro",
        )

        for diagnostico in diagnosticos:

            if (
                filtro != "Todos"
                and diagnostico["prioridade"] != filtro
            ):
                continue

            prioridade = diagnostico["prioridade"]

            if prioridade == "Alta":
                classe = "priority-high"
            elif prioridade == "Média":
                classe = "priority-medium"
            else:
                classe = "priority-low"

            st.html(f"""
            <div class="diagnostic-card">

                <div class="diagnostic-card-title">
                    {html_escape(diagnostico["titulo"])}
                </div>

                <div
                    style="
                        margin-top:7px;
                        font-size:.67rem;
                        font-weight:850;
                        text-transform:uppercase;
                        letter-spacing:1px;
                    "
                    class="{classe}"
                >
                    ● PRIORIDADE {prioridade.upper()}
                </div>

            </div>
            """)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    diagnostico["metrica"],
                    fmt_pct(diagnostico["taxa"], 1),
                )

            with col2:
                st.metric(
                    "Referência",
                    fmt_pct(diagnostico["referencia"], 1),
                )

            with col3:
                st.metric(
                    "Gap",
                    fmt_pp(diagnostico["gap"]),
                )

            col1, col2 = st.columns(2)

            with col1:
                st.html(f"""
                <div class="action-card">

                    <div class="action-label">
                        🧭 INVESTIGAR
                    </div>

                    <div class="action-title">
                        {html_escape(diagnostico["investigacao"])}
                    </div>

                </div>
                """)

            with col2:
                st.html(f"""
                <div class="evidence-card">

                    <div class="evidence-label">
                        🔎 EVIDÊNCIA
                    </div>

                    <div class="evidence-text">
                        {html_escape(diagnostico["evidencia"])}
                        <br><br>
                        <span style="color:#52525b;">
                            Amostra: {diagnostico["n"]}
                            observações.
                        </span>
                    </div>

                </div>
                """)

            st.html("<br>")


# ============================================================
# ECONOMIA
# ============================================================

with aba3:

    st.html("""
    <div class="section-kicker">
        Economic intelligence
    </div>
    """)

    st.header("Economia")

    st.write(
        "Entenda como o contexto econômico se relaciona "
        "com o resultado das rodadas."
    )

    def find_economy_key(possible):
        for key in economy:
            normalized = (
                key.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if normalized in possible:
                return key
        return None

    pistol_key = find_economy_key({"pistol"})
    eco_key = find_economy_key({"eco"})
    force_key = find_economy_key(
        {"force", "force_buy", "forcebuy"}
    )
    full_buy_key = find_economy_key(
        {"full_buy", "fullbuy", "full"}
    )

    metricas_economia = [
        (
            "Pistol",
            economy[pistol_key]["rate"]
            if pistol_key else pistol,
            "Início de rodada",
        ),
        (
            "Recuperação",
            recovery,
            "Após perder pistol",
        ),
        (
            "Conversão",
            conversion,
            "Após ganhar pistol",
        ),
        (
            "Force Buy",
            economy[force_key]["rate"]
            if force_key else None,
            "Investimento forçado",
        ),
    ]

    col1, col2, col3, col4 = st.columns(4)

    for coluna, (nome, valor, descricao) in zip(
        [col1, col2, col3, col4],
        metricas_economia,
    ):

        with coluna:

            st.html(f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    {nome}
                </div>

                <div class="kpi-value">
                    {fmt_pct(valor)}
                </div>

                <div class="kpi-description">
                    {descricao}
                </div>

            </div>
            """)

    st.html("<br>")

    # --------------------------------------------------------
    # Gráfico de economia
    # --------------------------------------------------------

    col1, col2 = st.columns([1.4, 1])

    economia_rows = []

    labels = [
        ("Pistol", pistol_key),
        ("Eco", eco_key),
        ("Force Buy", force_key),
        ("Full Buy", full_buy_key),
    ]

    for label, key in labels:
        if key and key in economy:
            economia_rows.append({
                "Situação": label,
                "Win Rate": economy[key]["rate"],
                "Amostra": economy[key]["n"],
            })

    economia_df = pd.DataFrame(
        economia_rows,
        columns=["Situação", "Win Rate", "Amostra"],
    )

    with col1:

        st.html("""
        <div class="section-kicker">
            Performance econômica
        </div>
        """)

        if not economia_df.empty:

            fig_economia = px.bar(
                economia_df,
                x="Situação",
                y="Win Rate",
                range_y=[0, 100],
                text="Win Rate",
                custom_data=["Amostra"],
            )

            style_bar_figure(fig_economia)

            fig_economia.update_traces(
                hovertemplate=(
                    "%{x}<br>"
                    "Win Rate: %{y:.1f}%<br>"
                    "Amostra: %{customdata[0]} rounds"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                fig_economia,
                width="stretch",
            )

        else:
            st.info(
                "O campo de economia não possui categorias "
                "suficientes para gerar o gráfico."
            )

    # --------------------------------------------------------
    # Diagnóstico econômico
    # --------------------------------------------------------

    with col2:

        st.html("""
        <div class="section-kicker">
            Diagnóstico econômico
        </div>
        """)

        if recovery is not None:

            st.html(f"""
            <div class="diagnosis-hero">

                <div class="diagnosis-kicker">
                    ⚠ Contexto prioritário
                </div>

                <div class="diagnosis-title-big">
                    Recuperação pós-pistol
                </div>

                <div class="diagnosis-description">
                    {recovery:.1f}% de Win Rate nos
                    rounds seguintes ao pistol perdido.
                    Referência: {fmt_pct(recovery_ref, 1)}.
                </div>

            </div>
            """)

            if (
                recovery_ref is not None
                and recovery < recovery_ref
            ):
                st.warning(
                    "A recuperação está abaixo da referência "
                    "observada na base."
                )
            else:
                st.success(
                    "A recuperação não está abaixo da referência "
                    "observada na base."
                )

        else:
            st.info(
                "A amostra de rounds após pistols perdidos "
                "não é suficiente."
            )

    # --------------------------------------------------------
    # Tabela compacta
    # --------------------------------------------------------

    st.html("<br>")

    if not economia_df.empty:

        st.subheader("Detalhamento por situação")

        display_df = economia_df.copy()

        display_df["Win Rate"] = display_df[
            "Win Rate"
        ].map(lambda x: f"{x:.1f}%")

        display_df = display_df.rename(
            columns={
                "Situação": "Situação econômica",
                "Amostra": "Rounds",
            }
        )

        st.dataframe(
            display_df,
            hide_index=True,
            width="stretch",
        )

    st.html("""
    <div class="insight-strip">

        <div class="insight-icon">
            💡
        </div>

        <div class="insight-text">

            <strong style="color:#e4e4e7;">
                O que investigar:
            </strong>

            como as escolhas econômicas aparecem associadas
            ao resultado dos rounds, especialmente nos momentos
            de recuperação após um pistol perdido.

        </div>

    </div>
    """)


# ============================================================
# MAPAS
# ============================================================

with aba4:

    st.html("""
    <div class="section-kicker">
        Spatial intelligence
    </div>
    """)

    st.header("Mapas")

    st.write(
        "Explore padrões de desempenho e evidências espaciais "
        "a partir dos dados reais de partida."
    )

    if not maps:
        st.warning("Nenhum mapa foi encontrado nos dados.")
    else:

        mapa_selecionado = st.selectbox(
            "Mapa analisado",
            maps,
            format_func=pretty_name,
            key="mapa_aba",
        )

        mapa_data = map_metrics(
            time,
            mapa_selecionado,
        )

        st.html(f"""
        <div class="map-hero">

            <div class="map-name">
                {html_escape(pretty_name(mapa_selecionado))}
            </div>

            <div class="map-subtitle">
                Performance por contexto tático ·
                {mapa_data["n"]} rounds da equipe
            </div>

        </div>
        """)

        st.html("<br>")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.html(f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    Win Rate
                </div>

                <div class="kpi-value">
                    {fmt_pct(mapa_data["win"])}
                </div>

                <div class="kpi-description">
                    Resultado no mapa
                </div>

            </div>
            """)

        with col2:
            st.html(f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    Ataque
                </div>

                <div class="kpi-value">
                    {fmt_pct(mapa_data["attack"])}
                </div>

                <div class="kpi-description">
                    Performance ofensiva
                </div>

            </div>
            """)

        with col3:
            st.html(f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    Defesa
                </div>

                <div class="kpi-value">
                    {fmt_pct(mapa_data["defense"])}
                </div>

                <div class="kpi-description">
                    Performance defensiva
                </div>

            </div>
            """)

        st.html("<br>")

        # ----------------------------------------------------
        # Performance no mapa
        # ----------------------------------------------------

        col1, col2 = st.columns([1.25, 1])

        with col1:

            map_chart_data = pd.DataFrame({
                "Contexto": [
                    "Win Rate",
                    "Ataque",
                    "Defesa",
                ],
                "Valor": [
                    mapa_data["win"],
                    mapa_data["attack"],
                    mapa_data["defense"],
                ],
            }).dropna()

            if not map_chart_data.empty:

                fig_mapa = px.bar(
                    map_chart_data,
                    x="Contexto",
                    y="Valor",
                    range_y=[0, 100],
                    text="Valor",
                )

                st.plotly_chart(
                    style_bar_figure(fig_mapa),
                    width="stretch",
                )

            else:
                st.info("Não há dados suficientes para este mapa.")

        # ----------------------------------------------------
        # Leitura tática
        # ----------------------------------------------------

        with col2:

            st.html("""
            <div class="section-kicker">
                Leitura tática
            </div>
            """)

            ataque_mapa = mapa_data["attack"]
            defesa_mapa = mapa_data["defense"]

            if ataque_mapa is None or defesa_mapa is None:
                leitura = (
                    "Não há amostra suficiente para comparar "
                    "ataque e defesa neste mapa."
                )

            elif ataque_mapa > defesa_mapa:
                leitura = (
                    f"O time apresenta melhor desempenho no "
                    f"ataque ({ataque_mapa:.1f}%) do que na defesa "
                    f"({defesa_mapa:.1f}%)."
                )

            elif defesa_mapa > ataque_mapa:
                leitura = (
                    f"O time apresenta melhor desempenho na "
                    f"defesa ({defesa_mapa:.1f}%) do que no ataque "
                    f"({ataque_mapa:.1f}%)."
                )

            else:
                leitura = (
                    "O desempenho está equilibrado entre "
                    "ataque e defesa."
                )

            st.html(f"""
            <div class="evidence-card">

                <div class="evidence-label">
                    🧠 INSIGHT
                </div>

                <div class="evidence-text">
                    {html_escape(leitura)}
                </div>

            </div>
            """)

        st.html("<br>")

        # ----------------------------------------------------
        # HEATMAP REAL
        # ----------------------------------------------------

        st.html("""
        <div class="section-kicker">
            Evidência espacial
        </div>
        """)

        st.subheader(
            f"Eventos espaciais · {pretty_name(mapa_selecionado)}"
        )

        heatmap_df, heatmap_error = make_heatmap(
            time,
            mapa_selecionado,
        )

        if heatmap_df is not None:

            x_col, y_col = find_coordinate_columns(
                heatmap_df
            )

            fig_heat = px.density_heatmap(
                heatmap_df,
                x=x_col,
                y=y_col,
                nbinsx=30,
                nbinsy=30,
            )

            fig_heat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(8,8,13,.95)",
                font=dict(color="#a1a1aa"),
                xaxis=dict(
                    title="Coordenada X",
                    gridcolor="#27272f",
                ),
                yaxis=dict(
                    title="Coordenada Y",
                    gridcolor="#27272f",
                    scaleanchor="x",
                    scaleratio=1,
                ),
                margin=dict(l=10, r=10, t=20, b=10),
            )

            st.plotly_chart(
                fig_heat,
                width="stretch",
            )

            st.html(f"""
            <div class="insight-strip">

                <div class="insight-icon">
                    🗺️
                </div>

                <div class="insight-text">

                    <strong style="color:#e4e4e7;">
                        Evidência espacial:
                    </strong>

                    o mapa acima usa eventos reais disponíveis
                    no dataset e permite observar onde os eventos
                    de combate da equipe se concentram.

                    <br>

                    <span style="color:#52525b;">
                        {len(heatmap_df)} eventos com coordenadas
                        válidas foram utilizados.
                    </span>

                </div>

            </div>
            """)

        else:

            st.html(f"""
            <div class="action-card">

                <div class="action-label">
                    🔥 EVIDÊNCIA ESPACIAL
                </div>

                <div class="action-title">
                    Heatmap indisponível para este filtro
                </div>

                <div class="action-text">
                    {html_escape(heatmap_error)}
                </div>

            </div>
            """)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    <strong>VALOCOACH</strong>
    &nbsp;•&nbsp;
    Post-Match Intelligence
    &nbsp;•&nbsp;
    Transformando dados de partida em decisões.

</div>
""")