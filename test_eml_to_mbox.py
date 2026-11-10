#!/usr/bin/env python3
"""Tests for eml_to_mbox.py (stdlib unittest only, no extra dependencies)."""

import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "eml_to_mbox.py"
)

VALID_EML = (
    "From: alice@example.com\r\n"
    "To: bob@example.com\r\n"
    "Subject: hello\r\n"
    "Date: Mon, 10 Nov 2026 10:00:00 +0000\r\n"
    "Message-ID: <abc123@example.com>\r\n"
    "\r\n"
    "Hi Bob.\r\n"
)


def run_cli(folder, mbox):
    return subprocess.run(
        [sys.executable, SCRIPT, folder, mbox],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


class TestExitCode(unittest.TestCase):
    def test_all_failed_exits_nonzero_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "empty.eml"), "wb"):
                pass
            proc = run_cli(tmp, os.path.join(tmp, "out.mbox"))
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("Conversion failed!", proc.stdout)
            self.assertNotIn("Traceback", proc.stdout)

    def test_successful_conversion_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(
                os.path.join(tmp, "a.eml"), "w", encoding="utf-8"
            ) as handle:
                handle.write(VALID_EML)
            out_mbox = os.path.join(tmp, "out.mbox")
            proc = run_cli(tmp, out_mbox)
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertIn("Conversion complete! 1 email(s)", proc.stdout)
            with open(out_mbox, "rb") as handle:
                content = handle.read()
            self.assertIn(b"Hi Bob.", content)


if __name__ == "__main__":
    unittest.main()
