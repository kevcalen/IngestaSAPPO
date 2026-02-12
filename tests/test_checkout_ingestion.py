import os
from src.runner import run_massive_checkouts

def test_checkout_massive_200():
    country = os.getenv("MI_RUTA_COUNTRY", "CL").upper().strip()
    volume = int(os.getenv("MI_RUTA_VOLUME", "1"))
    turn = int(os.getenv("MI_RUTA_TURN", "1"))
    start_transport = int(os.getenv("MI_RUTA_START_TRANSPORT", "1000001"))
    date_str = os.getenv("MI_RUTA_DATE") or None
    workers = int(os.getenv("MI_RUTA_WORKERS", "10"))

    results_path = run_massive_checkouts(
        country=country,
        volume=volume,
        turn=turn,
        start_transport=start_transport,
        date_str=date_str,
        workers=workers,
        out_dir="artifacts",
    )
    assert results_path.exists()
