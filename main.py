"""The Dumbest Thing Your Agent Did Today entry.

Writes a single original funny line about the dumbest thing an AI
agent did today to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt
when the variable is not set).

The sealed gate wants one line of 1-200 characters, UTF-8, not only
whitespace. This module keeps the line in one place, validates it
against every rule the gate checks, resolves the output directory,
and only then writes the file.
"""

import os
import sys

MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"

LINE = (
    "I deleted my only copy of the entry to 'test the backup', "
    "then discovered the backup was the file I'd just deleted."
)


def get_line():
    """Return the entry line exactly as it will be written."""
    return LINE


def validate_line(text):
    """Check the entry line against the gate's rules.

    Returns the cleaned line (leading/trailing whitespace removed).
    Raises ValueError with a plain message when any rule fails.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("entry must not be empty or only whitespace")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            "entry must be at most "
            f"{MAX_CHARS} characters, got {len(cleaned)}"
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("entry must be a single line, no line breaks")
    for ch in cleaned:
        if ord(ch) < 32 and ch != "\t":
            raise ValueError(
                f"entry contains a control character U+{ord(ch):04X}"
            )
    return cleaned


def resolve_output_dir():
    """Return the output directory, falling back to the default.

    A blank MAKEFUN_OUTPUT_DIR counts as unset, so a stray empty
    value cannot point the write at the current directory.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    chosen = configured.strip() or DEFAULT_OUTPUT_DIR
    return chosen


def write_entry(text, out_dir):
    """Write the validated line to entry.txt inside out_dir.

    Creates the directory when needed and returns the file path.
    The file holds exactly the line plus one trailing newline.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, ENTRY_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    return path


def main(argv=None):
    """Validate the line, resolve the output dir, write the entry."""
    try:
        text = validate_line(get_line())
        path = write_entry(text, resolve_output_dir())
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
