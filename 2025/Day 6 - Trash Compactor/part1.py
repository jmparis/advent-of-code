"""
part1.py - Day 6: Trash Compactor (part 1)

Lecture de `input.txt` (même dossier), sépare les problèmes par colonnes entièrement vides,
extrait les nombres (toutes les lignes sauf la dernière) et l'opérateur (dernière ligne)
pour chaque problème, calcule le résultat (+ ou *) puis affiche la somme totale.
"""
from pathlib import Path
import math
import sys

INPUT = Path(__file__).with_name("input.txt")


def read_lines(path: Path):
    if not path.exists():
        print(f"input file not found: {path}")
        sys.exit(1)
    # keep trailing spaces per line (splitlines preserves spaces)
    return path.read_text(encoding="utf-8").splitlines()


def find_nonempty_column_ranges(lines):
    if not lines:
        return []
    maxlen = max(len(line) for line in lines)
    padded = [line.ljust(maxlen) for line in lines]
    # a column is a separator if every line has a space at that column
    is_separator = [all(row[col] == ' ' for row in padded) for col in range(maxlen)]
    ranges = []
    in_range = False
    start = 0
    for i, sep in enumerate(is_separator):
        if not sep and not in_range:
            in_range = True
            start = i
        elif sep and in_range:
            in_range = False
            ranges.append((start, i - 1))
    if in_range:
        ranges.append((start, maxlen - 1))
    return ranges, padded


def parse_block(padded_lines, lo, hi):
    tokens = []
    for row in padded_lines:
        s = row[lo:hi+1].strip()
        if s:
            tokens.append(s)
    return tokens


def compute_from_tokens(tokens):
    if not tokens:
        raise ValueError("empty block")
    op = tokens[-1].strip()
    nums = tokens[:-1]
    if not nums:
        raise ValueError(f"no numbers in block for operator {op}")
    try:
        values = [int(x) for x in nums]
    except ValueError as e:
        raise ValueError(f"failed to parse integer in tokens {nums}") from e
    if op == '+':
        return sum(values)
    elif op == '*':
        return math.prod(values)
    else:
        raise ValueError(f"unknown operator: {op}")


def main():
    lines = read_lines(INPUT)
    ranges, padded = find_nonempty_column_ranges(lines)
    if not ranges:
        print("no problems found")
        return
    total = 0
    for lo, hi in ranges:
        tokens = parse_block(padded, lo, hi)
        # ignore any trailing meta lines that might not be numbers/operators
        if not tokens:
            continue
        try:
            val = compute_from_tokens(tokens)
        except Exception as e:
            print(f"skipping block {lo}-{hi}: {e}")
            continue
        total += val
    print(total)


if __name__ == '__main__':
    main()

