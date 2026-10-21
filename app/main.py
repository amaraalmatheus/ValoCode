import streamlit as st
import plotly.express as px


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="VALOCOACH — Post-Match Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.html("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 78% 0%,
            rgba(124, 58, 237, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 35%,
            rgba(168, 85, 247, 0.08),
            transparent 22%
        ),
        linear-gradient(
            180deg,
            #07070b 0%,
            #0a0a10 45%,
            #08080d 100%
        );
    color: #f4f4f5;
}

.main {
    background: transparent;
}

.block-container {
    max-width: 1480px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* =========================================================
   TIPOGRAFIA
   ========================================================= */

h1, h2, h3, h4 {
    color: #ffffff !important;
}

h1 {
    font-size: 2.3rem !important;
    font-weight: 850 !important;
    letter-spacing: -1.5px;
}

h2 {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 750 !important;
}

p {
    color: #a1a1aa;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b0b11 0%,
            #08080d 100%
        );
    border-right: 1px solid rgba(168, 85, 247, 0.14);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
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
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 700;
}

.sidebar-section {
    margin-top: 30px;
    margin-bottom: 8px;
    color: #52525b;
    font-size: 0.65rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 800;
}

.sidebar-status {
    margin-top: 25px;
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(168, 85, 247, 0.06);
    border: 1px solid rgba(168, 85, 247, 0.14);
}

.sidebar-status-title {
    color: #c084fc;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 800;
}

.sidebar-status-text {
    color: #71717a;
    font-size: 0.75rem;
    margin-top: 5px;
}


/* =========================================================
   TOP BAR
   ========================================================= */

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
    color: #ffffff;
    letter-spacing: -0.5px;
}

.topbar-brand span {
    color: #a855f7;
}

.topbar-badge {
    padding: 5px 9px;
    border-radius: 999px;
    border: 1px solid rgba(168, 85, 247, 0.25);
    background: rgba(168, 85, 247, 0.07);
    color: #c084fc;
    font-size: 0.58rem;
    font-weight: 800;
    letter-spacing: 1px;
}


/* =========================================================
   HERO
   ========================================================= */

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
            rgba(124, 58, 237, 0.23),
            rgba(20, 17, 29, 0.94) 45%,
            rgba(8, 8, 13, 0.98)
        );

    border: 1px solid rgba(168, 85, 247, 0.25);

    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.35),
        inset 0 1px 0 rgba(255,255,255,0.03);
}

.hero::before {
    content: "";
    position: absolute;
    width: 400px;
    height: 400px;
    right: -130px;
    top: -210px;
    border-radius: 50%;
    background: rgba(168, 85, 247, 0.13);
    filter: blur(15px);
}

.hero::after {
    content: "";
    position: absolute;
    width: 1px;
    height: 130px;
    right: 29%;
    top: 38px;
    background:
        linear-gradient(
            180deg,
            transparent,
            rgba(168,85,247,0.45),
            transparent
        );
    transform: rotate(25deg);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-eyebrow {
    color: #c084fc;
    font-size: 0.68rem;
    font-weight: 850;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    margin-top: 9px;
    font-size: 3rem;
    line-height: 0.98;
    font-weight: 950;
    letter-spacing: -2px;
    color: white;
}

.hero-title span {
    color: #a855f7;
}

.hero-subtitle {
    margin-top: 12px;
    max-width: 650px;
    color: #a1a1aa;
    font-size: 0.93rem;
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
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    color: #71717a;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}


/* =========================================================
   SEÇÕES
   ========================================================= */

.section-kicker {
    margin-bottom: 8px;
    color: #71717a;
    font-size: 0.63rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 1.7px;
}


/* =========================================================
   CONTROL BAR
   ========================================================= */

.control-bar {
    padding: 14px 16px;
    margin-bottom: 20px;
    background: rgba(17, 17, 24, 0.72);
    border: 1px solid #242432;
    border-radius: 15px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.02);
}


/* =========================================================
   KPI
   ========================================================= */

.kpi-card {
    position: relative;
    overflow: hidden;
    padding: 20px;
    min-height: 125px;

    background:
        linear-gradient(
            145deg,
            rgba(24, 24, 34, 0.94),
            rgba(13, 13, 19, 0.98)
        );

    border: 1px solid #27272f;
    border-radius: 17px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.18);

    transition: 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(168,85,247,0.40);
    box-shadow:
        0 16px 40px rgba(124,58,237,0.12);
}

