# Changelog

## 1.0.0 (2026-06-10)

Öffentliche Erstversion.

- 12 Standard-Direktoren als entpersonalisierte Defaults im Skill gebündelt (`directors/`)
- Zwei-Schichten-Architektur: Skill-Ordner (Update-Gebiet) getrennt vom persönlichen Ordner `~/.claude/council/` (Profil, eigene Direktoren, Sessions)
- Onboarding beim ersten Start (optionales persönliches Profil)
- Eigene Direktoren per `templates/director-template.md`, Ersetzen per Dateiname/Slot, Deaktivieren per `inactive_directors`
- Vier Modi: Stand-up, Boardroom, 1:1, Devil's Advocate
- Session-Output als Markdown-Datei mit Decision/Action/Risk/Open
