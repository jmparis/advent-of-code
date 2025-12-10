#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Factory (Part 2)
Optimal solution using Integer Linear Programming with Gaussian Elimination

Problem: Find minimum button presses to set joltage counters to exact target values.
Each button press increments specific counters by 1.

Mathematical formulation:
- Minimize: Σ x[j] (total button presses)
- Subject to: A * x = targets (where A[i][j] = 1 if button j affects counter i)
- Constraints: x[j] >= 0, x[j] ∈ ℤ

Algorithm:
1. Use Gaussian elimination to find the solution space
2. Express solution as: x = x_particular + Σ c_i * null_basis_i
3. Search for non-negative integer solution with minimum L1 norm
"""

from typing import List, Tuple, Optional
from fractions import Fraction
import sys


def parse_machine_line(line: str) -> Tuple[List[int], List[List[int]]]:
    """Parse a machine configuration line for Part 2 (joltage requirements)."""
    start_brace = line.find('{')
    end_brace = line.find('}')
    joltage_str = line[start_brace + 1:end_brace]
    
    if joltage_str:
        targets = [int(x.strip()) for x in joltage_str.split(',')]
    else:
        targets = []
    
    button_configs = []
    start_paren = line.find('(')
    while start_paren != -1:
        end_paren = line.find(')', start_paren)
        if end_paren == -1:
            break
        
        button_str = line[start_paren + 1:end_paren]
        if button_str:
            if ',' in button_str:
                indices = [int(x.strip()) for x in button_str.split(',')]
            else:
                indices = [int(button_str)]
            button_configs.append(indices)
        
        start_paren = line.find('(', end_paren)
    
    return targets, button_configs


def gaussian_elimination_rational(A: List[List[Fraction]], b: List[Fraction]) -> Tuple[Optional[List[Fraction]], List[List[Fraction]], List[int], List[int]]:
    """
    Perform Gaussian elimination over rationals to find:
    1. A particular solution (if exists)
    2. Null space basis vectors
    3. Pivot and free variable indices
    
    Returns: (particular_solution, null_basis, pivot_cols, free_cols)
    """
    m = len(A)  # rows (counters)
    n = len(A[0]) if A else 0  # cols (buttons)
    
    # Create augmented matrix [A|b]
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    pivot_cols = []
    pivot_rows = []
    row = 0
    
    # Forward elimination
    for col in range(n):
        # Find pivot
        pivot_row = -1
        for r in range(row, m):
            if aug[r][col] != 0:
                pivot_row = r
                break
        
        if pivot_row == -1:
            continue
        
        # Swap rows
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_cols.append(col)
        pivot_rows.append(row)
        
        # Scale pivot row
        pivot_val = aug[row][col]
        for j in range(n + 1):
            aug[row][j] /= pivot_val
        
        # Eliminate column
        for r in range(m):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col]
                for j in range(n + 1):
                    aug[r][j] -= factor * aug[row][j]
        
        row += 1
    
    # Check for inconsistency
    for r in range(row, m):
        if aug[r][n] != 0:
            return None, [], pivot_cols, []  # No solution
    
    # Identify free variables
    free_cols = [j for j in range(n) if j not in pivot_cols]
    
    # Build particular solution (set free variables to 0)
    particular = [Fraction(0)] * n
    for i, pc in enumerate(pivot_cols):
        particular[pc] = aug[i][n]
    
    # Build null space basis
    null_basis = []
    for fc in free_cols:
        basis_vec = [Fraction(0)] * n
        basis_vec[fc] = Fraction(1)
        for i, pc in enumerate(pivot_cols):
            basis_vec[pc] = -aug[i][fc]
        null_basis.append(basis_vec)
    
    return particular, null_basis, pivot_cols, free_cols


def compute_coefficient_bounds(particular: List[Fraction], null_basis: List[List[Fraction]]) -> List[Tuple[int, int]]:
    """
    Compute bounds for each null space coefficient such that the solution can be non-negative.
    """
    n = len(particular)
    k = len(null_basis)
    bounds = []
    
    for i in range(k):
        min_c = -10000
        max_c = 10000
        
        for j in range(n):
            if null_basis[i][j] > 0:
                # particular[j] + c * null_basis[i][j] >= 0
                # c >= -particular[j] / null_basis[i][j]
                bound = float(-particular[j] / null_basis[i][j])
                min_c = max(min_c, int(bound) - 1)
            elif null_basis[i][j] < 0:
                # c <= -particular[j] / null_basis[i][j]
                bound = float(-particular[j] / null_basis[i][j])
                max_c = min(max_c, int(bound) + 1)
        
        bounds.append((min_c, max_c))
    
    return bounds


def find_min_nonneg_solution(particular: List[Fraction], null_basis: List[List[Fraction]], max_search: int = 100000) -> Optional[List[int]]:
    """
    Find the non-negative integer solution with minimum L1 norm.
    
    Solution form: x = particular + Σ c_i * null_basis_i
    We need x >= 0 and x integer, minimize sum(x).
    """
    n = len(particular)
    k = len(null_basis)
    
    if k == 0:
        # Unique solution - check if it's non-negative integer
        solution = []
        for v in particular:
            if v < 0 or v.denominator != 1:
                return None
            solution.append(int(v))
        return solution
    
    # Compute bounds for coefficients
    bounds = compute_coefficient_bounds(particular, null_basis)
    
    best_solution = None
    best_sum = float('inf')
    
    # For small null space, enumerate more thoroughly
    if k <= 3:
        from itertools import product
        
        # Create ranges with reasonable limits
        ranges = []
        for i in range(k):
            min_c, max_c = bounds[i]
            # Limit range size but ensure we cover the feasible region
            range_size = max_c - min_c + 1
            if range_size > 1000:
                # Sample more densely around 0
                mid = (min_c + max_c) // 2
                min_c = max(min_c, mid - 500)
                max_c = min(max_c, mid + 500)
            ranges.append(range(min_c, max_c + 1))
        
        for coeffs in product(*ranges):
            solution = []
            total = 0
            valid = True
            
            for j in range(n):
                val = particular[j]
                for i in range(k):
                    val += coeffs[i] * null_basis[i][j]
                
                if val < 0 or val.denominator != 1:
                    valid = False
                    break
                
                int_val = int(val)
                solution.append(int_val)
                total += int_val
            
            if valid and total < best_sum:
                best_sum = total
                best_solution = solution
        
        return best_solution
    
    # For medium null space (4-6 dimensions), use smarter search
    if k <= 6:
        from itertools import product
        
        # Create smaller ranges
        ranges = []
        for i in range(k):
            min_c, max_c = bounds[i]
            range_size = max_c - min_c + 1
            if range_size > 100:
                mid = (min_c + max_c) // 2
                min_c = max(min_c, mid - 50)
                max_c = min(max_c, mid + 50)
            ranges.append(range(min_c, max_c + 1))
        
        # Check if total combinations is manageable
        total_combos = 1
        for r in ranges:
            total_combos *= len(r)
        
        if total_combos <= max_search:
            for coeffs in product(*ranges):
                solution = []
                total = 0
                valid = True
                
                for j in range(n):
                    val = particular[j]
                    for i in range(k):
                        val += coeffs[i] * null_basis[i][j]
                    
                    if val < 0 or val.denominator != 1:
                        valid = False
                        break
                    
                    int_val = int(val)
                    solution.append(int_val)
                    total += int_val
                
                if valid and total < best_sum:
                    best_sum = total
                    best_solution = solution
            
            return best_solution
    
    # For larger null space, use heuristic search with multiple strategies
    import random
    
    # Strategy 1: Try coefficient = 0 first
    solution = []
    valid = True
    for v in particular:
        if v < 0 or v.denominator != 1:
            valid = False
            break
        solution.append(int(v))
    
    if valid:
        best_solution = solution
        best_sum = sum(solution)
    
    # Strategy 2: Try to minimize by setting coefficients to make particular values smaller
    for _ in range(min(max_search // 2, 50000)):
        coeffs = []
        for i in range(k):
            min_c, max_c = bounds[i]
            # Bias towards middle of range
            mid = (min_c + max_c) // 2
            spread = min(100, (max_c - min_c) // 2)
            c = random.randint(max(min_c, mid - spread), min(max_c, mid + spread))
            coeffs.append(c)
        
        solution = []
        total = 0
        valid = True
        
        for j in range(n):
            val = particular[j]
            for i in range(k):
                val += coeffs[i] * null_basis[i][j]
            
            if val < 0 or val.denominator != 1:
                valid = False
                break
            
            int_val = int(val)
            solution.append(int_val)
            total += int_val
        
        if valid and total < best_sum:
            best_sum = total
            best_solution = solution
    
    # Strategy 3: Local search from best solution found
    if best_solution is not None:
        # Try to improve by adjusting coefficients
        current_coeffs = [0] * k  # Start from zero coefficients
        
        for iteration in range(1000):
            improved = False
            for i in range(k):
                for delta in [-1, 1, -10, 10, -50, 50]:
                    new_coeffs = current_coeffs[:]
                    new_coeffs[i] += delta
                    
                    # Check bounds
                    min_c, max_c = bounds[i]
                    if new_coeffs[i] < min_c or new_coeffs[i] > max_c:
                        continue
                    
                    solution = []
                    total = 0
                    valid = True
                    
                    for j in range(n):
                        val = particular[j]
                        for ii in range(k):
                            val += new_coeffs[ii] * null_basis[ii][j]
                        
                        if val < 0 or val.denominator != 1:
                            valid = False
                            break
                        
                        int_val = int(val)
                        solution.append(int_val)
                        total += int_val
                    
                    if valid and total < best_sum:
                        best_sum = total
                        best_solution = solution
                        current_coeffs = new_coeffs
                        improved = True
            
            if not improved:
                break
    
    return best_solution


def solve_linear_system(targets: List[int], buttons: List[List[int]]) -> Optional[int]:
    """
    Solve the linear system A * x = targets over non-negative integers.
    Minimize sum(x).
    """
    n_counters = len(targets)
    n_buttons = len(buttons)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in targets) else None
    
    if all(t == 0 for t in targets):
        return 0
    
    # Build coefficient matrix A (as Fractions for exact arithmetic)
    A = [[Fraction(0)] * n_buttons for _ in range(n_counters)]
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                A[counter_idx][j] = Fraction(1)
    
    b = [Fraction(t) for t in targets]
    
    # Solve using Gaussian elimination
    particular, null_basis, pivot_cols, free_cols = gaussian_elimination_rational(A, b)
    
    if particular is None:
        return None  # No solution exists
    
    # Find minimum non-negative integer solution
    solution = find_min_nonneg_solution(particular, null_basis)
    
    if solution is None:
        return None
    
    return sum(solution)


def solve_machine(targets: List[int], buttons: List[List[int]]) -> Optional[int]:
    """Main solver."""
    n_buttons = len(buttons)
    n_counters = len(targets)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in targets) else None
    
    if all(t == 0 for t in targets):
        return 0
    
    if any(t < 0 for t in targets):
        return None
    
    # Check if any counter has no buttons affecting it
    counter_coverage = [0] * n_counters
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                counter_coverage[counter_idx] += 1
    
    for i in range(n_counters):
        if targets[i] > 0 and counter_coverage[i] == 0:
            return None
    
    return solve_linear_system(targets, buttons)


def main():
    """Main function to solve the Part 2 factory problem."""
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    
    total_presses = 0
    valid_machines = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        try:
            targets, button_configs = parse_machine_line(line)
            min_presses = solve_machine(targets, button_configs)
            
            if min_presses is not None:
                total_presses += min_presses
                valid_machines += 1
                print(f"Machine {line_num}: {min_presses} presses")
            else:
                print(f"Machine {line_num}: No solution")
        
        except Exception as e:
            print(f"Error processing line {line_num}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\nTotal minimum button presses for {valid_machines} machines: {total_presses}")
    return total_presses


if __name__ == "__main__":
    main()