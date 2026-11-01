from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


class DemoOutputBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="demo-test-", dir=Path(__file__).resolve().parent)
        self.root = Path(self.temp.name)
        self.project = Path(__file__).resolve().parents[1]

    def tearDown(self):
        self.temp.cleanup()

    def run_demo(self, out):
        return subprocess.run([sys.executable, "-B", str(self.project / "demo.py"), "--out", str(out)],
                              cwd=self.root, capture_output=True, text=True, encoding="utf-8")

    def test_demo_writes_only_under_explicit_empty_output_and_preserves_rerun(self):
        out = self.root / "demo"
        result = self.run_demo(out)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"demo"}, {p.name for p in self.root.iterdir()})
        self.assertEqual({"pilot.sqlite", "RESULT.json", "READOUT.md"}, {p.name for p in out.iterdir()})
        data = json.loads((out / "RESULT.json").read_text(encoding="utf-8"))
        self.assertEqual(["q30", "q30"], data["shared_quote_ids"])
        self.assertEqual(0, data["metrics_after_apply_before_use"]["commercial_used"])
        self.assertEqual(1, data["metrics"]["diagnostic_hold_used"])
        before = {p.name: p.read_bytes() for p in out.iterdir()}
        retry = self.run_demo(out)
        self.assertNotEqual(0, retry.returncode)
        self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})

    def test_nonempty_output_sentinel_is_not_overwritten(self):
        out = self.root / "existing"
        out.mkdir()
        sentinel = out / "user-work.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        result = self.run_demo(out)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("preserve", sentinel.read_text(encoding="utf-8"))
        self.assertEqual([sentinel], list(out.iterdir()))
