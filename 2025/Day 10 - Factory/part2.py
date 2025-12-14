#!/usr/bin/env python3

"""Advent of Code 2025 - Day 10: Factory (Part 2).

Determine the minimum number of button presses required to satisfy each
machine's joltage counters. Each button press increments a fixed subset of
counters by exactly one. The task reduces to solving a system of linear
equations with non-negative integer variables while minimising the L1 norm of
those variables.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

BUTTON_RE = re.compile(r"\(([^)]*)\)")
TARGET_RE = re.compile(r"\{([^}]*)\}")


def parse_machine_line(line: str) -> Tuple[List[int], List[List[int]]]:
    """Extract target counters and button definitions from an input line."""

    target_match = TARGET_RE.search(line)
    if not target_match:
        raise ValueError(f"Missing target definition: {line}")

    target_values = [
        int(value.strip())
        for value in target_match.group(1).split(",")
        if value.strip()
    ]

    buttons: List[List[int]] = []
    for group in BUTTON_RE.findall(line):
        indices = [
            int(value.strip())
            for value in group.split(",")
            if value.strip()
        ]
        buttons.append(indices)

    return target_values, buttons


def build_matrix(buttons: Sequence[Sequence[int]], num_counters: int) -> List[List[int]]:
    """Build the coefficient matrix describing button-to-counter relationships."""

    matrix = [[0] * len(buttons) for _ in range(num_counters)]
    for button_idx, indices in enumerate(buttons):
        seen: set[int] = set()
        for counter_idx in indices:
            if 0 <= counter_idx < num_counters and counter_idx not in seen:
                matrix[counter_idx][button_idx] = 1
                seen.add(counter_idx)
    return matrix


def compute_button_bounds(
    buttons: Sequence[Sequence[int]],
    num_counters: int,
    targets: Sequence[int],
) -> List[int]:
    """Return an absolute upper bound for each button press count."""

    bounds: List[int] = []
    for indices in buttons:
        relevant = [targets[idx] for idx in indices if 0 <= idx < num_counters]
        bounds.append(min(relevant) if relevant else 0)
    return bounds


def gaussian_elimination_rref(
    matrix: Sequence[Sequence[int]],
    targets: Sequence[int],
) -> Tuple[List[List[Fraction]], List[int], bool]:
    """Run Gauss-Jordan elimination over Fractions; return RREF and pivot info."""

    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows else 0
    augmented = [
        [Fraction(value) for value in row] + [Fraction(target)]
        for row, target in zip(matrix, targets)
    ]

    row = 0
    pivot_cols: List[int] = []

    for col in range(num_cols):
        pivot = None
        for search_row in range(row, num_rows):
            if augmented[search_row][col] != 0:
                pivot = search_row
                break
        if pivot is None:
            continue

        augmented[row], augmented[pivot] = augmented[pivot], augmented[row]

        pivot_val = augmented[row][col]
        augmented[row] = [value / pivot_val for value in augmented[row]]

        for other_row in range(num_rows):
            if other_row == row:
                continue
            factor = augmented[other_row][col]
            if factor == 0:
                continue
            augmented[other_row] = [
                augmented[other_row][idx] - factor * augmented[row][idx]
                for idx in range(num_cols + 1)
            ]

        pivot_cols.append(col)
        row += 1
        if row == num_rows:
            break

    inconsistent = False
    for check_row in range(num_rows):
        if all(augmented[check_row][c] == 0 for c in range(num_cols)):
            if augmented[check_row][num_cols] != 0:
                inconsistent = True
                break

    return augmented, pivot_cols, inconsistent


def verify_solution(
    matrix: Sequence[Sequence[int]],
    targets: Sequence[int],
    solution: Sequence[int],
) -> bool:
    """Ensure the candidate solution satisfies all constraints exactly."""

    num_rows = len(matrix)
    num_cols = len(solution)
    for row in range(num_rows):
        total = 0
        for col in range(num_cols):
            total += matrix[row][col] * solution[col]
        if total != targets[row]:
            return False
    return True


def search_free_variables(
    rhs: Sequence[Fraction],
    coeffs: Sequence[Sequence[Fraction]],
    pivot_cols: Sequence[int],
    free_vars: Sequence[int],
    button_bounds: Sequence[int],
    num_variables: int,
) -> Tuple[Optional[int], Optional[List[int]]]:
    """Enumerate feasible free-variable assignments while minimising presses."""

    num_pivots = len(pivot_cols)
    num_free = len(free_vars)

    if num_free == 0:
        return None, None

    order = sorted(range(num_free), key=lambda idx: button_bounds[free_vars[idx]])
    ordered_free_vars = [free_vars[idx] for idx in order]
    ordered_coeffs = [
        [coeffs[row][idx] for idx in order]
        for row in range(num_pivots)
    ]

    suffix_min = [[Fraction(0)] * (num_free + 1) for _ in range(num_pivots)]
    suffix_max = [[Fraction(0)] * (num_free + 1) for _ in range(num_pivots)]

    for row in range(num_pivots):
        for idx in range(num_free - 1, -1, -1):
            coeff = ordered_coeffs[row][idx]
            max_val = button_bounds[ordered_free_vars[idx]]
            if coeff >= 0:
                min_contrib = Fraction(0)
                max_contrib = coeff * max_val
            else:
                min_contrib = coeff * max_val
                max_contrib = Fraction(0)
            suffix_min[row][idx] = min_contrib + suffix_min[row][idx + 1]
            suffix_max[row][idx] = max_contrib + suffix_max[row][idx + 1]

    current_sum = [Fraction(0)] * num_pivots
    assignments = [0] * num_free
    best_total: Optional[int] = None
    best_vector: Optional[List[int]] = None

    def feasible_from(start_idx: int) -> bool:
        for row in range(num_pivots):
            min_total = current_sum[row] + suffix_min[row][start_idx]
            max_total = current_sum[row] + suffix_max[row][start_idx]
            lower = rhs[row] - max_total
            upper = rhs[row] - min_total
            pivot_idx = pivot_cols[row]
            lower_int = max(0, math.ceil(lower))
            upper_int = min(button_bounds[pivot_idx], math.floor(upper))
            if lower_int > upper_int:
                return False
        return True

    def dfs(idx: int, free_press_sum: int) -> None:
        nonlocal best_total, best_vector

        if best_total is not None and free_press_sum >= best_total:
            return

        if not feasible_from(idx):
            return

        if idx == num_free:
            candidate = [0] * num_variables
            total = free_press_sum
            for free_idx, var_index in enumerate(ordered_free_vars):
                candidate[var_index] = assignments[free_idx]

            for row in range(num_pivots):
                value = rhs[row] - current_sum[row]
                if value.denominator != 1:
                    return
                int_value = int(value)
                pivot_idx = pivot_cols[row]
                if int_value < 0 or int_value > button_bounds[pivot_idx]:
                    return
                candidate[pivot_idx] = int_value
                total += int_value

            if best_total is None or total < best_total:
                best_total = total
                best_vector = candidate
            return

        var_index = ordered_free_vars[idx]
        coeff_column = [ordered_coeffs[row][idx] for row in range(num_pivots)]
        upper_bound = button_bounds[var_index]

        for value in range(upper_bound + 1):
            new_sum = free_press_sum + value
            if best_total is not None and new_sum >= best_total:
                break

            for row in range(num_pivots):
                current_sum[row] += coeff_column[row] * value

            assignments[idx] = value
            dfs(idx + 1, new_sum)

            for row in range(num_pivots):
                current_sum[row] -= coeff_column[row] * value

    dfs(0, 0)
    return best_total, best_vector


def solve_machine(
    targets: Sequence[int],
    buttons: Sequence[Sequence[int]],
) -> Optional[Tuple[int, List[int]]]:
    """Solve a single machine definition."""

    num_counters = len(targets)
    num_buttons = len(buttons)

    if num_counters == 0:
        return 0, [0] * num_buttons

    if num_buttons == 0:
        if any(targets):
            return None
        return 0, []

    matrix = build_matrix(buttons, num_counters)
    button_bounds = compute_button_bounds(buttons, num_counters, targets)

    for row, target in zip(matrix, targets):
        if all(value == 0 for value in row) and target != 0:
            return None

    rref, pivot_cols, inconsistent = gaussian_elimination_rref(matrix, targets)
    if inconsistent:
        return None

    pivot_cols = list(pivot_cols)
    num_pivots = len(pivot_cols)
    pivot_set = set(pivot_cols)
    free_vars = [idx for idx in range(num_buttons) if idx not in pivot_set]

    rhs = [rref[row][-1] for row in range(num_pivots)]
    coeffs = [
        [rref[row][col] for col in free_vars]
        for row in range(num_pivots)
    ]

    if not free_vars:
        solution = [0] * num_buttons
        total = 0
        for row, col in enumerate(pivot_cols):
            value = rhs[row]
            if value.denominator != 1:
                return None
            int_value = int(value)
            if int_value < 0 or int_value > button_bounds[col]:
                return None
            solution[col] = int_value
            total += int_value

        if not verify_solution(matrix, targets, solution):
            return None
        return total, solution

    best_total, best_vector = search_free_variables(
        rhs,
        coeffs,
        pivot_cols,
        free_vars,
        button_bounds,
        num_buttons,
    )

    if best_vector is None or best_total is None:
        return None

    if not verify_solution(matrix, targets, best_vector):
        return None

    return best_total, best_vector


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "input.txt"

    total_presses = 0
    solved_machines = 0

    with input_path.open("r", encoding="utf-8") as handle:
        for line_num, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue

            targets, buttons = parse_machine_line(line)
            result = solve_machine(targets, buttons)

            if result is None:
                print(f"Machine {line_num}: No solution")
                continue

            presses, _ = result
            total_presses += presses
            solved_machines += 1
            print(f"Machine {line_num}: {presses} presses")

    print(
        f"\nTotal minimum presses for {solved_machines} machines: {total_presses}"
    )


if __name__ == "__main__":
    main()
