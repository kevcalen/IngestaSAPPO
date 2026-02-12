from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    fields = [
        "country",
        "base_url",
        "transport",
        "turn",
        "key",
        "date",
        "status_code",
        "success_flag",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})


def write_summary(rows: List[Dict[str, Any]], path_json: Path, path_md: Path) -> None:
    total = len(rows)
    ok = sum(1 for r in rows if r.get("status_code") == 200)
    bad = total - ok

    statuses: Dict[str, int] = {}
    for r in rows:
        s = str(r.get("status_code"))
        statuses[s] = statuses.get(s, 0) + 1

    # hasta 10 errores como muestra
    sample_errors = []
    for r in rows:
        if r.get("status_code") != 200:
            sample_errors.append(
                {
                    "key": r.get("key"),
                    "status_code": r.get("status_code"),
                    "response": r.get("response"),
                }
            )
        if len(sample_errors) >= 10:
            break

    summary = {
        "total": total,
        "ok_200": ok,
        "failed": bad,
        "status_distribution": statuses,
        "sample_errors": sample_errors,
    }

    path_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    country = rows[0].get("country") if rows else "N/A"
    md = []
    md.append(f"# Reporte Checkout ({country})")
    md.append("")
    md.append(f"- Total requests: **{total}**")
    md.append(f"- OK (200): **{ok}**")
    md.append(f"- Failed (!=200): **{bad}**")
    md.append("")
    md.append("## Distribución por status")
    for k, v in sorted(statuses.items(), key=lambda x: x[0]):
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Muestras de errores (hasta 10)")
    if sample_errors:
        for e in sample_errors:
            md.append(f"- key={e['key']} status={e['status_code']} response={e['response']}")
    else:
        md.append("- Sin errores ✅")

    path_md.write_text("\n".join(md), encoding="utf-8")
