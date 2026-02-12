from __future__ import annotations
import os
from dataclasses import dataclass


DEFAULT_BASE_URLS = {
  "BR": "https://wyt491chn1-vpce-0a0fb3bfae4c4521d.execute-api.us-east-1.amazonaws.com/develop/sap-po/checkouts",
  "AR": "https://k1c5p3ragd-vpce-0b490d8cf7ef7f4b4.execute-api.us-east-1.amazonaws.com/develop/sap-po/checkouts",
  "CL": "https://6ary7k823f-vpce-08f3fe9af82db4d33.execute-api.us-east-1.amazonaws.com/develop/sap-po/checkouts"
}

@dataclass(frozen=True)
class CountryConfig:
    country: str
    base_url: str
    api_key: str

def get_country_config(country: str) -> CountryConfig:
    c = country.upper().strip()

    base_url = os.getenv(f"MI_RUTA_BASE_URL_{c}") or DEFAULT_BASE_URLS.get(c)
    if not base_url:
        raise ValueError(
            f"No BASE_URL for {c}. Define MI_RUTA_BASE_URL_{c} as env/secret."
        )

    api_key = os.getenv(f"MI_RUTA_API_KEY_{c}")
    if not api_key:
        raise ValueError(
            f"No API KEY for {c}. Define MI_RUTA_API_KEY_{c} as env/secret."
        )

    return CountryConfig(country=c, base_url=base_url, api_key=api_key)
