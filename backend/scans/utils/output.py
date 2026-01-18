import re

ANSI_ESCAPE_RE = re.compile(
    r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by control codes
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
    """,
    re.VERBOSE,
)


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from tool output.
    """
    return ANSI_ESCAPE_RE.sub("", text)
