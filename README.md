Silicon Velten — Clay

Local-First KI-Agent für kontrollierte Geschäftsprozessautomatisierung

https://img.shields.io/badge/status-alpha-orange
https://img.shields.io/badge/lizenz-siehe%20LICENSE-blue
https://img.shields.io/badge/architektur-local--first-green
https://img.shields.io/badge/ausf%C3%BChrung-human--in--the--loop-yellow

Clay ist ein modularer KI-Agent, der komplexe Geschäftsprozesse in klar definierte, prüfbare und freigabepflichtige Schritte zerlegt. Der zentrale Architekturgedanke:

Das Sprachmodell darf planen — die Anwendung kontrolliert die Ausführung.

🎥 Live-Demo

▶️ Clay in Aktion: https://www.youtube.com/watch?v=XXVy7oCdnh0

Gezeigt wird ein vollständiger Beispielworkflow:

Aufgabe analysieren

Arbeitsablauf planen

Web-Recherche durchführen

Informationen verarbeiten

PDF erzeugen

E-Mail vorbereiten und kontrolliert versenden

🎯 Motivation

Viele KI-Assistenten werden als Cloud-Dienste betrieben. Für Unternehmen entstehen dadurch grundlegende Fragen, die vor einem produktiven Einsatz beantwortet werden müssen:

Wo werden Unternehmensdaten verarbeitet?

Welche Daten verlassen die eigene Infrastruktur?

Welche externen Dienste werden benötigt?

Welche laufenden API- oder Tokenkosten entstehen?

Welche Aktionen darf ein autonomer Agent tatsächlich ausführen?

Wie lässt sich eine KI-Aktion nachvollziehen und belegen?

Silicon Velten verfolgt deshalb einen Local-First-Ansatz: Die KI-Inferenz kann auf eigener Hardware betrieben werden. Sensible Workflows und Unternehmensdaten können innerhalb der eigenen Infrastruktur verarbeitet werden. Externe Dienste sind optional und explizit konfigurierbar — nicht implizit vorausgesetzt.
🧠 Was ist Clay?

Clay ist kein Chatbot. Es ist ein kontrollierter Agenten-Workflow, bestehend aus mehreren spezialisierten Komponenten.

Die fünf Ebenen:
Ebene Verantwortung

    Benutzer Aufgabe formulieren, Aktionen freigeben

    Planung Zerlegung in strukturierte, überprüfbare Arbeitsschritte

    Kontrolle Prüfung jeder geplanten Aktion gegen explizite Regeln

    Freigabe Menschliche Entscheidung bei sensiblen Aktionen

    Ausführung Ausschließlich genehmigte und regelkonforme Aktionen

Jede Ebene hat eine klar abgegrenzte Verantwortung. Es gibt keinen Pfad, über den das Sprachmodell direkt eine Aktion ausführt, ohne die Ebenen 3 und 4 zu passieren.
🔐 Sicherheitsmodell
„Full-Trust" bedeutet nicht blindes Vertrauen

Der Begriff Full-Trust Agent beschreibt in diesem Projekt nicht, dass dem Sprachmodell vertraut wird. Er beschreibt, dass die Anwendung die Ausführung kontrolliert — unabhängig davon, was das Modell plant.

Vereinfacht:
text

LLM-Output → Strukturierter Plan → Regelprüfung → Freigabe → Ausführung
(nicht vertrauenswürdig) (vertrauenswürdig)

Grundsätze

Kein implizites Vertrauen in Modell-Ausgaben. Jede geplante Aktion wird als Datenstruktur geparst und gegen Regeln geprüft.

Default Deny. Aktionen, die keiner explizit erlaubten Klasse zugeordnet werden können, werden abgelehnt — nicht ausgeführt.

Human-in-the-Loop für sensible Aktionen. Versand von E-Mails, Schreiben von Dateien, externe API-Aufrufe, Netzwerkzugriffe mit Nebenwirkungen und alles, was die Systemgrenzen verlässt, erfordern eine explizite Freigabe.

Audit-Trail. Jede geplante, geprüfte, freigegebene oder abgelehnte Aktion wird protokolliert.

Least Privilege. Der Agent erhält nur die Werkzeuge, die für den konfigurierten Workflow notwendig sind.

Keine stillen Fallbacks. Kann eine Aktion nicht ausgeführt werden, wird dies berichtet — nicht durch eine improvisierte Alternative ersetzt.

Local-First. Standardmäßig wird kein externer Dienst kontaktiert. Externe Endpunkte müssen explizit konfiguriert werden.

Was Clay ausdrücklich nicht ist

Kein Ersatz für Sicherheitskonzepte, Netzwerksegmentierung oder Berechtigungsmanagement.

Keine Garantie gegen Prompt Injection. Clay reduziert die Auswirkung, indem das Modell keine Ausführungsrechte besitzt — beseitigt die Angriffsfläche aber nicht.

Keine Zertifizierung (DSGVO, ISO 27001, SOC 2 o. ä.). Die Local-First-Architektur unterstützt Compliance, ersetzt sie aber nicht.

