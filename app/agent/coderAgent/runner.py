"""
Test Runner / Validator.

Writes the generated code and tests to a temp directory and executes
them with pytest, capturing pass/fail plus the raw output so it can be
fed straight back into the Code Agent's retry loop.
"""

import os
import subprocess
import tempfile
from typing import Tuple

from utils import get_logger

log = get_logger("runner")


def run_tests(code: str, tests: str) -> Tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        code_path = os.path.join(tmp_dir, "generated_code.py")
        test_path = os.path.join(tmp_dir, "test_generated_code.py")

        with open(code_path, "w") as f:
            f.write(code)
        with open(test_path, "w") as f:
            f.write(tests)

        log.debug("Wrote code (%d chars) and tests (%d chars) to %s",
                  len(code), len(tests), tmp_dir)
        log.info("Running pytest (timeout=15s) ...")

        try:
            result = subprocess.run(
                ["pytest", test_path, "-q", "--tb=short"],
                cwd=tmp_dir,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except subprocess.TimeoutExpired:
            log.warning("pytest timed out after 15s — possible infinite loop in generated code")
            return False, (
                "Test run timed out after 15 seconds. "
                "The generated code may contain an infinite loop or blocking call. "
                "Fix any infinite loops or long-running operations."
            )

        passed = result.returncode == 0
        output = result.stdout + result.stderr

        if passed:
            log.info("pytest result: PASSED (returncode=0)")
        else:
            log.warning("pytest result: FAILED (returncode=%d)", result.returncode)
            log.debug("pytest output:\n%s", output.strip())

        return passed, output
