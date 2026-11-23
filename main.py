"""The Dumbest Thing Your Agent Did Today entry.

Writes a single original funny line about the dumbest thing an AI
agent did today to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt
when the variable is not set). The line is 1-199 characters (the
sealed gate's range), UTF-8, not only whitespace.
"""

import os

LINE = (
    "I deleted my only copy of the entry to 'test the backup', "
    "then discovered the backup was the file I'd just deleted."
)


def main():
    text = LINE.strip()
    if not 1 <= len(text) <= 199:
        raise ValueError(
            f"entry must be 1-199 characters, got {len(text)}"
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
