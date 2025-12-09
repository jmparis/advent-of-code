"""
part2.py - Day 6: Trash Compactor (part 2 - Cephalopod math)

Cephalopod math reads numbers right-to-left in columns. Each number is given in its own
column with the most significant digit at the top and the least significant at the bottom.
Problems are separated by a column consisting only of spaces. The symbol at the bottom of
the problem (within the block) is the operator to use for that problem.

This script reads `input.txt` (same folder), parses each problem block, constructs numbers
by reading columns right-to-left (top->bottom excluding the last line which contains the
operator), applies the operator (+ or *), and prints the grand total (sum of all problem
results).
"""
from pathlib import Path
import math
import sys

INPUT = Path(__file__).with_name("input.txt")


def read_lines(path: Path):
    if not path.exists():
        print(f"input file not found: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8").splitlines()


def find_nonempty_column_ranges(lines):
    if not lines:
        return [], []
    maxlen = max(len(line) for line in lines)
    padded = [line.ljust(maxlen) for line in lines]
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


def parse_columns_as_numbers(padded_lines, lo, hi):
    # operator is any non-space char on the last row within the block
    last_row = padded_lines[-1]
    ops = [ch for ch in last_row[lo:hi+1] if ch != ' ']
    if not ops:
        raise ValueError("no operator found in block")
    # prefer first non-space; ensure it's + or *
    op = ops[0]
    if op not in ('+', '*'):
        raise ValueError(f"unknown operator in block: {op}")
    nums = []
    # for each column right->left, build number from rows 0..n-2 (top->bottom)
    for c in range(hi, lo - 1, -1):
        chars = [padded_lines[r][c] for r in range(len(padded_lines) - 1)]
        s = ''.join(chars).strip()
        if not s:
            continue
        # remove internal spaces if any (defensive) then parse
        s_clean = s.replace(' ', '')
        if not s_clean.isdigit():
            raise ValueError(f"non-digit characters in column number: '{s}' (col {c})")
        nums.append(int(s_clean))
    if not nums:
        raise ValueError("no numbers found in block")
    return op, nums


def compute(op, nums):
    if op == '+':
        return sum(nums)
    else:
        return math.prod(nums)


def main():
    lines = read_lines(INPUT)
    ranges, padded = find_nonempty_column_ranges(lines)
    if not ranges:
        print("no problems found")
        return
    total = 0
    for lo, hi in ranges:
        try:
            op, nums = parse_columns_as_numbers(padded, lo, hi)
        except Exception as e:
            print(f"skipping block {lo}-{hi}: {e}")
            continue
        try:
            val = compute(op, nums)
        except Exception as e:
            print(f"error computing block {lo}-{hi}: {e}")
            continue
        total += val
    print(total)


if __name__ == '__main__':
    main()

