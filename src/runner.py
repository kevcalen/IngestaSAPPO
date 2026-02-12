from __future__ import annotations
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date as dt_date
from pathlib import Path
from typing import Any, Dict, List

from .api_client import ApiClient
from .config import get_country_config
from .payload_builder import load_template, build_key, build_payload
from .reporting import write_csv, write_summary


def run_massive_checkouts(
    *,
    country: str,
    volume: int,
    turn: int = 1,
    start_transport: int = 1000001,
    date_str: str | None = None,
    workers: int = 15,
    out_dir: str = "artifacts",
) -> Path:
    if volume <= 0:
        raise ValueError("volume must be > 0")

    cfg = get_country_config(country)
    template = load_template(cfg.country)
    client = ApiClient(cfg.base_url, cfg.api_key)

    date_str = date_str or dt_date.today().isoformat()

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    results_file = out_path / f"results_{cfg.country}.jsonl"

    def one(i: int) -> Dict[str, Any]:
        transport = start_transport + i
        key = build_key(transport, turn)
        payload = build_payload(template, key=key, date=date_str)

        status, body = client.post_checkout(payload)

        ok_success = None
        if isinstance(body, dict):
            # Adjust if your API uses different success semantics
            if "success" in body:
                ok_success = bool(body.get("success"))
            elif "message" in body:
                ok_success = str(body.get("message")).lower() == "success"

        return {
            "country": cfg.country,
            "base_url": cfg.base_url,
            "transport": transport,
            "turn": turn,
            "key": key,
            "date": date_str,
            "status_code": status,
            "success_flag": ok_success,
            "response": body,
        }

    results: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(one, i) for i in range(volume)]
        for f in as_completed(futures):
            results.append(f.result())

    with results_file.open("w", encoding="utf-8") as w:
        for row in results:
            w.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Reportes adicionales (CSV + resumen)
    csv_file = out_path / f"results_{cfg.country}.csv"
    summary_json = out_path / f"summary_{cfg.country}.json"
    summary_md = out_path / f"summary_{cfg.country}.md"

    write_csv(results, csv_file)
    write_summary(results, summary_json, summary_md)

    bad = [r for r in results if r["status_code"] != 200]
    if bad:
        raise RuntimeError(
            f"Failed {len(bad)}/{len(results)} requests (status != 200). "
            f"See {results_file} for details."
        )

    return results_file