Kein Produktionssystem „out of the box". Siehe Projektstatus.

🏗️ Architektur (Überblick)
text

┌─────────────────────────────────────────────────────────┐
│ Benutzer │
│ Aufgabe · Freigabe · Audit-Einsicht │
└──────────────────────────┬──────────────────────────────┘
│
┌──────────────────────────▼──────────────────────────────┐
│ Planung │
│ LLM-gestützte Zerlegung in Schritte │
│ (nicht vertrauenswürdig) │
└──────────────────────────┬──────────────────────────────┘
│ strukturierter Plan
┌──────────────────────────▼──────────────────────────────┐
│ Kontrolle │
│ Regelprüfung · Policy-Engine · Default Deny │
└──────────────────────────┬──────────────────────────────┘
│ geprüfte Aktionen
┌──────────────────────────▼──────────────────────────────┐
│ Freigabe │
│ Human-in-the-Loop für sensible Operationen │
└──────────────────────────┬──────────────────────────────┘
│ genehmigte Aktionen
┌──────────────────────────▼──────────────────────────────┐
│ Ausführung │
│ Werkzeuge · Sandbox · Audit-Log · Abbruch │
└─────────────────────────────────────────────────────────┘

⚙️ Voraussetzungen

Lokal betriebenes Sprachmodell (z. B. über Ollama, llama.cpp oder einen kompatiblen OpenAI-kompatiblen Endpoint)

Python 3.10+ (bzw. die vom Setup-Skript geforderte Version)

Ausreichend RAM/VRAM für das gewählte Modell

Optional: SMTP-Zugang für E-Mail-Versand, ausgehender Netzwerkzugang für Web-Recherche

Hinweis: Externe Abhängigkeiten sind optional und werden nur aktiviert, wenn der jeweilige Workflow sie explizit benötigt.

🚀 Installation
bash
Repository klonen

git clone <repo-url>
cd silicon-velten-clay
Virtuelle Umgebung anlegen

python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
Abhängigkeiten installieren

pip install -r requirements.txt
Konfiguration anlegen (Beispiel siehe unten)

cp config.example.yaml config.yaml

Beispielkonfiguration (config.yaml)
yaml

llm:
provider: ollama
endpoint: http://127.0.0.1:11434
model: llama3.1:8b

policy:
default: deny
allowed_tools:

    web_search

    pdf_generate

    email_prepare
    require_approval:

    email_send

    file_write

audit:
path: ./audit/log.jsonl
level: info

▶️ Nutzung
bash
Agent starten

python -m clay run --config config.yaml --task "Recherchiere X und erstelle ein PDF"
Audit-Log ansehen

python -m clay audit --tail 50

Der Agent führt den Workflow schrittweise aus. Aktionen, die in require_approval gelistet sind, werden angehalten und zur Freigabe vorgelegt.
🧪 Projektstatus

Alpha. Der Fokus liegt auf der Architektur und dem Sicherheitsmodell, nicht auf Feature-Vollständigkeit.

Aktuell stabil:

Grundlegende Planung und Werkzeugausführung

Policy-Prüfung mit Default Deny

Freigabeschritt für sensible Aktionen

Audit-Logging

In Arbeit:

Erweiterte Policy-Sprache

Sandboxing der Werkzeuge

Rollen- und Rechteverwaltung

Persistente Workflow-Zustände

Nicht empfohlen für:

Unbeaufsichtigten Produktivbetrieb

Verarbeitung besonders sensibler Daten ohne eigene zusätzliche Absicherung

Szenarien, in denen eine fehlerhafte Aktion nicht rückgängig gemacht werden kann

🗺️ Roadmap (Auszug)

□

Policy-Engine mit deklarativer Regelsprache
□

Werkzeug-Isolation (Subprozess-Sandbox)
□

Signierte Audit-Logs
□

Rollenbasierte Freigabe (Vier-Augen-Prinzip)
□

Referenz-Workflows als Vorlagen
□

Optionale Integration externer LLM-Endpoints mit explizitem Opt-in

🤝 Beitragen

Beiträge sind willkommen. Bitte beachten:

Sicherheitsrelevante Änderungen zuerst als Issue diskutieren.

Keine PRs, die implizites Vertrauen in Modell-Ausgaben einführen.

Jede neue Werkzeugklasse braucht eine klare Policy-Zuordnung.

Tests für Kontroll- und Freigabelogik sind Pflicht.

📄 Lizenz

Siehe LICENSE.
⚠️ Haftungsausschluss

Clay ist ein Werkzeug. Die Verantwortung für die Verarbeitung von Unternehmensdaten, die Einhaltung regulatorischer Anforderungen und die Absicherung der Laufzeitumgebung liegt beim Betreiber. Die in dieser README gemachten Aussagen beschreiben beabsichtigtes Verhalten, keine Garantien.
📬 Kontakt

Silicon Velten
🌐 www.silicon-velten.de
✉️ info@silicon-velten.de