.kpi-card::after {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    right: -40px;
    bottom: -40px;
    border-radius: 50%;
    background: rgba(168,85,247,0.07);
}

.kpi-label {
    color: #71717a;
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.kpi-value {
    margin-top: 7px;
    color: #ffffff;
    font-size: 2.35rem;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -1.5px;
}

.kpi-description {
    margin-top: 8px;
    color: #52525b;
    font-size: 0.68rem;
}


/* =========================================================
   DIAGNÓSTICO
   ========================================================= */

.diagnosis-hero {
    position: relative;
    overflow: hidden;
    padding: 26px 28px;
    margin: 10px 0 18px;
    border-radius: 20px;

    background:
        linear-gradient(
            120deg,
            rgba(168,85,247,0.14),
            rgba(17,17,24,0.96) 52%
        );

    border: 1px solid rgba(168,85,247,0.28);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.25);
}

.diagnosis-hero::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;

    background:
        linear-gradient(
            180deg,
            #c084fc,
            #7c3aed
        );
}

.diagnosis-kicker {
    color: #c084fc;
    font-size: 0.64rem;
    font-weight: 900;
    letter-spacing: 1.7px;
    text-transform: uppercase;
}

.diagnosis-title-big {
    margin-top: 8px;
    color: white;
    font-size: 1.55rem;
    font-weight: 900;
    letter-spacing: -0.7px;
}

.diagnosis-description {
    margin-top: 7px;
    color: #71717a;
    font-size: 0.82rem;
    line-height: 1.5;
}

.diagnosis-number-card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(7,7,11,0.48);
    border: 1px solid rgba(255,255,255,0.06);
}

.diagnosis-number-label {
    color: #52525b;
    font-size: 0.61rem;
    font-weight: 800;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.diagnosis-number {
    margin-top: 5px;
    color: white;
    font-size: 2.15rem;
    font-weight: 900;
    letter-spacing: -1px;
}

.diagnosis-number.danger {
    color: #f87171;
}

.diagnosis-number.reference {
    color: #a78bfa;
}

.diagnosis-number.diff {
    color: #fb7185;
}


/* =========================================================
   ACTION / EVIDENCE
   ========================================================= */

.action-card {
    padding: 20px 22px;
    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(251,146,60,0.08),
            rgba(17,17,24,0.96)
        );

    border: 1px solid rgba(251,146,60,0.18);
}

.action-label {
    color: #fb923c;
    font-size: 0.62rem;
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
    font-size: 0.76rem;
    line-height: 1.5;
}

.evidence-card {
    padding: 20px 22px;
    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(34,197,94,0.05),
            rgba(17,17,24,0.96)
        );

    border: 1px solid rgba(34,197,94,0.13);
}

.evidence-label {
    color: #86efac;
    font-size: 0.62rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.evidence-text {
    margin-top: 8px;
    color: #a1a1aa;
    font-size: 0.8rem;
    line-height: 1.55;
}


/* =========================================================
   DIAGNOSTIC CARDS
   ========================================================= */

.diagnostic-card {
    padding: 22px;
    margin-bottom: 13px;

    background:
        linear-gradient(
            145deg,
            rgba(19,19,27,0.98),
            rgba(11,11,16,0.98)
        );

    border: 1px solid #27272f;
    border-radius: 17px;
    transition: 0.2s ease;
}

.diagnostic-card:hover {
    border-color: rgba(168,85,247,0.30);
    transform: translateX(2px);
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


/* =========================================================
   MAPA
   ========================================================= */

.map-hero {
    padding: 25px;
    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.13),
            rgba(17,17,24,0.96)
        );

    border: 1px solid rgba(168,85,247,0.20);
}

