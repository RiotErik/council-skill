#!/usr/bin/env python3
"""Werkzeug für den Council-Skill: Personas prüfen und Inhaltsverzeichnis erzeugen.

Aufrufe (im Skill-Ordner):
  python3 tools/council_tool.py check [--streng] [--nur SLOT ...] [--pfad ORDNER]
  python3 tools/council_tool.py roster [--pfad ORDNER]

Nur Standardbibliothek. Exit-Code 0 = in Ordnung, 1 = Fehler gefunden.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TYPES = {"person", "figur", "archetyp"}
BOARDS = {"strategie-business", "leben-coaching", "entscheiden-denken", "führung-zeit-geld"}
REQUIRED_FIELDS = ["name", "typ", "slot", "domain", "tagline", "keywords"]
STRICT_FIELDS = ["boards", "reibung"]
CARD_SECTIONS = [
    "## Kurzporträt", "## Stimme", "## Denkmodelle", "## Lens", "## Blinde Flecken",
    "## Standard-Empfehlung", "## Leitsätze", "## Wann aufrufen",
]
DOSSIER_SECTIONS = [
    "## Quellen", "## Denkmodelle ausführlich", "## Beispielantworten",
    "## Zitate mit Fundstelle", "## Abgrenzung", "## Fehlbedienung",
]
CARD_WARN, CARD_MAX = 3500, 4500
EM_DASH = "—"
# Wortstämme mit Umlaut. Geprüft wird auf ihre Umschrift (ä zu ae usw.).
UMLAUT_STEMS = [
    "für", "über", "möcht", "könn", "wär", "grüß", "heiß", "schön", "spät", "führ",
    "änder", "möglich", "natürlich", "öffentlich", "wähl", "zurück", "gefühl", "prüf",
    "größ", "müss", "würd",
]
ROSTER_HEADER = (
    "# Inhaltsverzeichnis der Beiräte\n\n"
    "Automatisch erzeugt mit `python3 tools/council_tool.py roster`. Nicht von Hand bearbeiten.\n\n"
    "| Nr | Slot | Persona | Typ | Vorbild | Boards | Stichworte | Reibung | Karte | Dossier |\n"
    "|---|---|---|---|---|---|---|---|---|---|\n"
)


def _transliterate(word: str) -> str:
    return word.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")


TRANSLIT_RE = re.compile(
    r"\b\w*(?:" + "|".join(_transliterate(s) for s in UMLAUT_STEMS) + r")\w*\b", re.IGNORECASE
)
CONTRAST_RE = re.compile(r"\bnicht\b[^.!?\n]{0,120}\bsondern\b", re.IGNORECASE)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"FEHLER {where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"WARNUNG {where}: {message}")


def as_list(value) -> list[str]:
    if isinstance(value, list):
        return value
    return [value] if value else []


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None, text
    data: dict = {}
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = re.split(r"\s+#\s", value.strip())[0].strip()
        if value.startswith("[") and value.endswith("]"):
            data[key.strip()] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            data[key.strip()] = value
    return data, text[match.end():]


def has_section(body: str, prefix: str) -> bool:
    return any(line.startswith(prefix) for line in body.splitlines())


def section_text(body: str, heading: str) -> str:
    level = len(heading.split(" ")[0])
    lines, inside = [], False
    for line in body.splitlines():
        if line.startswith(heading):
            inside = True
            continue
        if inside and line.startswith("#") and len(line.split(" ")[0]) <= level:
            break
        if inside:
            lines.append(line)
    return "\n".join(lines)


def check_text_rules(rel: str, text: str, report: Report) -> None:
    for number, line in enumerate(text.splitlines(), start=1):
        where = f"{rel}:{number}"
        if EM_DASH in line:
            report.error(where, "Geviertstrich gefunden")
        for match in TRANSLIT_RE.finditer(line):
            report.error(where, f"Umlaut-Umschrift „{match.group(0)}“")
        if CONTRAST_RE.search(line):
            report.error(where, "Satzbau „nicht …, sondern …“")


def check_card(rel: str, text: str, strict: bool, report: Report) -> dict | None:
    front, body = parse_frontmatter(text)
    if front is None:
        report.error(rel, "Frontmatter fehlt (Datei muss mit --- beginnen)")
        return None
    for field in REQUIRED_FIELDS:
        if not front.get(field):
            report.error(rel, f"Pflichtfeld „{field}“ fehlt")
    typ = front.get("typ")
    if typ and typ not in TYPES:
        report.error(rel, f"typ „{typ}“ ungültig, erlaubt: person, figur, archetyp")
    if typ != "archetyp" and front.get("vorbild"):
        report.error(rel, "vorbild ist nur bei typ archetyp erlaubt")
    for board in as_list(front.get("boards")):
        if board not in BOARDS:
            report.error(rel, f"Board „{board}“ unbekannt")
    disclaimer = " ".join(
        line.lstrip(">").strip() for line in body.splitlines() if line.startswith(">")
    )
    if not disclaimer:
        report.error(rel, "Disclaimer (Zitatblock mit >) fehlt")
    elif typ == "archetyp":
        if "Archetyp" not in disclaimer:
            report.error(rel, "Archetyp-Disclaimer fehlt")
        vorbild = front.get("vorbild")
        if vorbild and f"ähnlich wie {vorbild}" not in disclaimer:
            report.error(rel, f"Disclaimer nennt nicht „ähnlich wie {vorbild}“")
    elif "Modellbildung" not in disclaimer:
        report.error(rel, "Disclaimer für Person oder Figur fehlt (Wort „Modellbildung“)")
    if strict:
        for field in STRICT_FIELDS:
            if not front.get(field):
                report.error(rel, f"Feld „{field}“ fehlt")
        for section in CARD_SECTIONS:
            if not has_section(body, section):
                report.error(rel, f"Abschnitt „{section}“ fehlt")
        if len(text) > CARD_MAX:
            report.error(rel, f"Karte zu lang: {len(text)} Zeichen (Grenze {CARD_MAX})")
        elif len(text) > CARD_WARN:
            report.warn(rel, f"Karte lang: {len(text)} Zeichen (Ziel {CARD_WARN})")
    return front


def check_dossier(rel: str, text: str, report: Report) -> None:
    _, body = parse_frontmatter(text)
    for section in DOSSIER_SECTIONS:
        if not has_section(body, section):
            report.error(rel, f"Abschnitt „{section}“ fehlt")
    primary = section_text(body, "### Primärquellen")
    count = sum(1 for line in primary.splitlines() if re.match(r"^\s*(?:-|\d+\.)\s+\S", line))
    if count < 3:
        report.error(rel, f"nur {count} Primärquellen (mindestens 3)")


def build_roster(root: Path) -> str:
    rows = []
    for card in sorted((root / "directors").glob("*.md")):
        front, _ = parse_frontmatter(card.read_text(encoding="utf-8"))
        if not front:
            continue
        dossier = root / "dossiers" / card.name
        cells = [
            card.name.split("-", 1)[0],
            front.get("slot", ""),
            front.get("name", ""),
            front.get("typ", ""),
            front.get("vorbild", ""),
            ", ".join(as_list(front.get("boards"))),
            ", ".join(as_list(front.get("keywords"))[:5]),
            ", ".join(as_list(front.get("reibung"))),
            f"directors/{card.name}",
            f"dossiers/{card.name}" if dossier.exists() else "",
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return ROSTER_HEADER + "\n".join(rows) + "\n"


def run_check(root: Path, strict: bool, only: set[str] | None) -> Report:
    report = Report()
    cards = sorted((root / "directors").glob("*.md"))
    if not cards:
        report.error("directors/", "keine Persona-Dateien gefunden")
    slots: dict[str, str] = {}
    strict_fronts: dict[str, dict] = {}
    for card in cards:
        rel = card.relative_to(root).as_posix()
        text = card.read_text(encoding="utf-8")
        preview, _ = parse_frontmatter(text)
        in_scope = strict and (not only or (preview or {}).get("slot") in only)
        front = check_card(rel, text, in_scope, report)
        if not front:
            continue
        slot = front.get("slot")
        if slot and slot in slots:
            report.error(rel, f"Slot „{slot}“ doppelt (auch in {slots[slot]})")
        elif slot:
            slots[slot] = rel
        if in_scope:
            strict_fronts[rel] = front
        dossier = root / "dossiers" / card.name
        if dossier.exists():
            check_dossier(dossier.relative_to(root).as_posix(), dossier.read_text(encoding="utf-8"), report)
        elif in_scope:
            report.error(rel, f"Dossier dossiers/{card.name} fehlt")
    for rel, front in strict_fronts.items():
        for other in as_list(front.get("reibung")):
            if other not in slots:
                report.error(rel, f"Reibung verweist auf unbekannten Slot „{other}“")
    if strict and not only:
        roster = root / "roster.md"
        if not roster.exists():
            report.error("roster.md", "fehlt (python3 tools/council_tool.py roster)")
        elif roster.read_text(encoding="utf-8") != build_roster(root):
            report.error("roster.md", "veraltet (python3 tools/council_tool.py roster)")
    for markdown in sorted(root.rglob("*.md")):
        parts = markdown.relative_to(root).parts
        if "testdaten" in parts or ".git" in parts or parts == ("CLAUDE.md",):
            continue
        check_text_rules(markdown.relative_to(root).as_posix(), markdown.read_text(encoding="utf-8"), report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Werkzeug für den Council-Skill")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Personas, Dossiers, Verzeichnis und Schreibregeln prüfen")
    check.add_argument("--streng", action="store_true", help="neues Format verlangen (Release-Prüfung)")
    check.add_argument("--nur", nargs="+", metavar="SLOT", help="strenge Prüfung nur für diese Slots")
    check.add_argument("--pfad", help="Skill-Ordner (Standard: Ordner über tools/)")
    roster = sub.add_parser("roster", help="roster.md aus den Karten erzeugen")
    roster.add_argument("--pfad", help="Skill-Ordner (Standard: Ordner über tools/)")
    args = parser.parse_args(argv)
    root = Path(args.pfad).resolve() if args.pfad else Path(__file__).resolve().parent.parent
    if args.command == "roster":
        (root / "roster.md").write_text(build_roster(root), encoding="utf-8")
        print(f"roster.md geschrieben: {root / 'roster.md'}")
        return 0
    report = run_check(root, args.streng, set(args.nur) if args.nur else None)
    for line in report.warnings + report.errors:
        print(line)
    print(f"{len(report.errors)} Fehler, {len(report.warnings)} Warnungen")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
