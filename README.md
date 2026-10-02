Silicon Velten — Clay
Full-Trust Enterprise Agent für kontrollierte Geschäftsprozessautomatisierung

Silicon Velten · www.silicon-velten.de · info@silicon-velten.de

    Das Sprachmodell darf planen — die Anwendung kontrolliert die Ausführung.

Silicon Velten — Clay ist ein modularer KI-Agent für die Automatisierung komplexer Geschäftsprozesse. Er verbindet ein lokal betriebenes Sprachmodell mit einer kontrollierten Agentenarchitektur aus Planung, Kontrolle, Freigabe und auditierter Ausführung.
🎥 Live-Demo

▶ Clay in Aktion auf YouTube ansehen

Der vollständige Beispielworkflow:
#	Schritt	Beschreibung
1	Aufgabe analysieren	Auftrag erfassen und verstehen
2	Arbeitsablauf planen	Zerlegung in prüfbare Einzelschritte
3	Web-Recherche	Kontrollierter Zugriff auf Informationsquellen
4	Informationen verarbeiten	Strukturierung und Aufbereitung
5	PDF erzeugen	Dokumentgenerierung
6	E-Mail versenden	Vorbereitung und kontrollierter Versand
🖼️ Screenshots

https://assets/aufgabe.jpg

Aufgabenstellung im Agenten

https://assets/popup.jpg

Freigabedialog vor einer kritischen Aktion

https://assets/excel.jpg

Automatisch generierter Excel-Bericht
🎯 Motivation

Viele moderne KI-Assistenten werden als Cloud-Dienste betrieben. Für Unternehmen entstehen dadurch grundlegende Fragen, die vor einem produktiven Einsatz beantwortet werden müssen:

    Wo werden Unternehmensdaten verarbeitet?

    Welche Daten verlassen die eigene Infrastruktur?

    Welche externen Dienste werden benötigt?

    Welche laufenden API- oder Tokenkosten entstehen?

    Welche Aktionen darf ein autonomer Agent tatsächlich ausführen?

    Wie lässt sich eine KI-Aktion nachvollziehen und belegen?

Silicon Velten verfolgt deshalb einen Local-First-Ansatz: Die KI-Inferenz kann auf eigener Hardware betrieben werden. Sensible Workflows und Unternehmensdaten bleiben innerhalb der eigenen Infrastruktur. Externe Dienste sind optional und explizit konfigurierbar — nicht implizit vorausgesetzt.
🧠 Was ist Clay?

Clay ist kein Chatbot. Es ist ein kontrollierter Agenten-Workflow, bestehend aus spezialisierten Komponenten mit klar getrennten Verantwortlichkeiten.
Die fünf Ebenen
Ebene	Verantwortung
1. Benutzer	Aufgabe formulieren und Aktionen freigeben
2. Planung	Zerlegung in strukturierte, prüfbare Arbeitsschritte
3. Kontrolle	Prüfung jeder geplanten Aktion gegen explizite Regeln
4. Freigabe	Menschliche Entscheidung bei sensiblen Aktionen
5. Ausführung	Ausschließlich genehmigte und regelkonforme Aktionen

Jede Ebene hat eine klar abgegrenzte Verantwortung. Es gibt keinen Pfad, über den das Sprachmodell direkt eine Aktion ausführt, ohne die Ebenen 3 und 4 zu passieren.
🔐 Sicherheitsmodell
„Full-Trust" bedeutet nicht blindes Vertrauen

Der Begriff Full-Trust Agent beschreibt in diesem Projekt ausdrücklich nicht, dass dem Sprachmodell blind vertraut wird. Er beschreibt, dass die Anwendung die Ausführung kontrolliert — unabhängig davon, was das Modell plant.

    Benutzeranfrage → Analyse (Sprachmodell) → Plan → Kontrolle → Freigabe (bei kritischen Aktionen) → Kontrollierte Ausführung → Ergebnis → Audit / Telemetry

Das Modell ist nicht automatisch die letzte Instanz über eine Aktion.
Grundsätze
Prinzip	Bedeutung
Kein implizites Vertrauen	Modell-Ausgaben werden als Daten geparst und gegen Regeln geprüft, nie direkt ausgeführt
Default Deny	Unbekannte Aktionen werden abgelehnt, nicht ausgeführt
Human-in-the-Loop	Sensible Aktionen erfordern explizite menschliche Freigabe
Audit-Trail	Jede geplante, geprüfte, freigegebene oder abgelehnte Aktion wird protokolliert
Least Privilege	Der Agent erhält nur die Werkzeuge, die er wirklich braucht
Keine stillen Fallbacks	Fehlgeschlagene Aktionen werden berichtet, nicht improvisiert ersetzt
Local-First	Kein externer Dienst ohne explizite Konfiguration
Was Clay ausdrücklich nicht ist

    ❌ Kein Ersatz für Sicherheitskonzepte, Netzwerksegmentierung oder Berechtigungsmanagement

    ❌ Keine Garantie gegen Prompt Injection — Clay reduziert die Auswirkung, beseitigt die Angriffsfläche aber nicht

    ❌ Keine Zertifizierung (DSGVO, ISO 27001, SOC 2 o. ä.) — Local-First unterstützt Compliance, ersetzt sie aber nicht

    ❌ Kein Produktionssystem „out of the box" — siehe Projektstatus

