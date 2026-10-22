# Changelog

## 2.2.0 (2026-10-22)

Echte Debatte.

- Boardroom und Devil's Advocate mit zweiter Runde: Jeder Beirat antwortet namentlich einem anderen und benennt einen Widerspruch oder blinden Fleck.
- Abstimmung als Tabelle mit Votum, Zuversicht von 1 bis 10 und entscheidender Bedingung.
- Neuer Modus Pre-Mortem: „Ein Jahr später ist es schiefgegangen. Warum?“ mit Risikotabelle, Frühwarnzeichen und Gegenmaßnahmen.
- Unabhängige Stimmen auf Zuruf („unabhängig“): In Claude Code schreibt jeder Beirat seine erste Runde in einem eigenen Durchgang. Familienangaben aus dem Profil gehen nur an Beiräte mit Board `leben-coaching`. Ohne Subagents läuft der normale Ablauf mit Hinweis.
- Klarstellungen: Aufruf über den Namen einer Persona, 1:1 ohne Dossier, Abstimmung bei Wie-Fragen, persönliche Karten ohne `typ`.

## 2.1.0 (2026-10-22)

Tiefere Beiräte.

- Alle zwölf Beiräte im neuen Format: kompakte Karte für jede Session und ausführliches Dossier (Quellen, Denkmodelle, Beispielantworten, Abgrenzung) für das 1:1. Zitate nur mit Fundstelle.
- Inhaltsverzeichnis `roster.md` mit Boards (`strategie-business`, `leben-coaching`, `entscheiden-denken`, `führung-zeit-geld`) und Reibungspartnern; neue Frontmatter-Felder `boards` und `reibung`.
- Dossier-Regel: Ein Dossier gilt nur zusammen mit seiner eigenen Karte. Wer einen Beirat persönlich ersetzt, bekommt dessen gebündeltes Dossier nicht untergeschoben.
- Neue Vorlagen `templates/karte-template.md` und `templates/dossier-template.md` ersetzen `director-template.md`.
- Prüfwerkzeug `tools/council_tool.py` für Format, Schreibregeln und Verzeichnis, mit Tests.

**Bitte beachten**: Eigene Beiräte im älteren Format funktionieren weiter. Wer bisher `director-template.md` kopiert hat, nimmt künftig `karte-template.md`.

## 2.0.0 (2026-10-22)

Archetypen und neuer Auftritt.

- **Namensregel**: Mit Namen bleiben nur historische, vor mehr als zehn Jahren verstorbene oder fiktive Personen (Steve Jobs, David Ogilvy, Andrew Grove, Sun Tzu, Harvey Specter). Sieben Direktoren sind jetzt Archetypen, die eine Denkschule verkörpern und nur auf ein Vorbild verweisen: Value-Investor (ähnlich wie Warren Buffett), Reichweiten-Macher (MrBeast), Weisheitslehrer (der Dalai Lama), Audience-Stratege (Rand Fishkin), Informationsarchitekt (Karl Kratz), Conversion-Forscher (André Morys), Familientherapeut (Jesper Juul).
- Neue Frontmatter-Felder `typ` (person, figur, archetyp) und `vorbild`. Vorbild-Namen funktionieren weiter als Aufruf („Frag Buffett“).
- Zitat-Regel: Archetypen sprechen in eigenen Leitsätzen und erzählen keine Lebensgeschichte ihres Vorbilds als eigene. Echte Zitate realer Personen nur mit Quelle.
- Stand-up mit zwei bis drei Direktoren (vorher fest drei).
- README neu: Einstieg ohne Vorwissen, Beispiel-Session, englische Kurzfassung, Social-Preview-Bild.
- Geviertstriche aus Personas, Template und Session-Vorlage entfernt.
- Template `director-template.md` um `typ`, `vorbild`, Archetyp-Disclaimer und Leitsätze ergänzt.

**Bitte beachten (Bruch)**: Sieben Persona-Dateien haben neue Namen, zum Beispiel `02-warren-buffett.md` → `02-value-investor.md`. Wer einen Standard-Direktor über den gleichen **Dateinamen** ersetzt hat, stellt seine Datei auf den gleichen **`slot`** um (steht im Frontmatter jeder Persona). Ersetzungen per `slot` funktionieren unverändert.

## 1.0.0 (2026-06-10)

Öffentliche Erstversion.

- 12 Standard-Direktoren als entpersonalisierte Defaults im Skill gebündelt (`directors/`)
- Zwei-Schichten-Architektur: Skill-Ordner (Update-Gebiet) getrennt vom persönlichen Ordner `~/.claude/council/` (Profil, eigene Direktoren, Sessions)
- Onboarding beim ersten Start (optionales persönliches Profil)
- Eigene Direktoren per `templates/director-template.md`, Ersetzen per Dateiname/Slot, Deaktivieren per `inactive_directors`
- Vier Modi: Stand-up, Boardroom, 1:1, Devil's Advocate
- Session-Output als Markdown-Datei mit Decision/Action/Risk/Open
