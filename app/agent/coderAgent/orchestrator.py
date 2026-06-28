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
from utils import get_logger, get_openai_client, MODEL

log = get_logger("orchestrator")


def classify_request(user_request: str) -> str:
    """Classify the user request into 'code_task', 'casual', or 'out_of_scope'."""
    try:
        response = get_openai_client().chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a routing assistant. Classify the user input into exactly one of three categories:\n"
                        "- 'code_task': if the user wants code written, a function built, a database query generated, "
                        "bug fixing, DSA questions, system design, code explanation, code review, or general programming discussions.\n"
                        "- 'casual': if the user is greeting you (e.g., 'hi', 'hello', 'good morning'), asking how you are, making small talk, "
                        "or saying simple conversational things.\n"
                        "- 'out_of_scope': if the user request is unrelated to programming or software development (e.g., general knowledge, "
                        "current affairs, politics, health/medical advice, legal/financial advice, entertainment, relationship advice, creative writing, etc.).\n"
                        "Respond ONLY with one word: 'code_task', 'casual', or 'out_of_scope'."
                    )
                },
                {"role": "user", "content": user_request}
            ],
            temperature=0.0,
            max_tokens=10
        )
        category = response.choices[0].message.content.strip().lower()
        if "out_of_scope" in category:
            return "out_of_scope"
        elif "casual" in category:
            return "casual"
        else:
            return "code_task"
    except Exception as exc:
        log.error("Failed to classify request: %s. Defaulting to code_task.", exc)
        return "code_task"


def generate_casual_reply(user_request: str) -> str:
    try:
        response = get_openai_client().chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful coding assistant. Respond to the user's greeting or small talk "
                        "naturally, briefly, and friendly. Remind them you are ready to help with coding."
                    )
                },
                {"role": "user", "content": user_request}
            ],
            temperature=0.7,
            max_tokens=80
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return "Hello! How can I help you with programming today?"


def run_pipeline(user_request: str, max_iterations: int = 3) -> dict:
    preview = user_request[:80].replace("\n", " ")
    log.info("▶ Pipeline started | max_iterations=%d | request: %r", max_iterations, preview)

    category = classify_request(user_request)
    log.info("🔀 Category classified: %s", category)

    if category == "casual":
        log.info("💬 Casual conversation detected. Bypassing pipeline.")
        reply = generate_casual_reply(user_request)
        return {
            "status": "success",
            "language": "conversation",
            "code": "",
            "tests": "",
            "attempts": 0,
            "history": [],
            "message": reply,
        }
    elif category == "out_of_scope":
        log.info("🚫 Out-of-scope query detected. Bypassing pipeline.")
        reply = "I can only assist with programming and coding-related queries. What coding problem can I help you solve today?"
        return {
            "status": "success",
            "language": "conversation",
            "code": "",
            "tests": "",
            "attempts": 0,
            "history": [],
            "message": reply,
        }

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