🛡️ Human-in-the-Loop

Eine der wichtigsten Funktionen von Clay ist die menschliche Kontrolle kritischer Aktionen. Der Agent kann einen vollständigen Plan erstellen. Vor freigabepflichtigen Aktionen wird der Ablauf dem Benutzer vorgelegt. Der Mensch entscheidet, ob die Aktion ausgeführt werden darf.

Beispiel: Aufgabe „Erstelle einen Bericht und sende ihn per E-Mail."
#	Schritt	Status
1	Aufgabe analysieren	automatisch
2	Recherche durchführen	automatisch
3	Daten verarbeiten	automatisch
4	PDF erstellen	automatisch
5	E-Mail vorbereiten	automatisch
6	Versand zur Freigabe vorlegen	⏸️ wartet auf Mensch
7	Nach Freigabe versenden	nach Freigabe
8	Vorgang protokollieren	automatisch
🔐 Kontrollschicht

Clay besitzt eine eigene Kontrollschicht, die außerhalb des Sprachmodells sitzt.

Grundidee: Nicht jede vom Sprachmodell vorgeschlagene Aktion darf automatisch ausgeführt werden. Aktionen werden nach ihrer Kritikalität unterschiedlich behandelt — von „direkt ausführbar" bis „grundsätzlich gesperrt".

    Die konkrete Klassifizierung ist Teil des geschützten Kerns und wird im persönlichen Gespräch erläutert.

🧱 Sicherheitsarchitektur

Die Architektur kombiniert mehrere Kontrollmechanismen:
Mechanismus	Funktion
Regelprüfung	Regeln bestimmen, welche Aktionen erlaubt, eingeschränkt oder freigabepflichtig sind
Human-in-the-Loop	Kritische Aktionen verlangen explizite menschliche Freigabe
Tool-Isolation	Werkzeuge werden kontrolliert ausgeführt
Audit Logging	Aktionen und Ergebnisse werden protokolliert
Circuit Breaker / Recovery	Fehlerhafte Abläufe werden kontrolliert beendet
Private Netzwerk-Kommunikation	Agent und Modellserver kommunizieren über private Netzwerke
Remote Approval	Freigaben können über eine Mobile Bridge von einem separaten Gerät erfolgen
⚠️ Bedrohungsmodell (Auszug)

Clay berücksichtigt bei der Architektur nicht nur normale Programmfehler, sondern auch mögliche Angriffs- und Manipulationsszenarien.

Betrachtete Szenarien: Prompt Injection · Manipulierte Webseiten · Manipulierte Dokumente · Kompromittierte Werkzeuge · Missbrauch privilegierter Aktionen · Kompromittierter Modellserver

Gegenmaßnahmen (Auszug): Trennung von Daten und Steuerlogik · Regelprüfung außerhalb des Sprachmodells · kontrollierte Werkzeuge · Freigabe für kritische Aktionen · Tool-Isolation · vollständiges Logging.
🧠 Architektur

Clay besteht aus mehreren spezialisierten Komponenten:
Komponente	Aufgabe
Zentrale Steuerung	Ablaufsteuerung, Kontextverwaltung, Fehlerbehandlung
Planung	Zerlegt natürliche Sprache in strukturierte Arbeitsschritte
Ausführung	Führt genehmigte Schritte kontrolliert aus
Kontext	Persistente Speichermechanismen für kurz- und langfristigen Kontext
Werkzeugverwaltung	Zentrale Registrierung aller verfügbaren Werkzeuge
🛠️ Werkzeugkategorien

Clay besitzt eine erweiterbare Werkzeuglandschaft. Die genaue Zusammensetzung ist konfigurations- und kundenabhängig.
Kategorie	Beispiele
Web-Recherche	Informationsbeschaffung, Quellenzugriff
Dokumente	Erstellung und Verarbeitung (PDF, Excel)
Kommunikation	E-Mail, Benachrichtigungen
Datenzugriff	Datenbanken, Dateisystem
Business-Automation	Wiederkehrende Workflows
Entwicklung	Code- und Entwicklerwerkzeuge
🌐 Local-First-Architektur

Eine der Besonderheiten von Silicon Velten ist die Trennung zwischen Agent und Modellserver.

Der Agent und die eigentliche Modellinferenz können auf unterschiedlichen Systemen betrieben und über ein privates Netzwerk verbunden werden. Dadurch kann Clay die Rechenleistung eines leistungsfähigen Systems nutzen, ohne dass der Agent selbst über entsprechende GPU-Ressourcen verfügen muss.

    Die konkrete Infrastruktur wird im persönlichen Gespräch erläutert.

