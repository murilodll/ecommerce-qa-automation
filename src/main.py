import pandas as pd
import plotly.express as px
import streamlit as st
import subprocess, json, webbrowser
from gherkin_loader import carregar_features
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
ARQUIVO_EXECUCOES = BASE_DIR.parent / "data" / "execucoes.csv"
RELATORIO_PLAYWRIGHT = (ROOT_DIR / "reports" / "playwright-report" / "index.html")
RELATORIO_CUCUMBER = (ROOT_DIR / "reports" / "cucumber-report" / "index.html")
RELATORIO_JSON = (ROOT_DIR / "reports" / "playwright-results.json")
DIRETORIO_FEATURES = (ROOT_DIR / "tests" / "ui" / "manual")

col_titulo, col_limpar = st.columns([3, 1], vertical_alignment="center")

with col_titulo:
    st.title("🧪 Execução de Testes")

with col_limpar:
    if "execucao" not in st.session_state:
      st.session_state.execucao = 0
    
    if st.button("🔄 Limpar Execução"):
        st.session_state.df_testes["estado"] = 0
        st.session_state.df_testes["observacao"] = ""

        df_execucoes = st.session_state.df_testes[
            ["id", "estado", "observacao"]
        ]

        df_execucoes.to_csv(
            ARQUIVO_EXECUCOES,
            index=False
        )

        st.session_state.execucao += 1

        st.rerun()
    
tab_execucao, tab_automacao, tab_dashboard = st.tabs([
    "Manuais",
    "Automáticos [Playwright]",
    "📊 Dashboard"
])

