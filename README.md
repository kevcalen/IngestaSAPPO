# Mi Ruta - Massive Checkout Automation (Develop)

Automatización de ingesta masiva de **Checkout** via API Gateway (POST `/sap-po/checkouts`),
validando **HTTP 200** y guardando evidencia por `key`.

## Stack
- Python 3.11
- pytest
- requests

## Cómo corre
Genera `key` como `{transportNumber}_{turn}` (ej: `1000001_1`) y reemplaza también el `date` en el JSON.

Los payloads base se toman desde `src/templates/checkout_<PAIS>.json` (derivados de la colección Postman).

## Variables de entorno
Requeridas:
- `MI_RUTA_COUNTRY`: CL | AR | BR | PY
- `MI_RUTA_API_KEY_<PAIS>`: API Key para el header `x-api-key`

Opcionales:
- `MI_RUTA_BASE_URL_<PAIS>`: endpoint completo del API Gateway para `/develop/sap-po/checkouts`
- `MI_RUTA_VOLUME`: cantidad de checkouts a ingerir (default 1)
- `MI_RUTA_TURN`: vuelta (default 1)
- `MI_RUTA_START_TRANSPORT`: número inicial para transport (default 1000001)
- `MI_RUTA_DATE`: fecha `YYYY-MM-DD` (default hoy)
- `MI_RUTA_WORKERS`: concurrencia (default 10)

## Ejecución local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export MI_RUTA_COUNTRY=CL
export MI_RUTA_API_KEY_CL="***"
export MI_RUTA_VOLUME=10
export MI_RUTA_TURN=1
export MI_RUTA_START_TRANSPORT=1000001
export MI_RUTA_DATE=2026-02-01

pytest -q
```

## GitHub Actions
Workflow: `.github/workflows/checkout.yml`

- Se ejecuta manualmente (`workflow_dispatch`)
- Permite escoger `country` o `ALL`
- Subirá un artifact `artifacts-<PAIS>` con el archivo `results_<PAIS>.jsonl`

## Siguiente fase (Paso 2) esperar que corra 
Luego se integra validación de persistencia en DynamoDB / AppSync con `boto3` (lectura), usando `key` y `date`.