.map-name {
    color: white;
    font-size: 1.9rem;
    font-weight: 900;
    letter-spacing: -1px;
}

.map-subtitle {
    margin-top: 5px;
    color: #71717a;
    font-size: 0.76rem;
}


/* =========================================================
   INSIGHT
   ========================================================= */

.insight-strip {
    display: flex;
    align-items: center;
    gap: 14px;

    padding: 15px 17px;
    margin: 15px 0;

    background: rgba(168,85,247,0.055);
    border: 1px solid rgba(168,85,247,0.13);
    border-radius: 13px;
}

.insight-icon {
    font-size: 1.25rem;
}

.insight-text {
    color: #a1a1aa;
    font-size: 0.77rem;
    line-height: 1.45;
}


/* =========================================================
   STREAMLIT
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17,17,24,0.75);
    border-color: #27272f !important;
    border-radius: 16px;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
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


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    margin-top: 55px;
    padding: 25px 0 5px;
    border-top: 1px solid #20202a;
    text-align: center;
    color: #3f3f46;
    font-size: 0.68rem;
    letter-spacing: 0.5px;
}

.footer strong {
    color: #71717a;
}


/* =========================================================
   ESCONDER MENU
   ========================================================= */

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
# DADOS PROVISÓRIOS
# ============================================================

dados_times = {

    "LOUD": {
        "win_rate": 70,
        "ataque": 65,
        "defesa": 75,

        "problema": "Baixa recuperação após perder o pistol",
        "taxa_problema": 38,
        "referencia": 60,

        "investigacao": "Decisões econômicas nos rounds seguintes",

        "evidencia": (
            "Após perder o pistol, o time venceu apenas "
            "38% das rodadas seguintes analisadas."
        ),

        "economia": {
            "pistol": 60,
            "eco": 32,
            "force": 45,
            "full_buy": 68,
            "recuperacao": 38,
            "conversao": 72
        }
    },

    "MIBR": {
        "win_rate": 55,
        "ataque": 48,
        "defesa": 62,

        "problema": "Baixa conversão de vantagem numérica",
        "taxa_problema": 42,
        "referencia": 60,

        "investigacao": (
            "Execução das rodadas após conseguir vantagem"
        ),

        "evidencia": (
            "Em apenas 42% das rodadas em que o time "
            "conseguiu vantagem numérica, a rodada terminou "
            "em vitória."
        ),

        "economia": {
            "pistol": 60,
            "eco": 32,
            "force": 45,
            "full_buy": 68,
            "recuperacao": 35,
            "conversao": 72
        }
    },

    "FURIA": {
        "win_rate": 62,
        "ataque": 60,
        "defesa": 64,

        "problema": "Desempenho inferior no lado defensor",
        "taxa_problema": 47,
        "referencia": 60,

        "investigacao": (
            "Adaptação às entradas adversárias"
        ),

        "evidencia": (
            "O time apresentou 47% de Win Rate no lado "
            "defensor, indicando um desempenho inferior "
            "nesse contexto."
        ),

        "economia": {
            "pistol": 60,
            "eco": 48,
            "force": 52,
            "full_buy": 68,
            "recuperacao": 55,
            "conversao": 70
        }
    }
}


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

    time = st.selectbox(
        "Equipe analisada",
        list(dados_times.keys())
    )

    contexto = st.selectbox(
        "Contexto",
        ["Todos", "Ataque", "Defesa"]
    )

    mapa_filtro = st.selectbox(
        "Mapa",
        ["Todos", "Ascent", "Bind", "Haven", "Lotus"]
    )

    st.html("""
    <div class="sidebar-status">

        <div class="sidebar-status-title">
            ● Sistema operacional
        </div>

        <div class="sidebar-status-text">
            Análise pós-jogo ativa
        </div>

    </div>
    """)


# ============================================================
# DADOS SELECIONADOS
# ============================================================

dados = dados_times[time]

win_rate = dados["win_rate"]
ataque = dados["ataque"]
defesa = dados["defesa"]

problema = dados["problema"]
taxa_problema = dados["taxa_problema"]
referencia = dados["referencia"]

