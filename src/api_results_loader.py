from pathlib import Path
import xml.etree.ElementTree as ET


def carregar_resultados_api(
    reports_dir: str = "reports/api"
) -> dict:

    pasta = Path(reports_dir)

    resultado = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "duration": 0.0,
        "suites": [],
    }

    if not pasta.exists():
        return resultado

    for arquivo in pasta.glob("TEST-*.xml"):
        root = ET.parse(arquivo).getroot()

        total = int(root.attrib.get("tests", 0))
        failures = int(root.attrib.get("failures", 0))
        errors = int(root.attrib.get("errors", 0))
        skipped = int(root.attrib.get("skipped", 0))
        duration = float(root.attrib.get("time", 0))

        passed = total - failures - errors - skipped

        suite = {
            "name": root.attrib.get("name", arquivo.stem),
            "total": total,
            "passed": passed,
            "failed": failures,
            "errors": errors,
            "skipped": skipped,
            "duration": duration,
        }

        resultado["suites"].append(suite)

        resultado["total"] += total
        resultado["passed"] += passed
        resultado["failed"] += failures
        resultado["errors"] += errors
        resultado["skipped"] += skipped
        resultado["duration"] += duration

    return resultado