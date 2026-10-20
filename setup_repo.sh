#!/usr/bin/env bash
# Cria a estrutura de pastas do VALOCOACH e o primeiro commit.
set -e

mkdir -p app src/valocoach/diagnostics data/raw data/processed docs reports tests
touch data/raw/.gitkeep data/processed/.gitkeep reports/.gitkeep
touch src/valocoach/__init__.py src/valocoach/diagnostics/__init__.py
touch src/valocoach/{loader,metrics,maps,report}.py
touch app/main.py tests/__init__.py

cat > requirements.txt << 'REQ'
pandas
numpy
streamlit
plotly
matplotlib
reportlab
pytest
REQ

cat > THIRD_PARTY.md << 'TP'
# Materiais de terceiros

Liste aqui bibliotecas, fontes e imagens usadas, com a licença de cada uma.

| Item | Licença | Link |
|---|---|---|
TP

cat > docs/inventario_viabilidade.md << 'INV'
# Inventário de viabilidade

Para cada diagnóstico candidato, confirmar se os JSONs sustentam.

| # | Diagnóstico | Campos necessários | Viável? | Observações |
|---|---|---|---|---|
| 1 | Recuperação após perder o pistol | | | |
| 2 | Ataque vs. defesa por mapa | | | |
| 3 | Conversão após ganhar o pistol | | | |
| 4 | Force buy sem resultado | | | |
| 5 | Dependência de um jogador | | | |
INV

git init -b main
git add .
git commit -m "chore: estrutura inicial do VALOCOACH"
echo "Pronto! Agora conecte ao GitHub (veja o passo a passo)."
