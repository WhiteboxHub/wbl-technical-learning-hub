"""Automated verification tests for python-course Day 1 & Day 2 demos and exercises."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def run_script(rel_path: str, stdin_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / rel_path)],
        input=stdin_text,
        text=True,
        capture_output=True,
        cwd=str(ROOT),
        check=True,
    )


class TestDay1Demos(unittest.TestCase):
    def test_beat_1_1_variables(self):
        res = run_script("demos/day1/beat_1_1_variables.py")
        self.assertIn("gpt-4o-mini", res.stdout)
        self.assertIn("gemini-2.5-flash", res.stdout)

    def test_beat_1_2_data_types(self):
        res = run_script("demos/day1/beat_1_2_data_types.py")
        for expected in ("<class 'str'>", "<class 'int'>", "<class 'float'>", "<class 'bool'>", "<class 'NoneType'>"):
            self.assertIn(expected, res.stdout)

    def test_beat_1_3_input_casting(self):
        res = run_script("demos/day1/beat_1_3_input_casting.py", stdin_text="Summarize AI\n200\n0.4\n")
        self.assertIn("'200200'", res.stdout)
        self.assertIn("400 (<class 'int'>)", res.stdout)
        self.assertIn("0.4 (<class 'float'>)", res.stdout)

    def test_beat_1_4_loops(self):
        res = run_script("demos/day1/beat_1_4_loops.py")
        self.assertIn("[skipped empty response]", res.stdout)
        self.assertIn("Model ready! Stopping retries.", res.stdout)

    def test_beat_1_5_revision(self):
        res = run_script("demos/day1/beat_1_5_revision.py", stdin_text="Translate text\n2\n")
        self.assertIn("Run 2/2", res.stdout)
        self.assertIn("Total tokens used: 240", res.stdout)

    def test_day1_exercise_runs(self):
        res = run_script("exercises/day1_exercise.py")
        self.assertIn("Final tokens used: 370", res.stdout)


class TestDay2Demos(unittest.TestCase):
    def tearDown(self):
        for name in ("run_log.txt", "updated_config.json"):
            p = ROOT / "demos" / "day2" / "data" / name
            if p.exists():
                p.unlink()

    def test_beat_2_1_functions(self):
        res = run_script("demos/day2/beat_2_1_functions.py")
        self.assertIn("print_only_cost returned : None", res.stdout)
        self.assertIn("Two API calls total ($)  : 0.006", res.stdout)

    def test_beat_2_2_containers(self):
        res = run_script("demos/day2/beat_2_2_containers.py")
        self.assertIn("(count = 2)", res.stdout)
        self.assertIn("'model': 'gpt-4o-mini'", res.stdout)

    def test_beat_2_3_comprehensions_bigo(self):
        res = run_script("demos/day2/beat_2_3_comprehensions_bigo.py")
        self.assertIn("['summarize ai', 'explain big-o']", res.stdout)
        self.assertIn("hits=1000/1000", res.stdout)

    def test_beat_2_4_file_io(self):
        res = run_script("demos/day2/beat_2_4_file_io.py")
        self.assertIn("Loaded document lines: 3", res.stdout)
        log_path = ROOT / "demos" / "day2" / "data" / "run_log.txt"
        cfg_path = ROOT / "demos" / "day2" / "data" / "updated_config.json"
        self.assertTrue(log_path.exists())
        self.assertTrue(cfg_path.exists())
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        self.assertEqual(data["last_doc_count"], 3)

    def test_day2_exercise_runs(self):
        res = run_script("exercises/day2_exercise.py")
        self.assertIn("'unique_count': 2", res.stdout)


if __name__ == "__main__":
    unittest.main()
