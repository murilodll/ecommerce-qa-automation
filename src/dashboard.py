import plotly.express as px
import streamlit as st

from api_results_loader import carregar_resultados_api
from runners import carregar_resultado_automacao


def renderizar_dashboard(df_exibicao, status_map, color_map, relatorio_json):
    st.subheader("📊 Progresso das Execuções Manuais")

    resultados_api = carregar_resultados_api("reports/api")
    resultados_known_bugs = carregar_resultados_api("reports/api/known-bugs")

    df_counts = (
        df_exibicao["estado"]
        .map(lambda x: status_map.get(int(x), status_map[0])[0])
        .value_counts()
        .reset_index()
    )
    df_counts.columns = ["Status", "Quantidade"]

    fig = px.pie(
        df_counts,
        names="Status",
        values="Quantidade",
        color="Status",
        color_discrete_map=color_map,
        hole=0.4,
    )

    fig.update_traces(textposition="inside", textinfo="percent+value")
    fig.update_layout(margin=dict(t=20, b=20, l=10, r=10), showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("🤖 Execução Automatizada")

    resultado_automacao = carregar_resultado_automacao(relatorio_json)

    if resultado_automacao is None:
        st.info("Nenhuma execução automatizada encontrada.")
    else:
        total = (
            resultado_automacao["passou"]
            + resultado_automacao["falhou"]
            + resultado_automacao["ignorado"]
            + resultado_automacao["instavel"]
        )

        cold1, cold2, cold3, cold4 = st.columns(4)
        cold1.metric("Total", total)
        cold2.metric("Passaram", resultado_automacao["passou"])
        cold3.metric("Falharam", resultado_automacao["falhou"])
        cold4.metric("Ignorados", resultado_automacao["ignorado"])

        duracao_segundos = resultado_automacao["duracao"] / 1000
        taxa_sucesso = resultado_automacao["passou"] / total * 100 if total > 0 else 0

        st.write(f"⏱️ Duração: **{duracao_segundos:.2f}s**")
        st.write(f"Taxa de sucesso: **{taxa_sucesso:.1f}%**")
        st.progress(taxa_sucesso / 100)

    st.divider()
    st.subheader("API - REST Assured")

    if resultados_api["total"] == 0:
        st.info("Nenhum resultado de API encontrado.")
    else:
        colapi1, colapi2, colapi3, colapi4 = st.columns(4)
        colapi1.metric("Executados", resultados_api["total"])
        colapi2.metric("Aprovados", resultados_api["passed"])
        colapi3.metric("Falhas", resultados_api["failed"])
        colapi4.metric("Tempo", f'{resultados_api["duration"]:.2f}s')

    st.markdown("#### Suítes")

    for suite in resultados_api["suites"]:
        st.write(
            f'**{suite["name"]}** — '
            f'{suite["passed"]}/{suite["total"]} aprovados '
            f'({suite["duration"]:.2f}s)'
        )

    st.divider()
    st.markdown("#### Bugs conhecidos")

    if resultados_known_bugs["total"] > 0:
        reproduzidos = resultados_known_bugs["failed"]
        total = resultados_known_bugs["total"]

        col1, col2 = st.columns(2)
        col1.metric("Cenários de reprodução", total)
        col2.metric("Cenários com falha esperada", reproduzidos)

        if reproduzidos == total:
            st.warning(
                f"{reproduzidos}/{total} cenários reproduziram os bugs conhecidos."
            )
        elif reproduzidos == 0:
            st.success(
                "Nenhum bug conhecido foi reproduzido. "
                "Os defeitos podem ter sido corrigidos."
            )
        else:
            st.warning(
                f"{reproduzidos}/{total} cenários ainda "
                "reproduzem os bugs conhecidos."
            )
    else:
        st.info("Os testes de bugs conhecidos ainda não foram executados.")

    st.divider()
