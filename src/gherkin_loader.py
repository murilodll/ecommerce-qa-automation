from pathlib import Path

import pandas as pd
from gherkin.parser import Parser

def montar_descricao(
    steps: list,
    dados_exemplo: dict | None = None
) -> str:
    passos = []

    for step in steps:
        keyword = step["keyword"].strip()
        texto = step["text"]

        if dados_exemplo:
            for variavel, valor in dados_exemplo.items():
                texto = texto.replace(
                    f"<{variavel}>",
                    valor
                )

        passos.append(f"{keyword} {texto}")

    return "\n".join(passos)

def carregar_features(diretorio: Path) -> pd.DataFrame:
    cenarios = []

    for arquivo in diretorio.glob("*.feature"):
        conteudo = arquivo.read_text(encoding="utf-8")

        documento = Parser().parse(conteudo)
        feature = documento["feature"]

        funcionalidade = feature["name"]

        for child in feature["children"]:
            scenario = child.get("scenario")

            if not scenario:
                continue

            tags = [
                tag["name"]
                for tag in scenario.get("tags", [])
            ]

            id_manual = next(
                (
                    tag.removeprefix("@")
                    for tag in tags
                    if tag.startswith("@MANUAL-")
                ),
                None
            )

            if not id_manual:
                continue

            exemplos = scenario.get("examples", [])

            # Cenário normal
            if not exemplos:
                descricao = montar_descricao(
                    scenario["steps"]
                )

                cenarios.append({
                    "id": id_manual,
                    "funcionalidade": funcionalidade,
                    "nome": scenario["name"],
                    "descricao": descricao,
                })

                continue

            # Esquema do Cenário
            numero_exemplo = 1

            for bloco_exemplos in exemplos:
                cabecalho = bloco_exemplos.get("tableHeader")

                if not cabecalho:
                    continue

                colunas = [
                    cell["value"]
                    for cell in cabecalho["cells"]
                ]

                for linha in bloco_exemplos.get("tableBody", []):
                    valores = [
                        cell["value"]
                        for cell in linha["cells"]
                    ]

                    dados_exemplo = dict(zip(colunas, valores))

                    descricao = montar_descricao(
                        scenario["steps"],
                        dados_exemplo
                    )

                    cenarios.append({
                        "id": f"{id_manual}-{numero_exemplo}",
                        "funcionalidade": funcionalidade,
                        "nome": scenario["name"],
                        "descricao": descricao,
                    })

                    numero_exemplo += 1

    return pd.DataFrame(cenarios)