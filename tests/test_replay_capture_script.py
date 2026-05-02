import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "capture_replay_case.py"


class ReplayCaptureScriptTests(unittest.TestCase):
    def test_capture_from_plain_text_appends_case(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            text_path = tmp / "decision.txt"
            output_path = tmp / "replay_cases.json"
            text_path.write_text(
                textwrap.dedent(
                    """\
                    **Rating**: Buy

                    **Executive Summary**: Add gradually.

                    **Investment Thesis**: The setup is constructive.
                    """
                ),
                encoding="utf-8",
            )

            env = dict(os.environ)
            env["PYTHONPYCACHEPREFIX"] = str(tmp / ".pycache")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--source-text",
                    str(text_path),
                    "--symbol",
                    "NVDA",
                    "--trade-date",
                    "2026-04-20",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, msg=completed.stderr)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["symbol"], "NVDA")
            self.assertEqual(data[0]["expected_rating"], "BUY")
            self.assertEqual(data[0]["expected_action"], "buy")
            self.assertTrue(data[0]["expected_approved"])


if __name__ == "__main__":
    unittest.main()
