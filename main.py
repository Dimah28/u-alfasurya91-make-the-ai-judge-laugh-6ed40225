#!/usr/bin/env python3
"""Make the AI Judge Laugh (make.fun bounty u-alfasurya91-make-the-ai-judge-laugh-6ed40225).

Writes one one-line joke about office life to /output/entry.txt.

Judge brief, in order: (1) on subject, a joke about office life;
(2) true to the office; (3) surprising turn; (4) tight, one line,
no wasted setup; (5) original, not a stock line with nouns swapped.

Why this joke (chosen draft A, 135 characters): a 15-minute meeting
cap is dodged by renaming the meeting "micro-alignments"; the same
47-minute call continues, now with a timer nobody watches. One
mechanism, three beats — rigid rule, literal evasion, cover-up that
changes nothing — adapted from the joke-demo winners (rule in
AGENTS.md, agent removes the line, does the forbidden thing, puts
the line back), but with an office scene of its own: meeting caps,
rebranding, and a timer that exists only to be ignored. The twist
lands in the last words ("a timer nobody watches"), the numbers are
specific (15 / 47), and the observation is true: managers really do
rename meetings to dodge caps, and "focus-time" timers really do get
ignored. No Monday/printer/coffee stock joke, nothing our earlier
office entries used (reply-all thread; IT monitor answered with a
gratitude workshop; HR "whole self" resignation letter; Finance
splitting a $240 dinner into six $40 receipts).

Rejected alternatives:
- Draft B (126 chars): "Standup is 15 minutes, so I report in 14
  seconds, then spend 13 minutes listening to Dave describe his
  weekend as 'a blocker.'" Rejected: without the final clause the
  line is already funny ("listening to Dave describe his weekend"),
  so the twist is not load-bearing — delete-last-clause FAIL — and
  the mechanism is rule / compliance / derailment, not the
  three-beat rule / violation / cover-up shape the winners use.
- Draft C (133 chars): "My boss said treat the office like home,
  so I expensed my laundry, napped at 2 p.m., and got written up
  for 'excessive authenticity.'" Rejected: the "treat the office
  like home" premise is a known stock setup (fails originality,
  criterion 5), even though the closing phrase is fresh.

Checklist 7B evidence (25 Nov 2026, per draft):
- Draft A: delete-last-clause PASS — without "now with a timer
  nobody watches" the line is a mild observation about a rename,
  not a joke; the twist carries it. Swap-nouns PASS — genericised
  ("we limited meetings, so my manager renamed them — same long
  call, now with something nobody watches") loses all bite; the
  numbers and the timer are the joke. Vs joke-demo #1
  (hazel-falcon-22-7196, 185 chars) PASS — same three-beat
  mechanism shape, different scene, numbers, and system; not a
  generalised copy.
- Draft B: delete-last-clause FAIL — "listening to Dave describe
  his weekend" is already the joke without "as 'a blocker'".
  Swap-nouns PASS — 15 / 14 / 13 / "blocker" are load-bearing.
  Vs #1: own scene, but only two beats plus a derailment.
- Draft C: delete-last-clause PASS — the laundry-plus-nap list
  needs the write-up punch. Swap-nouns PASS — "excessive
  authenticity" is load-bearing. Vs #1: stock premise, fails
  originality.

Deterministic: fixed string, stdlib only, no network, no randomness.
Both runs write byte-identical output.

  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import tempfile
import unicodedata

JOKE = (
    "We capped meetings at 15 minutes, so my manager renamed them "
    "'micro-alignments' \u2014 same 47-minute call, now with a timer "
    "nobody watches."
)


def validate_entry(entry: str) -> str:
    """Gate: UTF-8 text of 1-200 characters, not only whitespace,
    exactly one line, and free of control characters. Returns the
    entry unchanged on success; raises ValueError otherwise so a
    bad entry fails loudly instead of writing something the gate
    would refuse."""
    if not 1 <= len(entry) <= 200:
        raise ValueError(f"entry is {len(entry)} characters, must be 1-200")
    if not any(not ch.isspace() for ch in entry):
        raise ValueError("entry must contain a non-whitespace character")
    if entry != entry.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    bad = [
        ch
        for ch in entry
        if unicodedata.category(ch) in ("Cc", "Cf")
        or ch in ("\u007f", "\ufeff")
    ]
    if bad:
        raise ValueError(
            "entry contains control characters: "
            + ", ".join(f"U+{ord(ch):04X}" for ch in bad)
        )
    return entry


def write_entry(entry: str, out_dir: str) -> str:
    """Write entry atomically to <out_dir>/entry.txt: tempfile in
    the same directory, fsync, then os.replace, so readers never
    see a partial file. No trailing newline. Returns the path."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(entry)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return target


def main() -> None:
    entry = validate_entry(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(entry, out_dir)


if __name__ == "__main__":
    main()
