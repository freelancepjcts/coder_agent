"""Shared helpers for the agent modules."""

import logging
import os
import re
import sys

from openai import OpenAI

# ---------------------------------------------------------------------------
# Logging setup — configure once here; all pipeline modules use get_logger()
# ---------------------------------------------------------------------------
def _configure_logging() -> None:
    """Set up the root 'pipeline' logger.

    - INFO  → high-level flow (which agent ran, attempt numbers, pass/fail)
    - DEBUG → verbose detail (char counts, keyword hits, model params)

    Call this once at process startup. Idempotent if called multiple times.
    """
    root = logging.getLogger("pipeline")
    if root.handlers:
        return  # already configured

    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)-30s %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(fmt)
    root.addHandler(handler)
    root.propagate = False  # don't double-log via the root logger


_configure_logging()


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the 'pipeline' namespace.

    Usage in each module:
        from utils import get_logger
        log = get_logger(__name__)
    """
    return logging.getLogger(f"pipeline.{name}")


# ---------------------------------------------------------------------------
# Environment / dotenv loading
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional; fall back to real env vars


def require_api_key() -> None:
    """Exit with a clear message if OPENAI_API_KEY is not set.

    Call this once at the start of each entry point (orchestrator.__main__
    and app.py) so users get a helpful error instead of a buried
    AuthenticationError mid-request.
    """
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit(
            "ERROR: OPENAI_API_KEY is not set.\n"
            "Either export it in your shell or add it to a .env file in the project root."
        )


# ---------------------------------------------------------------------------
# Shared OpenAI client — single source of truth, no more duplication
# ---------------------------------------------------------------------------
MODEL = "gpt-4o-mini"  # swap for whichever model your API key has access to

_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    """Lazily create the OpenAI client so importing this module never
    requires OPENAI_API_KEY to already be set — only calling it does."""
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


# ---------------------------------------------------------------------------
# Code-fence stripping — robustly extracts the fenced block
# ---------------------------------------------------------------------------
def strip_code_fences(text: str) -> str:
    """Extract code from inside ```...``` fences if the model adds them.

    Searches for the *first* fenced block anywhere in the text (handles
    the case where the model adds explanation before the fence). Falls
    back to returning the whole text if no fence is found.
    """
    text = text.strip()
    match = re.search(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text
