#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ████████████████████████████████████████████████████████████████████
# FILE       : tools/universal_fetcher.py
# PROJECT    : FULL_TRUST_AGENT / MICROAGENT
# VERSION    : v24.0.0 TITANIUM – PRÄZISE FEHLERBEHANDLUNG
# STATUS     : PRODUCTION READY – DETERMINISTISCH, ISOLIERT
# ----------------------------------------------------------------------
# v24.0.0 – ÄNDERUNGEN:
#   ✅ Gezielte Exception-Typen (RequestException, JSONDecodeError)
#   ✅ Alle Fehler werden über _debug geloggt
#   ✅ Kein stilles Scheitern – jeder Fehler wird zurückgegeben und protokolliert
#   ✅ Einheitlicher User-Agent (TitaniumAgent/24.0)
# ████████████████████████████████████████████████████████████████████

import json
import os
import sys
from typing import Any, Dict, List, Optional

# ------------------------------------------------------------
# IMPORT-PRÜFUNG
# ------------------------------------------------------------
REQUESTS_OK = False
requests = None
try:
    import requests as _requests
    requests = _requests
    REQUESTS_OK = True
except ImportError:
    pass

# ------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------
TIMEOUT = 10  # Sekunden (interner Request-Timeout)
AGENT_DEBUG = os.environ.get("AGENT_DEBUG", "0") == "1"


def _debug(msg: str) -> None:
    if AGENT_DEBUG:
        print(f"[universal_fetcher] {msg}", file=sys.stderr, flush=True)


# ------------------------------------------------------------
# TOOL-CONTRACT
# ------------------------------------------------------------
def run(payload: dict, action: dict) -> dict:
    """
    Ruft DuckDuckGo Instant Answer API auf (keyless, deutsche Antworten).

    Args:
        payload: {"query": "Albert Einstein"} (beliebige Suchanfrage)
        action:  dict mit Metadaten (optional)

    Returns:
        {"status": "success", "data": {...}, "error": None}
        oder
        {"status": "error", "data": {}, "error": "Beschreibung"}
    """
    if not isinstance(payload, dict):
        payload = {}

    # Query-Typ strikt prüfen
    raw_query = payload.get("query")
    if raw_query is None:
        return {"status": "error", "data": {}, "error": "No query provided"}

    if not isinstance(raw_query, str):
        return {
            "status": "error",
            "data": {},
            "error": f"Invalid query type: expected string, got {type(raw_query).__name__}"
        }

    query = raw_query.strip()
    if not query:
        return {"status": "error", "data": {}, "error": "No query provided"}

    # Platzhalter-Prüfung
    if "{{" in query:
        return {
            "status": "error",
            "data": {},
            "error": f"Unresolved planner variable in query: {query}"
        }

    if not REQUESTS_OK:
        return {"status": "error", "data": {}, "error": "requests not installed"}

    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; TitaniumAgent/24.0)",
                "Accept-Language": "de-DE,de;q=0.9"
            }
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        _debug(f"Request-Fehler bei DuckDuckGo: {e}")
        return {"status": "error", "data": {}, "error": f"Request failed: {e}"}

    try:
        data = resp.json()
    except json.JSONDecodeError as e:
        _debug(f"Ungültige JSON-Antwort: {e}")
        return {"status": "error", "data": {}, "error": f"Invalid JSON response: {e}"}

    # RelatedTopics robust extrahieren
    related_raw = data.get("RelatedTopics", [])
    related_topics: List[str] = []
    if isinstance(related_raw, list):
        for topic in related_raw[:5]:
            if isinstance(topic, dict) and topic.get("Text"):
                related_topics.append(str(topic.get("Text", "")))
    elif isinstance(related_raw, dict) and related_raw.get("Text"):
        related_topics.append(str(related_raw.get("Text", "")))

    result_data = {
        "abstract": data.get("AbstractText", ""),
        "answer": data.get("Answer", ""),
        "answer_type": data.get("AnswerType", ""),
        "related_topics": related_topics,
        "source_url": data.get("AbstractURL", ""),
        "heading": data.get("Heading", ""),
        "image": data.get("Image", ""),
        "source": "duckduckgo_instant_answer"
    }

    # Nur die inhaltlich relevanten Felder prüfen
    informative_fields = [
        result_data.get("abstract"),
        result_data.get("answer"),
        result_data.get("related_topics"),
        result_data.get("source_url"),
        result_data.get("heading"),
        result_data.get("image"),
    ]
    if not any(v for v in informative_fields if v not in ("", [])):
        return {
            "status": "error",
            "data": {},
            "error": "DuckDuckGo returned no information for this query"
        }

    return {"status": "success", "data": result_data, "error": None}


# ------------------------------------------------------------
# SUBPROZESS-EINSTIEG
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input.strip() else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "data": {}, "error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    # Akzeptiert sowohl direkten Payload als auch Action-Dict
    if isinstance(input_data, dict):
        if "payload" in input_data:
            payload = input_data["payload"]
        else:
            payload = input_data
        action = input_data.get("action", {})
    else:
        payload = {}
        action = {}

    result = run(payload, action)
    print(json.dumps(result, ensure_ascii=False))