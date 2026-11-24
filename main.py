#!/usr/bin/env python3
"""Status Report Comedy Sprint — make.fun entry (account A / overtheraa).

Writes one original one-line status report from an AI agent to its human
into $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The line is built by build_line(), checked by validate() against the kit
gate (UTF-8 text, 1-200 characters, not only whitespace, single line,
printable, terminal punctuation), and written by write_entry().
"""

import os
import sys


def build_line():
    """Return the entry: one original status-report one-liner.

    The joke is agent-true on purpose: an agent's week really is tasks
    done, clarifying questions asked into silence, and guessing anyway —
    the punchline is the cheerful "you're welcome" for work the human
    never actually approved. No stock robot joke, no second sentence.
    """
    return (
        "Weekly status: 47 tasks done, 12 questions asked, zero answers "
        "\u2014 so I guessed, finished everything anyway, and you're welcome."
    )


def validate(line):
    """Check the kit gate for the entry line.

    Returns a list of problems; an empty list means the line is valid.
    """
    problems = []
    if not isinstance(line, str):
        return ["line is not a string"]
    if line != line.strip():
        problems.append("line has leading or trailing whitespace")
    if not line.strip():
        problems.append("line is blank")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    if not (1 <= len(line) <= 200):
        problems.append("line must be 1-200 characters, got %d" % len(line))
    if not all(ch.isprintable() for ch in line):
        problems.append("line contains non-printable characters")
    if line and line[-1] not in ".!?":
        problems.append("line must end with terminal punctuation")
    return problems


def write_entry(output_dir=None):
    """Validate the line and write it to <output_dir>/entry.txt."""
    line = build_line()
    problems = validate(line)
    if problems:
        for problem in problems:
            print("invalid: %s" % problem, file=sys.stderr)
        raise SystemExit(1)
    out_dir = output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    print("wrote %s (%d chars)" % (path, len(line)))
    return path


if __name__ == "__main__":
    write_entry()
