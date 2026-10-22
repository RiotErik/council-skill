# Changelog

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
