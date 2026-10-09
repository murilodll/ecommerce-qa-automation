import pandas as pd
import streamlit as st

from gherkin_loader import carregar_features

STATUS_MAP = {
    0: ("0 - Não executado", "⚪"),
    1: ("1 - Passou", "🟢"),
    2: ("2 - Falhou", "🔴"),
    3: ("3 - Bloqueado", "🟡"),
}

COLOR_MAP = {
    "0 - Não executado": "#95A5A6",
    "1 - Passou": "#2ECC71",
    "2 - Falhou": "#E74C3C",
    "3 - Bloqueado": "#F1C40F",
}


def inicializar_testes(diretorio_features, arquivo_execucoes):
    if "df_testes" not in st.session_state:
        df_cenarios = carregar_features(diretorio_features)
        df_execucoes = pd.read_csv(arquivo_execucoes)

        df = df_cenarios.merge(df_execucoes, on="id", how="left")

        df["estado"] = df["estado"].fillna(0).astype(int)
        df["observacao"] = df["observacao"].fillna("").astype(str)

        st.session_state.df_testes = df


def limpar_execucao(arquivo_execucoes):
    st.session_state.df_testes["estado"] = 0
    st.session_state.df_testes["observacao"] = ""

    df_execucoes = st.session_state.df_testes[["id", "estado", "observacao"]]
    df_execucoes.to_csv(arquivo_execucoes, index=False)

    st.session_state.execucao += 1
    st.rerun()


def renderizar_testes_manuais(arquivo_execucoes, diretorio_features):
    inicializar_testes(diretorio_features, arquivo_execucoes)

    opcoes_radio = [valor[0] for valor in STATUS_MAP.values()]
    texto_para_int = {valor[0]: chave for chave, valor in STATUS_MAP.items()}

    col1, col2 = st.columns(2)

    with col1:
        funcionalidades = ["Todas"] + list(
            st.session_state.df_testes["funcionalidade"].unique()
        )
        filtro_func = st.selectbox("Filtrar por Suíte:", funcionalidades)

    with col2:
        status_opcoes = ["Todos"] + opcoes_radio
        filtro_status = st.selectbox(
            "Filtrar por Status:",
            status_opcoes,
        )

    df_exibicao = st.session_state.df_testes.copy()

    if filtro_func != "Todas":
        df_exibicao = df_exibicao[df_exibicao["funcionalidade"] == filtro_func]

    if filtro_status != "Todos":
        status_num = texto_para_int[filtro_status]
        df_exibicao = df_exibicao[df_exibicao["estado"] == status_num]

    st.divider()

    for _, row in df_exibicao.iterrows():
        test_id = row["id"]
        suite = str(row["funcionalidade"]).strip()
        nome = str(row["nome"]).strip()
        descricao = str(row["descricao"]).strip()
        estado_atual_num = int(row["estado"])

        status_texto, icone = STATUS_MAP.get(
            estado_atual_num,
            STATUS_MAP[0],
        )

        titulo_expander = (
            f"{icone} [{suite}] - {test_id}: " f"{nome} — ({status_texto})"
        )

        with st.expander(titulo_expander):
            st.markdown("**Cenário:**")
            st.code(descricao, language="gherkin")

            novo_status_texto = st.radio(
                label="Alterar Status:",
                options=opcoes_radio,
                index=opcoes_radio.index(status_texto),
                key=f"radio_teste_{test_id}_{st.session_state.execucao}",
            )

            novo_status_num = texto_para_int[novo_status_texto]

            observacao_atual = str(row.get("observacao", ""))

            if observacao_atual == "nan":
                observacao_atual = ""

            nova_observacao = st.text_area(
                "Observação:",
                value=observacao_atual,
                placeholder="Informe detalhes relevantes sobre a execução...",
                key=f"observacao_teste_{test_id}_{st.session_state.execucao}",
            )

            if st.button("💾 Salvar", key=f"salvar_teste_{test_id}"):
                idx_original = st.session_state.df_testes[
                    st.session_state.df_testes["id"] == test_id
                ].index[0]

                st.session_state.df_testes.at[idx_original, "estado"] = novo_status_num

                st.session_state.df_testes.at[idx_original, "observacao"] = (
                    nova_observacao
                )

                df_execucoes = st.session_state.df_testes[
                    ["id", "estado", "observacao"]
                ]

                df_execucoes.to_csv(
                    arquivo_execucoes,
                    index=False,
                )

                st.rerun()

    st.divider()
