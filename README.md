# Council: dein virtueller Beirat für Claude

Ein Skill für Claude Code und die Claude Desktop App. Er stellt dir ein Board aus 12 Beirat-Direktoren zur Seite: Steve Jobs (Produkt), Warren Buffett (Geld), David Ogilvy (Marke), Andrew Grove (Management), MrBeast (Reichweite), Dalai Lama (Ethik), Sun Tzu (Strategie), Harvey Specter (Verhandlung), Rand Fishkin (SEO), Karl Kratz (Informationsarchitektur), André Morys (Conversion) und Jesper Juul (Familie & Beziehungen).

Du stellst eine Frage ("Frag das Council: Soll ich diesen Auftrag annehmen?"), das Council debattiert aus mehreren Perspektiven und liefert dir eine Session-Datei mit klaren Stimmen, sichtbaren Spannungen und einer verdichteten Empfehlung: Decision, Action, Risk, Open.

**Vier Modi:**

| Modus | Besetzung | Wofür |
|-------|-----------|-------|
| Stand-up | 3 Direktoren, knapp | Alltagsfragen |
| Boardroom | 5–7 Direktoren mit Debatte | Strategische Fragen |
| 1:1 | Ein Direktor im Deep-Dive | Klar fachliche Fragen |
| Devil's Advocate | Zwei sich reibende Direktoren | Entscheidungen mit zwei plausiblen Pfaden |

## Voraussetzungen

Claude Code (Terminal oder VS Code) oder die Claude Desktop App auf macOS/Linux. Sonst nichts.

## Installation

**Weg 1: Terminal (eine Zeile)**

```bash
git clone https://github.com/RiotErik/council-skill.git ~/.claude/skills/council
```

Falls macOS beim ersten `git`-Aufruf die Installation der "Command Line Developer Tools" anbietet: bestätigen, kurz warten, Befehl wiederholen.

**Weg 2: Claude installiert es für dich**

Füge diesen Text in Claude Code ein:

> Bitte installiere mir einen Skill: Klone https://github.com/RiotErik/council-skill.git in den Ordner ~/.claude/skills/council und bestätige mir, dass dort eine SKILL.md liegt.

In Claude Code funktioniert das direkt. In der Desktop App nur, wenn die App Befehle auf deinem Rechner ausführen darf.

**Weg 3: ZIP, ganz ohne Terminal**

1. Oben auf dieser GitHub-Seite: grüner Button "Code" → "Download ZIP"
2. ZIP entpacken, den Ordner von `council-skill-main` in `council` umbenennen
3. Im Finder Cmd+Shift+G drücken, `~/.claude/skills` eingeben, den Ordner dort hineinlegen

Danach Claude neu starten und testen: **"Frag das Council: …"**

## Erster Start

Beim ersten Aufruf bietet dir das Council an, ein persönliches Profil anzulegen (Name, Rolle, aktuelle Projekte, optional Familiensituation, Stil-Wünsche). Das Profil landet in `~/.claude/council/profile.md`, also außerhalb des Skills. Es macht die Empfehlungen deutlich passender, ist aber freiwillig.

**Wichtig: Alles Persönliche lebt in `~/.claude/council/`** (Profil, eigene Direktoren, deine Sessions). Dieser Ordner gehört dir und wird von Updates nie angefasst. Ändere nichts direkt im Skill-Ordner `~/.claude/skills/council/`, der wird beim nächsten Update überschrieben.

## Eigene Direktoren in 3 Schritten

1. Kopiere `templates/director-template.md` aus dem Skill-Ordner
2. Fülle es aus (Hintergrund, Stimme, Werte, Lens, typische Fragen, Zitate)
3. Lege die Datei in `~/.claude/council/directors/`, z. B. als `13-meine-mentorin.md`

Oder einfacher: Sag Claude "Bau mir einen Council-Direktor für [Thema/Person]", der Skill führt dich durch das Template. Genauso kannst du Standard-Direktoren ersetzen (gleicher Dateiname oder gleicher `slot` in deinem Ordner gewinnt) oder deaktivieren (`inactive_directors` in deinem Profil).

## Update

```bash
git -C ~/.claude/skills/council pull
```

Oder per Prompt: "Bitte aktualisiere meinen Council-Skill: führe in ~/.claude/skills/council ein git pull aus." (ZIP-Installation: einfach Vorgang wiederholen und den alten Ordner ersetzen. Dein persönlicher Ordner bleibt davon unberührt.)

**Reparatur**, falls `git pull` meckert, weil im Skill-Ordner etwas geändert wurde:

```bash
git -C ~/.claude/skills/council fetch && git -C ~/.claude/skills/council reset --hard origin/main
```

## Wichtige Hinweise

**Die Direktoren sind fiktive Modellbildungen.** Sie sind von öffentlichen Aussagen, Büchern und Auftritten der jeweiligen Personen inspiriert. Es besteht keine Verbindung zu den realen Personen (bzw. bei Harvey Specter zur Figur und deren Rechteinhabern), und nichts an diesem Projekt ist von ihnen autorisiert oder gebilligt. Zitate sind entweder belegte Originalzitate oder ausdrücklich als sinngemäß gekennzeichnet.

**Das Council ersetzt keine Fachberatung.** Bei rechtlichen, steuerlichen oder medizinischen Fragen strukturiert es höchstens dein Denken; entscheiden müssen Anwalt, Steuerberater oder Arzt.

## Versionen

Siehe [CHANGELOG.md](CHANGELOG.md). Aktuelle Version: 1.0.0.

## Lizenz

MIT, siehe [LICENSE](LICENSE). Erstellt von Erik Lichtenecker.
