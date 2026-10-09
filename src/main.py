import os
from pathlib import Path

import streamlit as st

from api_results_loader import carregar_resultados_api
from runners import executar_testes_api, executar_testes_ui, iniciar_servidor_relatorios
from dashboard import renderizar_dashboard
from manual_tests import (
    COLOR_MAP,
    STATUS_MAP,
    inicializar_testes,
    limpar_execucao,
    renderizar_testes_manuais,
)

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
REPORTS_BASE_URL = os.getenv("REPORTS_BASE_URL", "http://localhost:8502")


@st.cache_resource
def obter_servidor_relatorios():
    return iniciar_servidor_relatorios(ROOT_DIR / "reports")


obter_servidor_relatorios()

ARQUIVO_EXECUCOES = ROOT_DIR / "data" / "execucoes.csv"
RELATORIO_PLAYWRIGHT = ROOT_DIR / "reports" / "playwright-report" / "index.html"
RELATORIO_CUCUMBER = ROOT_DIR / "reports" / "cucumber-report" / "index.html"
RELATORIO_JSON = ROOT_DIR / "reports" / "playwright-results.json"
DIRETORIO_FEATURES = ROOT_DIR / "tests" / "ui" / "manual"

inicializar_testes(
    DIRETORIO_FEATURES,
    ARQUIVO_EXECUCOES,
)

col_titulo, col_limpar = st.columns([3, 1], vertical_alignment="center")

with col_titulo:
    st.title("🧪 Execução de Testes")

with col_limpar:
    if "execucao" not in st.session_state:
        st.session_state.execucao = 0

tab_execucao, tab_automacao, tab_api, tab_dashboard = st.tabs(
    ["Manuais", "Automáticos [Playwright]", "API [Rest Assured]", "📊 Dashboard"]
)
with tab_execucao:
    st.title("Suítes de Testes Manuais")
    if st.button("🔄 Limpar Execução Manual"):
        limpar_execucao(ARQUIVO_EXECUCOES)
    renderizar_testes_manuais(ARQUIVO_EXECUCOES, DIRETORIO_FEATURES)

with tab_automacao:

    if "automacao_executada" not in st.session_state:
        st.session_state.automacao_executada = False

    colb1, colb2, colb3 = st.columns(3)

    with colb1:
        st.subheader("Testes Automáticos")

    with colb2:
        st.link_button(
            "📄 Abrir relatório Playwright",
            f"{REPORTS_BASE_URL}/playwright-report/index.html",
            disabled=not RELATORIO_PLAYWRIGHT.exists(),
        )

    with colb3:
        st.link_button(
            "🥒 Abrir relatório Cucumber",
            f"{REPORTS_BASE_URL}/cucumber-report/index.html",
            disabled=not RELATORIO_CUCUMBER.exists(),
        )

    if st.button("▶ Executar testes", type="primary"):
        with st.spinner("Executando Playwright..."):
            resultado = executar_testes_ui(ROOT_DIR)

        st.session_state.automacao_executada = True

        if resultado.returncode == 0:
            st.success("Testes finalizados com sucesso.")
        else:
            st.error("A execução apresentou falhas.")

        st.code(resultado.stdout + resultado.stderr, language="text")

with tab_api:

    st.subheader("API - REST Assured")
    st.write(
        "Executa os testes de regressão da API, "
        "excluindo os cenários marcados como known-bug."
    )
    executar_bugs = st.checkbox("Executar bugs conhecidos", value=False)
    if st.button("Executar testes API", type="primary"):
        with st.spinner("Executando testes REST Assured..."):
            resultado = executar_testes_api(known_bugs=executar_bugs)

        if executar_bugs:
            if resultado.returncode != 0:
                st.warning("Os bugs conhecidos foram reproduzidos.")
            else:
                st.success(
                    "Os bugs conhecidos não foram reproduzidos. "
                    "Eles podem ter sido corrigidos."
                )
        else:
            if resultado.returncode == 0:
                st.success("Testes de API executados com sucesso.")
            else:
                st.error("A execução dos testes de API apresentou falhas.")

        with st.expander("Saída da execução"):
            st.code(resultado.stdout + resultado.stderr, language="text")

    reports_dir = "reports/api/known-bugs" if executar_bugs else "reports/api"

    resultados_api = carregar_resultados_api(reports_dir)
    if resultados_api["total"] > 0:
        st.write(
            f"Última execução: "
            f'**{resultados_api["passed"]}/{resultados_api["total"]} '
            f"testes aprovados**"
        )

with tab_dashboard:
    renderizar_dashboard(
        st.session_state.df_testes,
        status_map=STATUS_MAP,
        color_map=COLOR_MAP,
        relatorio_json=RELATORIO_JSON,
    )
