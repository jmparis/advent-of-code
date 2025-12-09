#!/usr/bin/env python3
from pathlib import Path
import sys
from collections import defaultdict


def read_grid(path: Path):
    raw = path.read_text(encoding="utf-8").splitlines()
    lines = [ln.rstrip('\n') for ln in raw if ln.strip() != ""]
    if not lines:
        return []
    width = max(len(ln) for ln in lines)
    grid = [list(ln.ljust(width, '.')) for ln in lines]
    return grid


def count_timelines(grid):
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

    # beams: mapping column -> number of timelines currently at that column on current row
    beams = defaultdict(int)
    beams[start_c] = 1
    r = start_r
    # propagate until bottom or no active beams
    while beams and r < R - 1:
        nr = r + 1
        next_beams = defaultdict(int)
        received = defaultdict(int)  # splitter column -> total number of beams hitting it this step
        for c, cnt in list(beams.items()):
            if c < 0 or c >= C:
                continue
            ch = grid[nr][c]
            if ch == '^':
                received[c] += cnt
            else:
                next_beams[c] += cnt
        # each beam hitting a splitter spawns one left and one right beam
        for c, cnt in received.items():
            if c - 1 >= 0:
                next_beams[c - 1] += cnt
            if c + 1 < C:
                next_beams[c + 1] += cnt
        beams = next_beams
        r = nr
    # total number of timelines is sum of counts of beams remaining
    total = sum(beams.values())
    return total


def main():
    p = Path(__file__).parent / 'input.txt'
    if not p.exists():
        print("input.txt not found next to part2.py", file=sys.stderr)
        sys.exit(1)
    grid = read_grid(p)
    try:
        result = count_timelines(grid)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(result)

if __name__ == '__main__':
    main()

