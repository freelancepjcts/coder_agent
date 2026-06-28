"""
Router Agent.

Decides whether a request wants Python or SQL code, based on keywords.
Kept deliberately simple per the hackathon brief - this step doesn't
need an LLM call to do its job well.

False-positive prevention: a single generic keyword like "join", "select",
or "table" is common in plain Python requests ("join two lists", "select
the largest element", "lookup table"). We require at least two SQL keywords
to co-occur before routing to SQL, and we check for Python override signals
that should always win.
"""

from utils import get_logger

log = get_logger("router")

SQL_KEYWORDS = [
    "sql", "query", "select", "database", "table", "join",
    "insert", "update", "delete", "where", "from",
]

# If any of these appear, it's almost certainly a Python request regardless
# of SQL keyword matches.
PYTHON_OVERRIDE_PHRASES = [
    "in python", "python function", "python script", "python class",
]


def detect_language(request: str) -> str:
    """Return 'sql' if the request looks database-flavored, else 'python'.

    Requires at least 2 SQL keywords to co-occur to avoid false-positives
    from everyday words like 'join', 'select', or 'table'.
    """
    lowered = request.lower()

    # Explicit Python signals always win
    for phrase in PYTHON_OVERRIDE_PHRASES:
        if phrase in lowered:
            log.debug("Python override phrase matched: %r → routing to python", phrase)
            return "python"

    matched = [kw for kw in SQL_KEYWORDS if kw in lowered]
    sql_hits = len(matched)
    log.debug("SQL keyword hits: %d %s", sql_hits, matched)

    language = "sql" if sql_hits >= 2 else "python"
    log.debug("Routing decision: %s (threshold=2, hits=%d)", language, sql_hits)
    return language
