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


class RosterTest(unittest.TestCase):
    def test_roster_matches_handwritten_expectation(self):
        tool = load_tool()
        expected = (DATA / "gut" / "roster.md").read_text(encoding="utf-8")
        self.assertEqual(tool.build_roster(DATA / "gut"), expected)


if __name__ == "__main__":
    unittest.main()
