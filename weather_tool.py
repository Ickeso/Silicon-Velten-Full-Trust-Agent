#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ████████████████████████████████████████████████████████████████████
# FILE       : tools/weather_tool.py
# PROJECT    : FULL_TRUST_AGENT / MICROAGENT
# VERSION    : v22.1.2 ENTERPRISE – SANDBOX-CONTROLLED TIMEOUT & AUTO TZ
# ROLE       : 3‑Tage‑Vorhersage für jede Stadt weltweit, ohne API‑Key
# STATUS     : PRODUCTION READY – ENTERPRISE TOOL LAYER
# ----------------------------------------------------------------------
# v22.1.2 – ENTERPRISE-HÄRTUNG:
#   ✅ Signal-basierten Timeout entfernt (Sandbox steuert Prozess-Timeout)
#   ✅ timezone=auto für korrekte lokale Zeiten weltweit
#   ✅ Legacy-Wrapper (_tool_contract) vollständig entfernt
#   ✅ Platzhalter-Prüfung für city/location hinzugefügt
#   ✅ Klare ImportError-Behandlung für requests
#   ✅ Keine funktionalen Einbußen
# ████████████████████████████████████████████████████████████████████

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# ------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------
TIMEOUT = 15  # Sekunden (interner Request-Timeout, kein Prozess-Timeout)
AGENT_DEBUG = os.environ.get("AGENT_DEBUG", "0") == "1"

# Umfangreiche Städtetabelle – für sofortige Antworten ohne Geocoding
CITY_COORDS: Dict[str, Tuple[float, float]] = {
    "berlin": (52.52, 13.41),
    "münchen": (48.14, 11.58),
    "hamburg": (53.55, 9.99),
    "köln": (50.94, 6.96),
    "frankfurt": (50.11, 8.68),
    "stuttgart": (48.78, 9.18),
    "düsseldorf": (51.23, 6.78),
    "leipzig": (51.34, 12.37),
    "dortmund": (51.51, 7.47),
    "essen": (51.46, 7.01),
    "bremen": (53.08, 8.80),
    "dresden": (51.05, 13.74),
    "hannover": (52.37, 9.74),
    "nürnberg": (49.45, 11.08),
    "velten": (52.69, 13.18),
    "new york": (40.71, -74.01),
    "london": (51.51, -0.13),
    "paris": (48.86, 2.35),
    "tokio": (35.68, 139.76),
    "sydney": (-33.87, 151.21),
    "moskau": (55.76, 37.62),
    "peking": (39.91, 116.40),
    "rio de janeiro": (-22.91, -43.20),
}


def _debug(msg: str) -> None:
    if AGENT_DEBUG:
        print(f"[weather_tool] {msg}", file=sys.stderr, flush=True)


def _geocode_city(city: str) -> Optional[Tuple[float, float]]:
    """Ermittelt Koordinaten für jede beliebige Stadt weltweit über Open‑Meteo Geocoding."""
    import requests as req
    try:
        resp = req.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "language": "de", "format": "json"},
            timeout=TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        if "results" in data and len(data["results"]) > 0:
            r = data["results"][0]
            return r["latitude"], r["longitude"]
    except Exception as e:
        _debug(f"Geocoding fehlgeschlagen: {e}")
    return None


def run(payload: dict, action: dict) -> dict:
    """
    Holt eine 3‑Tage‑Wettervorhersage für eine beliebige Stadt weltweit
    über die kostenlose Open‑Meteo API (kein API‑Key nötig).

    Args:
        payload: {"city": "Berlin"} oder {"location": "Berlin"}
        action:  dict mit Metadaten (optional)

    Returns:
        {"status": "success", "data": {"city": ..., "forecast": [...]}, "error": None}
    """
    # ★ Platzhalter-Prüfung (Titanium)
    for key in ("city", "location"):
        val = payload.get(key)
        if isinstance(val, str) and "{{" in val:
            return {"status": "error", "data": {}, "error": f"Unresolved planner variable in {key}: {val}"}

    # ★ requests verfügbar?
    try:
        import requests as req
    except ImportError:
        return {"status": "error", "data": {}, "error": "requests library not installed"}

    city = (payload or {}).get("city") or (payload or {}).get("location", "")
    if not city:
        return {"status": "error", "data": {}, "error": "No city provided"}

    city_lower = city.strip().lower()

    coords = CITY_COORDS.get(city_lower)
    if not coords:
        _debug(f"Keine festen Koordinaten für '{city}', Geocoding wird gestartet...")
        coords = _geocode_city(city_lower)
        if not coords:
            return {"status": "error", "data": {}, "error": f"City not found: {city}"}

    try:
        params = {
            "latitude": coords[0],
            "longitude": coords[1],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",   # ✅ FIX: lokale Zeit für jede Stadt
            "forecast_days": 3
        }
        resp = req.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_probability_max", [])

        forecast = []
        for i in range(len(dates)):
            forecast.append({
                "date": dates[i],
                "temp_max": temps_max[i] if i < len(temps_max) else None,
                "temp_min": temps_min[i] if i < len(temps_min) else None,
                "precipitation_probability": precip[i] if i < len(precip) else None,
            })

        return {
            "status": "success",
            "data": {
                "city": city.capitalize(),
                "coordinates": {"lat": coords[0], "lon": coords[1]},
                "forecast": forecast,
                "units": "°C, %"
            },
            "error": None
        }

    except Exception as e:
        return {"status": "error", "data": {}, "error": str(e)}


# ------------------------------------------------------------
# SUBPROZESS-EINSTIEG (STANDARD)
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input.strip() else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "data": {}, "error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    # Flexibler Eingang: direktes Payload-Dict oder Action-Dict mit 'payload'-Schlüssel
    if isinstance(input_data, dict):
        if "payload" in input_data:
            payload = input_data["payload"] if isinstance(input_data["payload"], dict) else {}
        else:
            payload = input_data
        action = input_data.get("action", {}) if isinstance(input_data.get("action"), dict) else {}
    else:
        payload = {}
        action = {}

    result = run(payload, action)
    print(json.dumps(result, ensure_ascii=False))