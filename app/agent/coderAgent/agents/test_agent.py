"""
Test Generation Agent.

Writes pytest-style unit tests for a piece of generated code. Called
exactly once per request: the tests are the fixed target that the Code
Agent retries against, so they should not be regenerated mid-loop.

For SQL requests, "code" is the run_query(conn)-style Python module
described in code_agent.py, so the tests here open an in-memory sqlite3
connection and check structural properties of the result (row count,
limit respected, column shape) rather than exact values - there's no
ground-truth answer to compare against since the schema is invented.
"""

import sys
import os

# Ensure the project root is in sys.path so utils can always be found
# regardless of how this module is imported.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils import strip_code_fences, get_openai_client, MODEL, get_logger

log = get_logger("test_agent")

SYSTEM_PROMPTS = {
    "python": (
        "You are a meticulous test writer. Given a Python function, write 3 to 5 "
        "pytest unit tests covering normal cases and at least one edge case. "
        "Use plain assert statements. Return ONLY valid Python test code that "
        "imports the function(s) from a module named `generated_code`. "
        "No explanations, no markdown fences."
    ),
    "sql": (
        "You are a meticulous test writer for SQL-via-Python code. The module under test "
        "(import everything needed from `generated_code`) defines SCHEMA_SQL, SEED_SQL, "
        "QUERY_SQL, and a function run_query(conn). Write 2 to 4 pytest tests that: open an "
        "in-memory sqlite3 connection with sqlite3.connect(':memory:'), call run_query(conn), "
        "and assert reasonable structural properties of the result - for example that it is a "
        "non-empty list, that any row limit implied by the original request is respected, and "
        "that each row has a sensible, consistent number of columns. Import sqlite3 yourself. "
        "Return ONLY valid Python test code. No explanations, no markdown fences."
    ),
}


def generate_tests(code: str, language: str = "python", request: str = "") -> str:
    """Generate pytest tests for the given code snippet."""
    log.info("Calling %s | model=%s | temperature=0.2 | code_len=%d chars",
             MODEL, language, len(code))
    user_message = (
        f"Original request:\n{request}\n\nCode under test:\n{code}" if request else code
    )
    response = get_openai_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[language]},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    result = strip_code_fences(response.choices[0].message.content)
    log.debug("Tests received: %d chars | finish_reason=%s",
              len(result), response.choices[0].finish_reason)
    return result
