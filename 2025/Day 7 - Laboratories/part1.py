#!/usr/bin/env python3
from pathlib import Path
import sys

def read_grid(path: Path):
    raw = path.read_text(encoding="utf-8").splitlines()
    # keep non-empty lines (strip trailing/leading whitespace but preserve dots)
    lines = [ln.rstrip('\n') for ln in raw if ln.strip() != ""]
    if not lines:
        return []
    # normalize width
    width = max(len(ln) for ln in lines)
    grid = [list(ln.ljust(width, '.')) for ln in lines]
    return grid


def count_splits(grid):
    if not grid:
        return 0
    R = len(grid)
    C = len(grid[0])
    start_r = start_c = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start_r, start_c = r, c
                break
        if start_r is not None:
            break
    if start_r is None:
        raise ValueError("No start position 'S' found in input")

    beams = {start_c}
    splits = 0
    r = start_r
    # propagate until bottom or no active beams
    while beams and r < R - 1:
        nr = r + 1
        next_beams = set()
        received = set()
        for c in beams:
            if c < 0 or c >= C:
                continue
            ch = grid[nr][c]
            if ch == '^':
                received.add(c)
            else:
                # any non-splitter cell lets the beam pass
                next_beams.add(c)
        # splitters emit beams to immediate left and right on the same row (nr)
        for c in received:
            if c - 1 >= 0:
                next_beams.add(c - 1)
            if c + 1 < C:
                next_beams.add(c + 1)
        splits += len(received)
        beams = next_beams
        r = nr
    return splits


def main():
    p = Path(__file__).parent / 'input.txt'
    if not p.exists():
        print("input.txt not found next to part1.py", file=sys.stderr)
        sys.exit(1)
    grid = read_grid(p)
    try:
        result = count_splits(grid)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(result)

if __name__ == '__main__':
    main()

