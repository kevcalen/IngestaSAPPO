from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

def load_template(country: str) -> Dict[str, Any]:
    c = country.upper().strip()
    path = TEMPLATES_DIR / f"checkout_{c}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing template for {c}: {path}. Create it under src/templates/."
        )
    return json.loads(path.read_text(encoding="utf-8"))

def build_key(transport_number: int, turn: int) -> str:
    # Confirmed format: "{transportNumber}_{turn}" e.g. "1000001_1"
    return f"{transport_number}_{turn}"

def build_payload(template: Dict[str, Any], *, key: str, date: str) -> Dict[str, Any]:
    payload = json.loads(json.dumps(template))  # deep copy
    payload["key"] = key
    payload["date"] = date
    return payload