investigacao = dados["investigacao"]
evidencia = dados["evidencia"]

economia = dados["economia"]

diferenca = taxa_problema - referencia


if win_rate >= 60:
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

    </div>

</div>
""")


# ============================================================
# HERO
# ============================================================

st.html(f"""
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
        </div>

        <div class="hero-pills">

            <div class="hero-pill">
                POST-MATCH
            </div>

            <div class="hero-pill">
                DATA-DRIVEN
            </div>

            <div class="hero-pill">
                COACHING INTELLIGENCE
            </div>

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
    "MAPAS"
])


# ============================================================
# COMMAND CENTER
# ============================================================

with aba1:

    st.html("""
    <div class="section-kicker">
        Visão executiva
    </div>
    """)

    st.header(f"{time} · Command Center")

    st.html(f"""
    <div class="control-bar">

        <b style="color:#e4e4e7;">
            Contexto analisado:
        </b>

        <span style="color:#a855f7;">
            {contexto}
        </span>

        <span style="color:#52525b; margin-left:12px;">
            •
        </span>

        <span style="color:#71717a; margin-left:12px;">
            Status: {status}
        </span>

    </div>
    """)


    # ========================================================
    # KPI
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Win Rate
            </div>

            <div class="kpi-value">
                {win_rate}%
            </div>

            <div class="kpi-description">
                Desempenho geral
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
                {ataque}%
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
                {defesa}%
            </div>

            <div class="kpi-description">
                Performance defensiva
            </div>

        </div>
        """)

    with col4:
        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Gap crítico
            </div>

            <div class="kpi-value">
                {abs(diferenca)}pp
            </div>

            <div class="kpi-description">
                Distância para referência
            </div>

        </div>
        """)


    st.html("<br>")


    # ========================================================
    # STATUS
    # ========================================================

    if win_rate >= 60:
        st.success(
            f"🟢 {time} apresenta desempenho geral positivo, "
            f"com {win_rate}% de Win Rate."
        )

    elif win_rate >= 50:
        st.info(
            f"🟡 {time} apresenta desempenho intermediário, "
            f"com {win_rate}% de Win Rate."
        )

    else:
        st.warning(
            f"🔴 {time} apresenta desempenho abaixo de 50%, "
            f"indicando um ponto de atenção."
        )


    st.html("<br>")


    # ========================================================
    # DIAGNÓSTICO PRINCIPAL
    # ========================================================

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
            {problema}
        </div>

        <div class="diagnosis-description">
            O VALOCOACH identificou este contexto como
            prioridade para investigação.
        </div>

    </div>
    """)


    col1, col2, col3 = st.columns(3)

    with col1:

        classe = "danger" if taxa_problema < referencia else ""

        st.html(f"""
        <div class="diagnosis-number-card">

            <div class="diagnosis-number-label">
                Resultado observado
            </div>

            <div class="diagnosis-number {classe}">
                {taxa_problema}%
            </div>

        </div>
        """)

    with col2:

        st.html(f"""
        <div class="diagnosis-number-card">

            <div class="diagnosis-number-label">
                Referência
            </div>

            <div class="diagnosis-number reference">
                {referencia}%
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
                {diferenca} pp
            </div>

        </div>
        """)


    # ========================================================
    # EVIDÊNCIA / AÇÃO
    # ========================================================

    st.html("<br>")

    col1, col2 = st.columns(2)

    with col1:

        st.html(f"""
        <div class="evidence-card">

            <div class="evidence-label">
                🔎 Evidência encontrada
            </div>

            <div class="evidence-text">
                {evidencia}
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
                {investigacao}
            </div>

            <div class="action-text">
                O indicador não determina sozinho a causa.
                Ele aponta um contexto prioritário para
                investigação.
            </div>

        </div>
        """)


    st.html("<br>")


    # ========================================================
    # GRÁFICOS
    # ========================================================

    col1, col2 = st.columns([1.35, 1])

    with col1:

        st.html("""
        <div class="section-kicker">
            Performance
        </div>
        """)

        st.subheader("Desempenho por contexto")

        dados_grafico = {
            "Indicador": ["Win Rate", "Ataque", "Defesa"],
            "Valor": [win_rate, ataque, defesa]
        }

        grafico = px.bar(
            dados_grafico,
            x="Indicador",
            y="Valor",
            range_y=[0, 100],
            text="Valor"
        )

        grafico.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            marker_color="#8b5cf6"
        )

        grafico.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a1a1aa"),
            yaxis=dict(
                title="",
                gridcolor="#27272f"
            ),
            xaxis=dict(title=""),
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            grafico,
            width="stretch"
        )


    with col2:

        st.html("""
        <div class="section-kicker">
            Diagnóstico
        </div>
        """)

        st.subheader("Resultado × referência")

        dados_comparacao = {
            "Indicador": ["Observado", "Referência"],
            "Valor": [taxa_problema, referencia]
        }

        grafico_comparacao = px.bar(
            dados_comparacao,
            x="Indicador",
            y="Valor",
            range_y=[0, 100],
            text="Valor"
        )

        grafico_comparacao.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            marker_color=["#ef4444", "#8b5cf6"]
        )

        grafico_comparacao.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a1a1aa"),
            yaxis=dict(
                title="",
                gridcolor="#27272f"
            ),
            xaxis=dict(title=""),
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            grafico_comparacao,
            width="stretch"
        )


    # ========================================================
    # LEITURA EXECUTIVA
    # ========================================================

    st.html("""
    <div class="insight-strip">

        <div class="insight-icon">
            🧠
        </div>

        <div class="insight-text">
            <strong style="color:#e4e4e7;">
                Leitura executiva:
            </strong>
            o valor do VALOCOACH não está apenas em mostrar
            o percentual, mas em conectar o desvio observado
            ao contexto que merece investigação.
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
        "observados nas partidas."
    )


    if time == "LOUD":

        diagnosticos = [
            {
                "titulo": "Baixa recuperação após perder o pistol",
                "taxa": 38,
                "metrica": "Win Rate após perder pistol",
                "prioridade": "Alta",
                "investigacao": "Decisões econômicas nos rounds seguintes",
                "evidencia": (
                    "Após perder o pistol, o time venceu apenas "
                    "38% das rodadas seguintes analisadas."
                ),
                "referencia": 60
            },
            {
                "titulo": "Boa performance defensiva",
                "taxa": 75,
                "metrica": "Win Rate na defesa",
                "prioridade": "Baixa",
                "investigacao": "Manutenção dos padrões defensivos",
                "evidencia": (
                    "A equipe apresentou 75% de Win Rate "
                    "no lado defensor."
                ),
                "referencia": 60
            }
        ]

    elif time == "MIBR":

        diagnosticos = [
            {
                "titulo": "Baixa conversão de vantagem numérica",
                "taxa": 42,
                "metrica": "Win Rate após conseguir vantagem",
                "prioridade": "Alta",
                "investigacao": "Execução das rodadas após conseguir vantagem",
                "evidencia": (
                    "Em apenas 42% das rodadas em que o time "
                    "conseguiu vantagem numérica, a rodada terminou "
                    "em vitória."
                ),
                "referencia": 60
            },
            {
                "titulo": "Baixa recuperação após perder o pistol",
                "taxa": 35,
                "metrica": "Win Rate após perder pistol",
                "prioridade": "Média",
                "investigacao": "Decisões econômicas nos rounds seguintes",
                "evidencia": (
                    "Após perder o pistol, o time venceu apenas "
                    "35% das rodadas seguintes analisadas."
                ),
                "referencia": 60
            },
            {
                "titulo": "Queda de desempenho na defesa",
                "taxa": 47,
                "metrica": "Win Rate na defesa",
                "prioridade": "Média",
                "investigacao": "Adaptação às entradas adversárias",
                "evidencia": (
                    "O time apresentou 47% de Win Rate "
                    "no lado defensor."
                ),
                "referencia": 60
            }
        ]

    else:

        diagnosticos = [
            {
                "titulo": "Desempenho inferior no lado defensor",
                "taxa": 47,
                "metrica": "Win Rate na defesa",
                "prioridade": "Média",
                "investigacao": "Adaptação às entradas adversárias",
                "evidencia": (
                    "O time apresentou 47% de Win Rate "
                    "no lado defensor."
                ),
                "referencia": 60
            },
            {
                "titulo": "Boa conversão de vantagem",
                "taxa": 68,
                "metrica": "Win Rate após conseguir vantagem",
                "prioridade": "Baixa",
                "investigacao": "Manter eficiência após conseguir vantagem",
                "evidencia": (
                    "A equipe apresentou boa capacidade "
                    "de converter vantagens em vitórias."
                ),
                "referencia": 60
            }
        ]


    altas = sum(
        d["prioridade"] == "Alta"
        for d in diagnosticos
    )

    medias = sum(
        d["prioridade"] == "Média"
        for d in diagnosticos
    )

    baixas = sum(
        d["prioridade"] == "Baixa"
        for d in diagnosticos
    )


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
        ["Todos", "Alta", "Média", "Baixa"]
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

        diferenca_diag = (
            diagnostico["taxa"]
            - diagnostico["referencia"]
        )


        st.html(f"""
        <div class="diagnostic-card">

            <div class="diagnostic-card-title">
                {diagnostico["titulo"]}
            </div>

            <div
                style="
                    margin-top:7px;
                    font-size:0.67rem;
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
                f'{diagnostico["taxa"]}%'
            )

        with col2:
            st.metric(
                "Referência",
                f'{diagnostico["referencia"]}%'
            )

        with col3:
            st.metric(
                "Gap",
                f"{diferenca_diag} pp"
            )


        col1, col2 = st.columns(2)

        with col1:

            st.html(f"""
            <div class="action-card">

                <div class="action-label">
                    🧭 INVESTIGAR
                </div>

                <div class="action-title">
                    {diagnostico["investigacao"]}
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
                    {diagnostico["evidencia"]}
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
        "Entenda como o contexto econômico influencia "
        "a capacidade de recuperação e conversão."
    )


    col1, col2, col3, col4 = st.columns(4)

    metricas_economia = [
        ("Pistol", economia["pistol"], "Início de rodada"),
        ("Recuperação", economia["recuperacao"], "Após perder pistol"),
        ("Conversão", economia["conversao"], "Após vantagem"),
        ("Force Buy", economia["force"], "Investimento forçado")
    ]

    for coluna, (nome, valor, descricao) in zip(
        [col1, col2, col3, col4],
        metricas_economia
    ):

        with coluna:

            st.html(f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    {nome}
                </div>

                <div class="kpi-value">
                    {valor}%
                </div>

                <div class="kpi-description">
                    {descricao}
                </div>

            </div>
            """)


    st.html("<br>")


    col1, col2 = st.columns([1.4, 1])

    with col1:

        st.html("""
        <div class="section-kicker">
            Performance econômica
        </div>
        """)

        dados_economia = {
            "Situação": [
                "Pistol",
                "Eco",
                "Force",
                "Full Buy"
            ],
            "Win Rate": [
                economia["pistol"],
                economia["eco"],
                economia["force"],
                economia["full_buy"]
            ]
        }

        grafico_economia = px.bar(
            dados_economia,
            x="Situação",
            y="Win Rate",
            range_y=[0, 100],
            text="Win Rate"
        )

        grafico_economia.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            marker_color="#8b5cf6"
        )

        grafico_economia.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a1a1aa"),
            yaxis=dict(
                title="",
                gridcolor="#27272f"
            ),
            xaxis=dict(title=""),
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            grafico_economia,
            width="stretch"
        )


    with col2:

        st.html("""
        <div class="section-kicker">
            Diagnóstico econômico
        </div>
        """)

        st.html(f"""
        <div class="diagnosis-hero">

            <div class="diagnosis-kicker">
                ⚠ Contexto prioritário
            </div>

            <div class="diagnosis-title-big">
                Recuperação
            </div>

            <div class="diagnosis-description">
                {economia["recuperacao"]}% após perder o pistol.
                Referência: 60%.
            </div>

        </div>
        """)

        if economia["recuperacao"] < 50:
            st.warning(
                "Baixa capacidade de recuperação."
            )
        else:
            st.success(
                "Boa capacidade de recuperação."
            )


    st.html(f"""
    <div class="insight-strip">

        <div class="insight-icon">
            💡
        </div>

        <div class="insight-text">
            <strong style="color:#e4e4e7;">
                O que investigar:
            </strong>
            decisões econômicas nos rounds seguintes
            ao pistol, especialmente a relação entre
            investimento e capacidade de recuperação.
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
        "Explore padrões de desempenho e evidências espaciais."
    )


    mapas = [
        "Ascent",
        "Bind",
        "Haven",
        "Lotus"
    ]

    mapa_selecionado = st.selectbox(
        "Mapa analisado",
        mapas
    )


    dados_mapas = {

        "Ascent": {
            "win_rate": 62,
            "ataque": 58,
            "defesa": 66
        },

        "Bind": {
            "win_rate": 55,
            "ataque": 52,
            "defesa": 58
        },

        "Haven": {
            "win_rate": 61,
            "ataque": 64,
            "defesa": 58
        },

        "Lotus": {
            "win_rate": 52,
            "ataque": 49,
            "defesa": 55
        }
    }


    mapa = dados_mapas[mapa_selecionado]


    st.html(f"""
    <div class="map-hero">

        <div class="map-name">
            {mapa_selecionado}
        </div>

        <div class="map-subtitle">
            Performance por contexto tático
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
                {mapa["win_rate"]}%
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
                {mapa["ataque"]}%
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
                {mapa["defesa"]}%
            </div>

            <div class="kpi-description">
                Performance defensiva
            </div>

        </div>
        """)


    st.html("<br>")


    col1, col2 = st.columns([1.25, 1])

    with col1:

        dados_mapa = {
            "Contexto": [
                "Win Rate",
                "Ataque",
                "Defesa"
            ],
            "Valor": [
                mapa["win_rate"],
                mapa["ataque"],
                mapa["defesa"]
            ]
        }

        grafico_mapa = px.bar(
            dados_mapa,
            x="Contexto",
            y="Valor",
            range_y=[0, 100],
            text="Valor"
        )

        grafico_mapa.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            marker_color="#8b5cf6"
        )

        grafico_mapa.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a1a1aa"),
            yaxis=dict(
                title="",
                gridcolor="#27272f"
            ),
            xaxis=dict(title=""),
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            grafico_mapa,
            width="stretch"
        )


    with col2:

        st.html("""
        <div class="section-kicker">
            Leitura tática
        </div>
        """)

        if mapa["ataque"] > mapa["defesa"]:

            leitura = (
                "O time apresenta melhor desempenho "
                "no ataque do que na defesa."
            )

        elif mapa["defesa"] > mapa["ataque"]:

            leitura = (
                "O time apresenta melhor desempenho "
                "na defesa do que no ataque."
            )

        else:

            leitura = (
                "O desempenho está equilibrado "
                "entre ataque e defesa."
            )


        st.html(f"""
        <div class="evidence-card">

            <div class="evidence-label">
                🧠 INSIGHT
            </div>

            <div class="evidence-text">
                {leitura}
            </div>

        </div>
        """)


        st.html("<br>")


        st.html("""
        <div class="action-card">

            <div class="action-label">
                🔥 EVIDÊNCIA ESPACIAL
            </div>

            <div class="action-title">
                Heatmap tático
            </div>

            <div class="action-text">
                Kills, mortes, first bloods e plants
                serão posicionados no mapa quando
                os dados reais forem integrados.
            </div>

        </div>
        """)


    st.html("<br>")


    st.html("""
    <div class="insight-strip">

        <div class="insight-icon">
            🗺️
        </div>

        <div class="insight-text">
            <strong style="color:#e4e4e7;">
                Próxima camada:
            </strong>
            conectar eventos espaciais aos diagnósticos,
            permitindo que o mapa funcione como evidência
            e não apenas como visualização.
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