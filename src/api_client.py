from __future__ import annotations
from typing import Any, Dict, Tuple
import requests

class ApiClient:
    def __init__(self, base_url: str, api_key: str, timeout_sec: int = 30):
        self.base_url = base_url
        self.timeout_sec = timeout_sec
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "x-api-key": api_key,
        })

    def post_checkout(self, payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any] | str]:
        r = self.session.post(self.base_url, json=payload, timeout=self.timeout_sec)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, r.text
