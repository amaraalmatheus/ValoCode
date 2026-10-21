# Materiais de terceiros e licenças

Este arquivo registra tudo que o VALOCOACH usa e que não foi escrito pela equipe, com a licença de cada item. Atende ao item "licenças de bibliotecas, imagens e fontes conferidas" do checklist de entrega do hackathon.

**Última conferência:** 20/10/2026, nos metadados dos pacotes e nas páginas oficiais dos projetos. Rever sempre que uma biblioteca for adicionada ou trocada.

## Como as bibliotecas entram no projeto

Nenhum código de terceiros está copiado neste repositório. As bibliotecas são instaladas pelo `pip` (`pyproject.toml` e `requirements.txt`), cada uma com a sua própria licença, que acompanha o pacote instalado. Todas as licenças abaixo são permissivas e permitem uso em um projeto como este.

## Bibliotecas em uso (pipeline de dados)

| Biblioteca | Para que serve | Licença |
|---|---|---|
| [pandas](https://pandas.pydata.org) | Tabelas, limpeza e cálculo das métricas | BSD-3-Clause |
| [NumPy](https://numpy.org) | Cálculo numérico (instalada junto com o pandas) | BSD-3-Clause (o pacote inclui componentes sob 0BSD, MIT, Zlib e CC0-1.0) |
| [python-dateutil](https://github.com/dateutil/dateutil) | Datas (dependência do pandas) | Dupla: Apache-2.0 ou BSD-3-Clause |
| [six](https://github.com/benjaminp/six) | Compatibilidade (dependência do pandas) | MIT |
| [tzdata](https://github.com/python/tzdata) | Fusos horários (dependência do pandas) | Apache-2.0 |

## Bibliotecas planejadas (interface, gráficos e relatório)

Listadas no `requirements.txt`. Se alguma deixar de ser usada, remover daqui e de lá.

| Biblioteca | Para que serve | Licença |
|---|---|---|
| [Streamlit](https://streamlit.io) | Interface do coach | Apache-2.0 |
| [Plotly](https://plotly.com/python/) | Gráficos e mapas de calor interativos | MIT |
| [Matplotlib](https://matplotlib.org) | Gráficos estáticos (relatório) | Licença do Matplotlib (baseada na PSF, permissiva) |
| [ReportLab](https://www.reportlab.com/opensource/) | Relatório de 1 página em PDF | BSD (edição de código aberto) |
| [tabulate](https://github.com/astanin/python-tabulate) | Tabelas em Markdown no relatório de qualidade (opcional) | MIT |

## Ferramentas de desenvolvimento (não fazem parte da entrega)

| Ferramenta | Uso | Licença |
|---|---|---|
| [pytest](https://pytest.org) | Testes automatizados | MIT |
| [setuptools](https://github.com/pypa/setuptools) | Empacotamento (`pip install -e .`) | MIT |

O Python em si é distribuído sob a licença da PSF e não é redistribuído por este repositório.

## Dados

- Os JSONs de partidas são fornecidos pela organização do hackathon e são a **única** fonte de dados do projeto.
- Eles **não** são redistribuídos: `data/raw/` e `data/processed/` ficam fora do Git (`.gitignore`).
- Não há scraping, APIs externas nem coleta em outros sites.

## Imagens, fontes, ícones e ilustrações

Até o momento, **nenhum** item de terceiros deste tipo é usado.

Observações para a frente de Interface e Mapas:
- Imagens do jogo (mapas, agentes, armas, ícones) pertencem à Riot Games. O edital exige respeitar direitos autorais, então não use esses arquivos sem permissão expressa da organização. Os mapas de calor funcionam como gráfico de pontos, sem imagem de fundo.
- Fontes: prefira as do sistema ou uma fonte com licença aberta (por exemplo, SIL OFL) e registre abaixo.

Se algum item for adicionado, registre aqui antes do commit:

| Item | Origem (link) | Licença | Onde é usado |
|---|---|---|---|
| _(nenhum até agora)_ | | | |

## Aviso sobre a Riot Games

O VALOCOACH não é endossado pela Riot Games e não reflete as opiniões da Riot Games ou de qualquer pessoa oficialmente envolvida na produção ou gestão de propriedades da Riot Games. VALORANT é marca registrada da Riot Games, Inc.