def carregar_resultado_automacao():
    if not RELATORIO_JSON.exists():
        return None

    with open(RELATORIO_JSON, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    stats = dados.get("stats", {})

    return {
        "passou": stats.get("expected", 0),
        "falhou": stats.get("unexpected", 0),
        "ignorado": stats.get("skipped", 0),
        "instavel": stats.get("flaky", 0),
        "duracao": stats.get("duration", 0),
    }

with tab_execucao:

  if "df_testes" not in st.session_state:
    df_cenarios = carregar_features(DIRETORIO_FEATURES)
    df_execucoes = pd.read_csv(ARQUIVO_EXECUCOES)

    df = df_cenarios.merge(
        df_execucoes,
        on="id",
        how="left"
    )

    df["estado"] = df["estado"].fillna(0).astype(int)
    df["observacao"] = df["observacao"].fillna("").astype(str)

    st.session_state.df_testes = df


  STATUS_MAP = {
      0: ("0 - Não executado", "⚪"),
      1: ("1 - Passou", "🟢"),
      2: ("2 - Falhou", "🔴"),
      3: ("3 - Bloqueado", "🟡")
  }

  COLOR_MAP = {
    "0 - Não executado": "#95A5A6",  # Cinza
    "1 - Sucesso": "#2ECC71",        # Verde
    "2 - Falha": "#E74C3C",          # Vermelho
    "3 - Bloqueado": "#F1C40F"       # Amarelo
  }

  OPCOES_RADIO = [val[0] for val in STATUS_MAP.values()]
  TEXTO_PARA_INT = {val[0]: key for key, val in STATUS_MAP.items()}

  st.title("Suítes de Testes Manuais")

  col1, col2 = st.columns(2)

  with col1:
      funcionalidades = ["Todas"] + list(st.session_state.df_testes["funcionalidade"].unique())
      filtro_func = st.selectbox("Filtrar por Suíte:", funcionalidades)

  with col2:
      status_opcoes = ["Todos"] + OPCOES_RADIO
      filtro_status = st.selectbox("Filtrar por Status:", status_opcoes)

  df_exibicao = st.session_state.df_testes.copy()

  if filtro_func != "Todas":
      df_exibicao = df_exibicao[df_exibicao["funcionalidade"] == filtro_func]

  if filtro_status != "Todos":
      status_num = TEXTO_PARA_INT[filtro_status]
      df_exibicao = df_exibicao[df_exibicao["estado"] == status_num]

  st.divider()

  for index, row in df_exibicao.iterrows():
      test_id = row['id']
      suite = str(row['funcionalidade']).strip()
      nome = str(row['nome']).strip()
      descricao = str(row['descricao']).strip()
      estado_atual_num = int(row['estado'])

      status_texto, icone = STATUS_MAP.get(estado_atual_num, STATUS_MAP[0])
      titulo_expander = f"{icone} [{suite}] - {test_id}: {nome} — ({status_texto})"

      with st.expander(titulo_expander):
          st.markdown("**Cenário:**")
          st.code(descricao, language="gherkin")
          
          novo_status_texto = st.radio(
              label="Alterar Status:",
              options=OPCOES_RADIO,
              index=OPCOES_RADIO.index(status_texto),
              key=f"radio_teste_{test_id}_{st.session_state.execucao}"
          )

          novo_status_num = TEXTO_PARA_INT[novo_status_texto]

          observacao_atual = str(row.get("observacao", ""))

          if observacao_atual == "nan":
              observacao_atual = ""

          nova_observacao = st.text_area(
              "Observação:",
              value=observacao_atual,
              placeholder="Informe detalhes relevantes sobre a execução...",
              key=f"observacao_teste_{test_id}_{st.session_state.execucao}"
          )

          if st.button("💾 Salvar", key=f"salvar_teste_{test_id}"):

              idx_original = st.session_state.df_testes[
                  st.session_state.df_testes["id"] == test_id
              ].index[0]

              st.session_state.df_testes.at[
                  idx_original, "estado"
              ] = novo_status_num

              st.session_state.df_testes.at[
                  idx_original, "observacao"
              ] = nova_observacao

              df_execucoes = st.session_state.df_testes[
                  ["id", "estado", "observacao"]
              ]

              df_execucoes.to_csv(
                  ARQUIVO_EXECUCOES,
                  index=False
              )

              st.rerun()

  st.divider()

with tab_automacao:
    if "automacao_executada" not in st.session_state:
      st.session_state.automacao_executada = False

    colb1, colb2, colb3 = st.columns(3)
    
    with colb1:
      st.subheader("Testes Automáticos")
    
    with colb2:
      if st.button("📄 Abrir relatório Playwright", disabled=(
        not st.session_state.automacao_executada
        or not RELATORIO_PLAYWRIGHT.exists()
    )):
        webbrowser.open(
          (ROOT_DIR / "reports/playwright-report/index.html").as_uri()
      )

    with colb3:
      if st.button("🥒 Abrir relatório Cucumber", disabled=(
        not st.session_state.automacao_executada
        or not RELATORIO_CUCUMBER.exists()
    )):
        webbrowser.open(
          (ROOT_DIR / "reports/cucumber-report/index.html").as_uri()
      )

    if st.button("▶ Executar testes"):
        with st.spinner("Executando Playwright..."):
            resultado = subprocess.run(
                ["npm", "test"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                shell=True
            )

        st.session_state.automacao_executada = True

        if resultado.returncode == 0:
            st.success("Testes finalizados com sucesso.")
        else:
            st.error("A execução apresentou falhas.")

        st.code(
            resultado.stdout + resultado.stderr,
            language="text"
        )


with tab_dashboard:
  st.subheader("📊 Progresso das Execuções Manuais")

  df_counts = (
      df_exibicao['estado']
      .map(lambda x: STATUS_MAP.get(int(x), STATUS_MAP[0])[0])
      .value_counts()
      .reset_index()
  )
  df_counts.columns = ['Status', 'Quantidade']

  fig = px.pie(
      df_counts,
      names='Status',
      values='Quantidade',
      color='Status',
      color_discrete_map=COLOR_MAP,
      hole=0.4  # Estilo Donut
  )

  fig.update_traces(textposition='inside', textinfo='percent+value')
  fig.update_layout(margin=dict(t=20, b=20, l=10, r=10), showlegend=True)

  st.plotly_chart(fig, use_container_width=True)

  st.divider()
  st.subheader("🤖 Execução Automatizada")

  resultado_automacao = carregar_resultado_automacao()

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

      cold1.metric(
          "Total",
          total
      )

      cold2.metric(
          "Passaram",
          resultado_automacao["passou"]
      )

      cold3.metric(
          "Falharam",
          resultado_automacao["falhou"]
      )

      cold4.metric(
          "Ignorados",
          resultado_automacao["ignorado"]
      )

      duracao_segundos = resultado_automacao["duracao"] / 1000

      taxa_sucesso = (
          resultado_automacao["passou"] / total * 100
          if total > 0
          else 0
      )

      st.write(
          f"⏱️ Duração: **{duracao_segundos:.2f}s**"
      )

      st.write(
          f"Taxa de sucesso: **{taxa_sucesso:.1f}%**"
      )

      st.progress(taxa_sucesso / 100)

  st.divider()
