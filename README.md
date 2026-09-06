# 🛡️ Silicon Velten – Full Trust Agent „Clay“

**Enterprise AI Agent Framework**  
*Lokal, privat, plattformübergreifend – mit Human‑in‑the‑Loop und mobiler Genehmigung.*

---

## 📌 Überblick

**Clay** ist ein vollständig lokal betriebener KI‑Agent, der komplexe Geschäftsprozesse automatisiert – von der Web‑Recherche über Dokumentenerstellung bis zum Versand von Rechnungen. Er wurde als **datenschutzkonforme Alternative zu Cloud‑Assistenten** entwickelt und kombiniert modernste Sprachmodelle mit deterministischer Ausführungslogik.

Das Besondere: **Clay läuft auf einem schlanken Linux‑System (Kali)** und nutzt ein **separates Windows‑System mit GPU** ausschließlich für das Sprachmodell. Die Kommunikation erfolgt über ein privates, verschlüsseltes Netzwerk (Tailscale). Dadurch entstehen **keine Token‑Kosten**, **keine Datenabwanderung ins Ausland** und eine **nahezu vollständige DSGVO‑Konformität**.

---

## 🎯 Ziele & Design‑Prinzipien

- **Volle Datenhoheit:** Alle Daten bleiben auf den eigenen Systemen. Es werden keine Cloud‑Dienste für die KI‑Verarbeitung genutzt.
- **Transparenz & Kontrolle:** Jeder Schritt von Clay wird protokolliert und kann vor der Ausführung genehmigt werden – auch von unterwegs.
- **Erweiterbarkeit:** Neue Werkzeuge werden automatisch erkannt und integriert, ohne den Kern zu verändern.
- **Sicherheit:** Werkzeuge laufen in isolierten Subprozessen, Ergebnisse werden signiert, Kommunikation ist verschlüsselt.
- **Plattformunabhängigkeit:** Der Agent selbst ist ressourcenschonend und läuft auf beliebigen Linux‑Systemen; die rechenintensive Modellinferenz wird auf einem Windows‑Rechner mit GPU ausgelagert.

---

## 🧠 Architektur im Überblick

mermaid
graph TD
    A[Benutzer] --> B[GUI PySide6]
    C[Mobile App] --> D[Mobile Bridge]
    B --> E[Approval & Human-in-the-Loop]
    D --> E
    E --> F[SmartCore]
    F --> G[Planner]
    F --> H[Memory & Context]
    F --> I[Executor]
    I --> J[Tool Registry]
    I --> K[Model Manager]
    J --> L[Tools 30+]
    K --> M[LM Studio / OpenAI-kompatibel]


### 🖥️ Clay auf Kali Linux – Modell auf Windows

- **Agent (Clay):** Läuft auf einem schlanken Linux‑System (z. B. Kali). Hier werden Planung, Tool‑Ausführung, Genehmigungslogik und Speicher verwaltet. Benötigt nur minimale Ressourcen.
- **Sprachmodell:** Wird in **LM Studio** auf einem Windows‑Rechner mit leistungsfähiger GPU betrieben. Aktuell kommt **dolphin 2.9.3 Mistral Nemo** zum Einsatz – ein leistungsstarkes, lokal ausführbares Modell.
- **Verbindung:** Beide Systeme kommunizieren über **Tailscale** – ein privates, verschlüsseltes Mesh‑Netzwerk. So kann der Modellserver sicher im lokalen Netz oder sogar an einem anderen Standort betrieben werden, ohne öffentliche IPs oder Cloud‑Dienste.
- **Vorteile dieser Architektur:**
  - **Keine Token‑Kosten:** Da das Modell lokal läuft, fallen keine nutzungsabhängigen Gebühren an.
  - **Kein Abwandern von Daten ins Ausland:** Es werden keine Daten an externe Server gesendet; alles bleibt in der eigenen Infrastruktur.
  - **Nahezu DSGVO‑konform:** Durch lokale Verarbeitung, minimale Datenerhebung und vollständige Audit‑Protokolle sind die Anforderungen der DSGVO weitgehend erfüllt. Bei Einsatz externer Dienste (z. B. Tavily für Websuche) kann durch entsprechende Verträge die Konformität weiter abgesichert werden.

---

## ✨ Was Clay bereits kann

### 🧠 Autonome Planung & Ausführung
- **Aufgabenzerlegung:** Clay analysiert eine Anfrage in natürlicher Sprache und plant selbstständig die notwendigen Schritte.
- **Selbstheilung:** Bei Fehlern erkennt Clay das Problem und sucht automatisch alternative Lösungswege, ohne dass ein Mensch eingreifen muss.
- **Selbstoptimierung:** Aus vergangenen Ausführungen lernt Clay und verbessert seine Strategien kontinuierlich.
- **Kontextbewusstsein:** Ein mehrschichtiges Memory‑System (Kurzzeit‑, Langzeit‑ und Reflexionsspeicher) sorgt dafür, dass Clay auch über mehrere Interaktionen hinweg kohärent bleibt.

