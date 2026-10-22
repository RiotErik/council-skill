"""Tests für tools/council_tool.py. Aufruf: python3 -m unittest discover -s tools -p 'test_*.py'"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
TOOL = TOOLS / "council_tool.py"
DATA = TOOLS / "testdaten"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


def load_tool():
    spec = importlib.util.spec_from_file_location("council_tool", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckTest(unittest.TestCase):
    def test_good_data_passes_strict(self):
        result = run("check", "--streng", "--pfad", str(DATA / "gut"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bad_data_fails_with_expected_messages(self):
        result = run("check", "--streng", "--pfad", str(DATA / "schlecht"))
        self.assertEqual(result.returncode, 1, result.stdout)
        for expected in [
            "Geviertstrich gefunden",
            "typ „roboter“ ungültig",
            "Satzbau „nicht …, sondern …“",
            "Umlaut-Umschrift",
            "Dossier dossiers/01-kaputt.md fehlt",
            "Abschnitt „## Blinde Flecken“ fehlt",
            "roster.md",
        ]:
            self.assertIn(expected, result.stdout)

    def test_format20_passes_without_strict(self):
        result = run("check", "--pfad", str(DATA / "format20"))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_format20_fails_strict(self):
        result = run("check", "--streng", "--pfad", str(DATA / "format20"))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Feld „boards“ fehlt", result.stdout)

    def test_only_limits_strict_checks(self):
        limited = run("check", "--streng", "--nur", "alpha", "--pfad", str(DATA / "gemischt"))
        self.assertEqual(limited.returncode, 0, limited.stdout)
        full = run("check", "--streng", "--pfad", str(DATA / "gemischt"))
        self.assertEqual(full.returncode, 1, full.stdout)
        self.assertIn("directors/03-alte-form.md: Abschnitt „## Kurzporträt“ fehlt", full.stdout)


    def test_only_with_unknown_slot_fails(self):
        result = run("check", "--streng", "--nur", "alpah", "--pfad", str(DATA / "gut"))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Slot „alpah“ aus --nur gehört zu keiner Karte", result.stdout)


class FrontmatterTest(unittest.TestCase):
    def test_quoted_values_are_unquoted(self):
        tool = load_tool()
        front, _ = tool.parse_frontmatter('---\nslot: "alpha"\nname: \'Die Testerin\'\n---\n')
        self.assertEqual(front["slot"], "alpha")
        self.assertEqual(front["name"], "Die Testerin")


class TextRulesTest(unittest.TestCase):
    def rule_errors(self, text: str) -> list[str]:
        tool = load_tool()
        report = tool.Report()
        tool.check_text_rules("probe.md", text, report)
        return report.errors

    def test_urls_are_not_flagged_as_umlaut_transliteration(self):
        text = "Mehr dazu unter https://example.de/ueber-mich/ und <https://example.de/fuehrung-fuer-alle>."
        self.assertEqual(self.rule_errors(text), [])

    def test_sources_and_quotes_sections_keep_original_wording(self):
        text = (
            "## Quellen\n"
            "### Primärquellen\n"
            "1. Carl Ueberreuter Verlag, Testbuch (1999)\n"
            "## Zitate mit Fundstelle\n"
            "- „Nicht weil es schwer ist, wagen wir es nicht, sondern weil wir es nicht wagen.“ (Seneca, Ep. 104)\n"
        )
        self.assertEqual(self.rule_errors(text), [])

    def test_rules_still_apply_after_sources_section(self):
        text = "## Quellen\n1. Buch (2001)\n## Abgrenzung\n- Das ist nicht schnell, sondern gründlich.\n"
        self.assertEqual(len(self.rule_errors(text)), 1)

    def test_em_dash_is_flagged_in_quotes_too(self):
        dash = "\u2014"
        text = f"## Zitate\n- „Erst denken {dash} dann handeln.“ (Test, 2001)\n"
        self.assertEqual(len(self.rule_errors(text)), 1)


class SourceHygieneTest(unittest.TestCase):
    def test_tool_sources_have_no_em_dash(self):
        for source in TOOLS.glob("*.py"):
            self.assertNotIn("\u2014", source.read_text(encoding="utf-8"), source.name)


class RosterTest(unittest.TestCase):
    def test_roster_matches_handwritten_expectation(self):
        tool = load_tool()
        expected = (DATA / "gut" / "roster.md").read_text(encoding="utf-8")
        self.assertEqual(tool.build_roster(DATA / "gut"), expected)


if __name__ == "__main__":
    unittest.main()