💰 Kostenkontrolle

Ein wesentliches Ziel des Local-First-Ansatzes ist die Unabhängigkeit von nutzungsabhängigen Cloud-Tokenkosten für die eigentliche Modellinferenz.

Bei lokaler Inferenz entstehen keine API-Gebühren pro Token. Reale Kosten bleiben nur für Hardware, Strom, Wartung, Speicher und optionale externe Dienste.
📊 Telemetry & ROI

Clay besitzt Telemetrie- und Logging-Funktionen zur Nachvollziehbarkeit von Werkzeug-Aktionen und Arbeitsabläufen. Je nach Workflow können beispielsweise erfasst werden:

    Aufgabe und Ausführungsstatus

    Werkzeug-Nutzung

    Fehler

    Betriebskosten

    geschätzte Zeitersparnis

Beispielrechnung:
Aufwand	Dauer
Manuelle Bearbeitung	45 Minuten
Automatisierte Bearbeitung	8 Minuten
Zeitersparnis	37 Minuten pro Vorgang
🧠 Learning & Adaptation

Clay besitzt Mechanismen zur Verarbeitung vergangener Ausführungen und Fehler. Vergangene Ergebnisse können genutzt werden, um zukünftige Abläufe gezielter zu gestalten.

    Der Lernmechanismus ersetzt dabei nicht die Kontrollschicht.

🖥️ GUI & Monitoring

Clay besitzt eine grafische Benutzeroberfläche. Die Oberfläche kann unter anderem darstellen:

    Benutzeranfragen

    generierte Pläne

    Ausführungsstatus

    Ergebnisse

    Genehmigungsdialoge

    Logs und Zeitverläufe

    Werkzeug-Aktivitäten

Der Benutzer soll dadurch jederzeit erkennen können, was Clay gerade plant bzw. ausführt.
🎬 Demo-Workflow

Das aktuelle Demo-Video zeigt einen vollständigen Beispielworkflow:

    Benutzeranfrage → Planung → Web-Recherche → Datenverarbeitung → PDF-Erstellung → E-Mail → Kontrollierte Ausführung

▶ Demo ansehen
🏢 Mögliche Einsatzbereiche

    Web-Recherche

    Dokumentenanalyse

    Berichtserstellung

    PDF- und Excel-Erstellung

    E-Mail-Automatisierung

    Interne Wissenssysteme

    Datenverarbeitung

    Administrative Prozesse

    Wiederkehrende Business-Workflows

Fokus: Kontrollierte Automatisierung statt unkontrollierter Autonomie.
🧪 Entwicklungsphilosophie
Prinzip	Bedeutung
Control over Autonomy	Kontrollierte Ausführung ist wichtiger als maximale Autonomie
Local First	Lokale KI-Inferenz, wann immer technisch sinnvoll
Human in the Loop	Menschen bleiben bei kritischen Aktionen in der Entscheidungskette
Observable Systems	Aktionen und Ergebnisse sind nachvollziehbar
Modular Architecture	Neue Komponenten integrierbar ohne Neuentwicklung
Security by Design	Sicherheit ist Bestandteil der Architektur
🏗️ Projektstatus

Silicon Velten / Clay befindet sich in aktiver Entwicklung.

Aktuelle Schwerpunkte:

    Agenten-Architektur

    Planung und Steuerung

    Werkzeug-Ökosystem

    Human-in-the-Loop

    Kontrollschicht

    Kontext & Speicher

    Telemetrie

    Lokale Modell-Integration

    Web-Recherche

    Business-Automation

    Sicherheit

⭐ Project Highlights

✓ Local LLM · ✓ Agent Architecture · ✓ Planner & Steuerung · ✓ Werkzeug-Registry · ✓ Kontext & Speicher · ✓ Kontrollschicht · ✓ Human-in-the-Loop · ✓ Approval Workflow · ✓ Remote Approval · ✓ Web Research · ✓ PDF Generation · ✓ Excel Automation · ✓ E-Mail Automation · ✓ Telemetry · ✓ ROI Tracking · ✓ GUI · ✓ Modular Architecture · ✓ Security by Design
📜 Lizenz

Silicon Velten / Clay ist proprietäre Software.

Der Quellcode, die Architektur und die zugehörigen Komponenten sind geistiges Eigentum des Projektautors. Eine Nutzung, Vervielfältigung, Weitergabe, Modifikation oder kommerzielle Verwendung ist ohne entsprechende Genehmigung bzw. Lizenz nicht gestattet.
📬 Kontakt

Silicon Velten
🌐 www.silicon-velten.de
✉️ info@silicon-velten.de

Für Anfragen zu Lizenzierung, Integration oder individuellen Workflows kontaktieren Sie uns gerne direkt.

Silicon Velten — Full-Trust Enterprise Agent „Clay"
Developed in Germany.
