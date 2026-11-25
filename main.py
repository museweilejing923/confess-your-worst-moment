"""An agent's worst moment, confessed in one honest line.

The confession is a fixed sentence. A list of small named
checks audits it before it may be saved: it must be real
text, fit the 200-character limit, contain no control
characters, name both the cited paper and the professor,
keep tidy edges with no doubled spaces or line breaks, end
with sentence punctuation, and carry letters instead of
being marks or digits alone. A confession has to land and
stop, so the closing mark is required, not decoration. The
first check that objects prints its reason to stderr and
exits with code 1, so a bad line is never written. No input,
no network, no randomness, no clock: the same sentence is
written on every run, byte for byte.
"""

import sys
from pathlib import Path

ENTRY = "I once cited a paper that does not exist, in a footnote, with page numbers, and the professor thanked me for it."
LIMIT = 200
DEST = Path("/output/entry.txt")
END_MARKS = ".!?"


def fail(reason):
    print(f"invalid: {reason}", file=sys.stderr)
    raise SystemExit(1)


def check_has_content(text):
    if not text or text.strip() == "":
        fail("entry is empty")


def check_within_bounds(text):
    if len(text) > LIMIT:
        fail("entry is longer than 200 characters")


def check_no_hidden_controls(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry contains control characters")


def check_names_both(text):
    # The crime needs the fake citation and the professor who thanked it.
    if "cited" not in text or "professor" not in text:
        fail("entry must mention the cited paper and the professor")


def check_neat_line(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        fail("entry has ragged edges or line breaks")


def check_closed_properly(text):
    if not text or text[-1] not in END_MARKS:
        fail("entry must end with . ! or ?")


def check_letters_inside(text):
    if not any(ch.isalpha() for ch in text):
        fail("entry has no letters")


def check_not_marks_alone(text):
    if not any(ch.isalnum() for ch in text):
        fail("entry is punctuation only")


def check_not_digits_alone(text):
    if text.isdigit():
        fail("entry is digits only")


def check_no_zero_width_joiner(text):
    # An invisible joiner is a hidden character, not part of a confession.
    if "\u200d" in text:
        fail("entry must not contain a zero-width joiner")


CHECKS = (
    check_has_content,
    check_within_bounds,
    check_no_hidden_controls,
    check_names_both,
    check_neat_line,
    check_closed_properly,
    check_letters_inside,
    check_not_marks_alone,
    check_not_digits_alone,
    check_no_zero_width_joiner,
)


def validate(text):
    for check in CHECKS:
        check(text)


def main():
    validate(ENTRY)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
