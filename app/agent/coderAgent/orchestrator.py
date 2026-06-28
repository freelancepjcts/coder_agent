"""
Orchestrator (Integration Agent).

Runs Router -> Code Agent -> Test Agent -> Validator in sequence. If
the generated code fails its tests, the Code Agent gets another shot
armed with the actual error output, up to max_iterations times. Tests
themselves are never regenerated mid-loop - only the code is retried.
"""

import os
os.environ.setdefault("OPENAI_API_KEY", "dummy-key-will-replace-later")

from agents.router import detect_language
from agents.code_agent import generate_code, fix_code
from agents.test_agent import generate_tests
from runner import run_tests
from utils import get_logger

log = get_logger("orchestrator")


def run_pipeline(user_request: str, max_iterations: int = 3) -> dict:
    preview = user_request[:80].replace("\n", " ")
    log.info("▶ Pipeline started | max_iterations=%d | request: %r", max_iterations, preview)

    language = detect_language(user_request)
    log.info("🔀 Language detected: %s", language)

    log.info("✍  Generating code  [%s] ...", language)
    code = generate_code(user_request, language)
    log.debug("   Code generated (%d chars)", len(code))

    log.info("🧪 Generating tests [%s] ...", language)
    tests = generate_tests(code, language, request=user_request)
    log.debug("   Tests generated (%d chars)", len(tests))

    history = []
    for attempt in range(1, max_iterations + 1):
        log.info("🔁 Attempt %d/%d — running tests ...", attempt, max_iterations)
        try:
            passed, output = run_tests(code, tests)
        except Exception as exc:
            passed, output = False, f"Runner crashed: {exc}"
            log.error("   Runner raised an unexpected exception: %s", exc)

        history.append({"attempt": attempt, "passed": passed, "output": output})

        if passed:
            log.info("✅ Tests PASSED on attempt %d/%d", attempt, max_iterations)
            return {
                "status": "success",
                "language": language,
                "code": code,
                "tests": tests,
                "attempts": attempt,
                "history": history,
            }

        log.warning("❌ Tests FAILED on attempt %d/%d", attempt, max_iterations)
        log.debug("   Test output:\n%s", output.strip())

        if attempt < max_iterations:
            log.info("🔧 Requesting code fix (attempt %d → %d) ...", attempt, attempt + 1)
            code = fix_code(user_request, code, output, language)
            log.debug("   Fixed code (%d chars)", len(code))

    log.error(
        "🚫 Pipeline FAILED — could not pass tests after %d attempt(s)", max_iterations
    )
    return {
        "status": "failed",
        "language": language,
        "code": code,
        "tests": tests,
        "attempts": max_iterations,
        "history": history,
        "message": (
            f"Could not get all tests passing after {max_iterations} attempts. "
            "Showing the closest attempt and the last failure below."
        ),
    }


if __name__ == "__main__":
    from utils import require_api_key
    require_api_key()

    request = input("Describe the code you want: ")
    result = run_pipeline(request)

    print(f"\nLanguage: {result['language']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Status: {result['status']}\n")
    print("Generated code:\n" + result["code"])
    print("\nGenerated tests:\n" + result["tests"])

    if result["status"] == "failed":
        print("\n" + result["message"])
        print(result["history"][-1]["output"])
