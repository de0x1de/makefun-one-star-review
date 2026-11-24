#!/usr/bin/env python3
"""Write the one-line entry for the One-Star Review bounty.

The entry is a single deadpan one-star review of oxygen, an everyday
essential nobody can opt out of. It is assembled here from three
sentence fragments so the line is built by the program rather than
copied in as one finished literal. The finished line is validated
before it is written, and the file is read back and compared byte
for byte.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# The review, split into its three natural fragments: the subject and
# the lifelong habit, the dependency twist, and the closing complaint.
PARTS = (
    "Oxygen: been breathing it my whole life ",
    "and now I'm dependent. ",
    "No warning label, no refund.",
)

MIN_CHARS = 1
MAX_CHARS = 160


def build_line() -> str:
    """Assemble the entry line from its fragments."""
    line = "".join(PARTS)
    if not line:
        raise ValueError("assembled line is empty")
    return line


def validate(line: str) -> bytes:
    """Check the line against the gate and return its UTF-8 bytes."""
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        raise ValueError(f"line length {len(line)} outside {MIN_CHARS}-{MAX_CHARS}")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if line != line.strip():
        raise ValueError("entry must not carry surrounding whitespace")
    if not line.isascii():
        raise ValueError("entry must be plain ASCII")
    if not line.startswith("Oxygen:"):
        raise ValueError("review must open by naming the essential it reviews")
    if not line.endswith("."):
        raise ValueError("review must close with a full stop")
    if line.count(". ") != 1 or "  " in line:
        raise ValueError("review must be two clean sentences with single spaces")
    encoded = line.encode("utf-8")
    if encoded.decode("utf-8") != line:
        raise ValueError("line does not survive a UTF-8 round trip")
    return encoded


def main() -> None:
    line = build_line()
    encoded = validate(line)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(encoded)
    read_back = OUTPUT_PATH.read_bytes()
    if read_back != encoded:
        raise SystemExit(f"read-back mismatch: {read_back!r} != {encoded!r}")
    print(f"wrote {len(encoded)} bytes to {OUTPUT_PATH}: {line}")


if __name__ == "__main__":
    main()
