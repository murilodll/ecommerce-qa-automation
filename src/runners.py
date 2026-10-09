import json
import shutil
import subprocess
from pathlib import Path


def carregar_resultado_automacao(relatorio_json):
    if not relatorio_json.exists():
        return None

    with open(relatorio_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    stats = dados.get("stats", {})

    return {
        "passou": stats.get("expected", 0),
        "falhou": stats.get("unexpected", 0),
        "ignorado": stats.get("skipped", 0),
        "instavel": stats.get("flaky", 0),
        "duracao": stats.get("duration", 0),
    }


def executar_testes_api(known_bugs=False):
    maven = shutil.which("mvn") or shutil.which("mvn.cmd")

    if not maven:
        raise RuntimeError(
            "Maven não encontrado no PATH. "
            "Verifique a instalação e reinicie o Streamlit."
        )

    reports_dir = Path("reports/api/known-bugs" if known_bugs else "reports/api")
    reports_dir.mkdir(parents=True, exist_ok=True)

    for arquivo in reports_dir.glob("TEST-*.xml"):
        arquivo.unlink()

    comando = [
        maven,
        "-f",
        "tests/api/pom.xml",
    ]

    if known_bugs:
        comando.append("-Pknown-bugs")

    comando.append("test")

    return subprocess.run(
        comando,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