### 🛠️ Integrierte Werkzeuge (über 30)
Clay verfügt über eine umfangreiche Tool‑Bibliothek, die sich nahtlos erweitern lässt:

| Kategorie | Beispiele |
|-----------|-----------|
| **Web & Recherche** | Tavily, DuckDuckGo, Playwright‑Scraping, universeller Fetcher, OSINT |
| **Dokumentenerstellung** | Excel‑Berichte, PDF‑Export, Rechnungserstellung, Projekt‑Scaffolding |
| **Kommunikation** | E‑Mail‑Versand mit Audit‑Trail |
| **Datenzugriff** | SQL‑Datenbanken, SAP‑Anbindung, Dateisystem‑Operationen |
| **Business‑Logik** | HR‑Tool, Logistik‑Tool, Finanzdaten (yfinance), Wetterdaten |
| **Entwicklung** | Code‑Tool, Abhängigkeitsprüfung, Shell‑Ausführung (sandboxed) |

### 🔐 Sicherheits‑ und Genehmigungsarchitektur
- **Human‑in‑the‑Loop:** Bevor Clay eine Aktion ausführt, kann er eine Genehmigung anfordern. Der Plan wird dabei **vollständig angezeigt** – in der Desktop‑GUI und **per Push auf das Smartphone**.
- **Mobile Genehmigung von überall:** Über die Mobile Bridge wird die Genehmigungsanfrage mit dem gesamten Plan an dein Handy gesendet. Du kannst jeden Schritt einzeln oder den gesamten Plan **von überall bestätigen oder ablehnen**.
- **Bestätigungs‑Popup:** Auch am Desktop erscheint vor der Ausführung ein übersichtliches Popup, das den Plan darstellt und eine bewusste Entscheidung ermöglicht.
- **Sandboxing & Signierung:** Jedes Tool läuft in einem isolierten Subprozess, Ergebnisse werden kryptografisch signiert, und die Kommunikation zwischen Agent und Modellserver ist verschlüsselt.
- **Audit‑Chain:** Alle Aktionen werden manipulationssicher protokolliert – wichtig für Compliance und Nachvollziehbarkeit.

### 📊 GUI & Monitoring
- Eine moderne **PySide6‑Oberfläche** mit Analyse‑Panel und Timeline‑Visualisierung zeigt den Fortschritt, Zwischenschritte und Ergebnisse in Echtzeit.
- Alle Logs und Audit‑Trails sind zentral einsehbar.

---

## 💻 Systemanforderungen

### Agent (Clay) – Kali Linux oder anderes Linux
| Komponente    | Minimum          | Empfohlen        |
|---------------|------------------|------------------|
| **CPU**       | 2 Kerne          | 4 Kerne          |
| **RAM**       | 4 GB             | 8 GB             |
| **Festplatte**| 10 GB frei       | 20 GB SSD        |
| **Netzwerk**  | Tailscale‑Client | –                |

### Modellserver (Windows mit GPU)
| Komponente    | Minimum                 | Empfohlen                     |
|---------------|-------------------------|-------------------------------|
| **GPU (VRAM)**| 8 GB (quantisiert)      | 12 GB oder mehr               |
| **RAM**       | 16 GB                   | 32 GB                         |
| **Festplatte**| 20 GB (Modell + LM Studio) | 50 GB SSD                  |
| **Software**  | LM Studio, Modell dolphin 2.9.3 Mistral Nemo | –            |

> **Hinweis:** Beide Systeme müssen im selben Tailscale‑Netzwerk sein. Der Agent erreicht das Modell über die lokale IP oder den Tailscale‑Namen des Windows‑Rechners.

---

## 📦 Installation

### 1. Voraussetzungen
- **Python 3.10 – 3.13** auf dem Linux‑System.
- **LM Studio** auf dem Windows‑Rechner mit geladenem Modell **dolphin 2.9.3 Mistral Nemo**.
- **Tailscale** auf beiden Systemen installiert und angemeldet.
- Optional: API‑Keys für Tavily (Websuche) – dann muss ggf. ein Auftragsverarbeitungsvertrag abgeschlossen werden.

### 2. Projekt einrichten (auf dem Linux‑System)
bash
# Ordner anlegen und wechseln
cd agent

# Virtuelle Umgebung erstellen
python3 -m venv .venv

# Aktivieren
source .venv/bin/activate


### 3. Abhängigkeiten installieren
bash
pip install -r requirements.txt


### 4. Konfiguration
Erstellen Sie eine `.env`‑Datei im Projektordner:

