import json
import shutil
import subprocess
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path


def iniciar_servidor_relatorios(reports_dir, port=8502):
    handler = partial(
        SimpleHTTPRequestHandler,
        directory=str(reports_dir),
    )

    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        handler,
    )

    thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    return server


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


def executar_testes_ui(root_dir):
    npm = shutil.which("npm") or shutil.which("npm.cmd")

    if not npm:
        raise RuntimeError(
            "npm não encontrado no PATH. "
            "Verifique a instalação e reinicie o Streamlit."
        )

    return subprocess.run(
        [npm, "test"],
        cwd=root_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


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
