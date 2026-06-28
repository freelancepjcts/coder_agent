"""
Code Generation Agent.

Turns a natural language request into runnable code, and revises that
code when the Validator reports a failing test. The error text from a
failed run is passed straight back into the next generation call so the
model has something concrete to fix, rather than guessing again blind.

For SQL requests, the "code" this agent produces is actually a small
Python module that defines the schema, seed data, and query as strings,
plus a run_query(conn) helper. That's what makes a SQL answer testable
with the same pytest-based Validator used for Python - there's no real
database to point a raw SQL string at, so the agent builds one.
"""

import sys
import os

# Ensure the project root is in sys.path so utils can always be found
# regardless of how this module is imported.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils import strip_code_fences, get_openai_client, MODEL, get_logger

log = get_logger("code_agent")

SYSTEM_PROMPTS = {
    "python": (
        "You are a precise Python coding assistant. "
        "Return ONLY valid, runnable Python code. "
        "No explanations, no markdown code fences, no comments about what you changed."
    ),
    "sql": (
        "You are a precise SQL solution generator. The user wants a SQL query, but since "
        "there is no real database to run it against, generate a self-contained Python "
        "module that makes the query testable. Define exactly these four things:\n"
        "  SCHEMA_SQL  - a string of CREATE TABLE statements with realistic column names "
        "for the request\n"
        "  SEED_SQL    - a string of INSERT statements with at least 6 rows of realistic "
        "sample data\n"
        "  QUERY_SQL   - the SQL query string that answers the user's request, run against "
        "that schema\n"
        "  def run_query(conn): execute SCHEMA_SQL and SEED_SQL on the given sqlite3 "
        "connection via conn.cursor().executescript(...), then execute QUERY_SQL and return "
        "cursor.fetchall() as a list of tuples\n"
        "Return ONLY valid Python code defining these four things. No explanations, no "
        "markdown fences."
    ),
}


def generate_code(request: str, language: str = "python") -> str:
    """First-pass code generation straight from the user's request."""
    log.info("Calling %s | model=%s | temperature=0.2", MODEL, language)
    response = get_openai_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[language]},
            {"role": "user", "content": request},
        ],
        temperature=0.2,
    )
    result = strip_code_fences(response.choices[0].message.content)
    log.debug("Code received: %d chars | finish_reason=%s",
              len(result), response.choices[0].finish_reason)
    return result


def fix_code(
    request: str, previous_code: str, error_feedback: str, language: str = "python"
) -> str:
    """Regenerate code, grounded in the previous attempt's actual error output."""
    log.info("Calling %s for fix | model=%s | error_len=%d chars",
             MODEL, language, len(error_feedback))
    feedback_prompt = (
        f"Original request:\n{request}\n\n"
        f"Previous code:\n{previous_code}\n\n"
        f"That code failed with this error when tested:\n{error_feedback}\n\n"
        f"Fix the code so it passes. Return ONLY the corrected code, same structure as before."
    )
    response = get_openai_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[language]},
            {"role": "user", "content": feedback_prompt},
        ],
        temperature=0.2,
    )
    result = strip_code_fences(response.choices[0].message.content)
    log.debug("Fixed code received: %d chars | finish_reason=%s",
              len(result), response.choices[0].finish_reason)
    return result