env
# Modell‑Server (Windows‑Rechner über Tailscale)
LM_STUDIO_URL=http://<tailscale-ip-des-windows-rechners>:1234/v1
MODEL_NAME=dolphin-2.9.3-mistral-nemo

# Tailscale‑Name des Modellservers (optional statt IP)
# MODEL_SERVER_HOST=my-windows-pc

# API‑Keys (optional, nur wenn externe Dienste genutzt werden)
TAVILY_API_KEY=ihr_tavily_key

# Sicherheit
LICENSE_FILE=license.key
PUBLIC_KEY_PATH=public_key.pem

# Weitere Einstellungen
LOG_LEVEL=INFO
AUDIT_ENABLED=true


### 5. Starten
bash
python main.py

Die GUI startet automatisch. Alternativ headless: `python main.py --no-gui`

---

## 🚀 Nutzung

### Typischer Ablauf
1. **Aufgabe eingeben:** In der GUI eine Aufgabe in natürlicher Sprache formulieren.
2. **Planung:** Clay erstellt einen detaillierten Plan und zeigt ihn an.
3. **Genehmigung:** Du erhältst eine Anfrage – auf dem Desktop und/oder per Push aufs Handy. Der **komplette Plan wird angezeigt**.
4. **Bestätigung:** Du kannst jeden Schritt einzeln oder den gesamten Plan freigeben – von überall.
5. **Ausführung:** Clay arbeitet die Schritte ab, überwacht Ergebnisse und protokolliert alles.
6. **Ergebnis:** Generierte Dateien (PDF, Excel, Rechnungen) liegen im `output/`‑Ordner.

### Beispiel: Rechnung erstellen und versenden

Aufgabe: "Erstelle eine Rechnung für Kunde Schmidt, 5 Stunden à 80 €, und sende sie per E‑Mail an dirk@example.com."

Clay wird:
- Die Daten validieren,
- ein PDF generieren,
- eine Genehmigung für den E‑Mail‑Versand anfordern (Plan wird auf dem Handy angezeigt),
- nach Freigabe die E‑Mail senden,
- alle Schritte im Audit‑Log dokumentieren.

### Mobile Genehmigung im Detail
- **Push aufs Smartphone:** Die Mobile Bridge sendet eine Benachrichtigung mit dem vollständigen Plan.
- **Bestätigen von überall:** Über die Benachrichtigung oder die zugehörige App kannst du den Plan prüfen und mit einem Tap freigeben oder ablehnen.
- **Desktop‑Popup:** Parallel erscheint ein Fenster mit demselben Plan, falls du am Rechner bist.

---

## 📁 Projektstruktur


agent/
├── core/               # Herzstück: SmartCore, Planner, Events, Types
├── executor/           # Runner, Sandbox, Tool‑Gateway, Recovery
├── tools/              # Alle Business‑Tools (Excel, PDF, Mail, …)
├── gui/                # PySide6‑Oberfläche
├── registry/           # Tool‑Registry (Single Source of Truth)
├── approval/           # Human‑in‑the‑Loop, Mobile‑Bridge
├── models/             # LM‑Studio‑Anbindung, Prompt‑Strategie
├── memory/             # Core‑Memory, Reflection, Rules
├── assets/             # Logo, Schriften
├── logs/               # Audit‑Logs (werden automatisch angelegt)
├── output/             # Generierte Dateien (Rechnungen, Berichte)
├── .env                # Konfiguration (API‑Keys, Pfade, Modus)
├── requirements.txt    # Alle Python‑Abhängigkeiten
└── README.md           # Diese Datei


---

📸 Screenshots
Aufgabenstellung	Excel-Ausgabe	Genehmigungs-Popup
https://assets/aufgabe.jpg	https://assets/excel.jpg	https://assets/popup.jpg

Die Screenshots zeigen die grafische Oberfläche von Clay mit Aufgabenstellung, generiertem Excel-Bericht und dem Genehmigungs-Popup.
🎥 Demo-Video
<video width="100%" controls> <source src="assets/demo.mp4" type="video/mp4"> Dein Browser unterstützt kein HTML5-Video. Bitte lade das Video <a href="assets/demo.mp4">hier herunter</a>. </video>

Das Video demonstriert eine typische Interaktion mit Clay: Aufgabenstellung, Planung, Genehmigung und Ausführung.
📜 Lizenz

Diese Software ist proprietär.
Nutzung, Vervielfältigung oder Modifikation sind ausschließlich mit einer gültigen, signierten Lizenzdatei gestattet.
Weitergabe oder Reverse Engineering sind ausdrücklich untersagt.

---

## 📮 Support & Kontakt

- **E‑Mail:** dirkschmidt392@gmail.com   
- **Webseite:**  

*Built with ❤️ in Velten – Enterprise AI Made Local.*