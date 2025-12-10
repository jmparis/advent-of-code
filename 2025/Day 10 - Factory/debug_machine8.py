#!/usr/bin/env python3
from fractions import Fraction

def parse_machine_line(line):
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


def gaussian_elimination_rational(A, b):
    m = len(A)
    n = len(A[0]) if A else 0
    
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    pivot_cols = []
    pivot_rows = []
    row = 0
    
    for col in range(n):
        pivot_row = -1
        for r in range(row, m):
            if aug[r][col] != 0:
                pivot_row = r
                break
        
        if pivot_row == -1:
            continue
        
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_cols.append(col)
        pivot_rows.append(row)
        
        pivot_val = aug[row][col]
        for j in range(n + 1):
            aug[row][j] /= pivot_val
        
        for r in range(m):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col]
                for j in range(n + 1):
                    aug[r][j] -= factor * aug[row][j]
        
        row += 1
    
    for r in range(row, m):
        if aug[r][n] != 0:
            return None, [], pivot_cols, []
    
    free_cols = [j for j in range(n) if j not in pivot_cols]
    
    particular = [Fraction(0)] * n
    for i, pc in enumerate(pivot_cols):
        particular[pc] = aug[i][n]
    
    null_basis = []
    for fc in free_cols:
        basis_vec = [Fraction(0)] * n
        basis_vec[fc] = Fraction(1)
        for i, pc in enumerate(pivot_cols):
            basis_vec[pc] = -aug[i][fc]
        null_basis.append(basis_vec)
    
    return particular, null_basis, pivot_cols, free_cols


# Machine 8 from input
line = '[...####.#.] (0,1,4,5,8) (4,6,7) (1,3,4,5,6,8,9) (0,5,9) (1,2,4,5,9) (0,2,3,4,5,6,7,8) (0,5,6,9) (1,3,8,9) (1,3,5,7,8,9) (4,5,7) (1,3,5,6,7,8,9) (1,2,4,5,6,7,8) (3,5,6,7) {145,40,16,28,49,200,23,46,32,152}'

targets, buttons = parse_machine_line(line)
print(f'Targets: {targets}')
print(f'Num counters: {len(targets)}')
print(f'Num buttons: {len(buttons)}')

# Build matrix
n_counters = len(targets)
n_buttons = len(buttons)
A = [[Fraction(0)] * n_buttons for _ in range(n_counters)]
for j, button in enumerate(buttons):
    for counter_idx in button:
        if counter_idx < n_counters:
            A[counter_idx][j] = Fraction(1)

b = [Fraction(t) for t in targets]

# Solve
particular, null_basis, pivot_cols, free_cols = gaussian_elimination_rational(A, b)
print(f'Particular solution: {[float(p) for p in particular] if particular else None}')
print(f'Null basis size: {len(null_basis)}')
print(f'Pivot cols: {pivot_cols}')
print(f'Free cols: {free_cols}')

if particular:
    print(f'Particular has negative values: {any(v < 0 for v in particular)}')
    print(f'Particular has non-integer values: {any(v.denominator != 1 for v in particular)}')
    neg_vals = [(i, float(v)) for i, v in enumerate(particular) if v < 0]
    print(f'Negative values: {neg_vals}')
    
    print(f'\nNull basis vectors:')
    for i, vec in enumerate(null_basis):
        print(f'  Basis {i} (free var {free_cols[i]}): {[float(v) for v in vec]}')
    
    # Check if null basis has non-integer values
    print(f'\nChecking for non-integer null basis values...')
    has_non_integer = False
    for i, vec in enumerate(null_basis):
        for j, v in enumerate(vec):
            if v.denominator != 1:
                print(f'  Basis {i}, position {j}: {v} (denominator={v.denominator})')
                has_non_integer = True
    
    if has_non_integer:
        print('Null basis has non-integer values - need to find integer multiples')
    
    # Brute force search with wider range
    print(f'\nBrute force searching for any valid solution...')
    
    best_solution = None
    best_sum = float('inf')
    best_coeffs = None
    
    k = len(null_basis)
    n = len(particular)
    
    # Search a reasonable range
    search_range = 100
    count = 0
    found_any = False
    
    for c0 in range(-search_range, search_range + 1):
        for c1 in range(-search_range, search_range + 1):
            for c2 in range(-search_range, search_range + 1):
                count += 1
                coeffs = [c0, c1, c2]
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
                
                if valid:
                    found_any = True
                    if total < best_sum:
                        best_sum = total
                        best_solution = solution
                        best_coeffs = coeffs
    
    print(f'Searched {count} combinations')
    
    if best_solution:
        print(f'Found solution with {best_sum} total presses')
        print(f'Coefficients: {best_coeffs}')
        print(f'Solution: {best_solution}')
        
        # Verify
        result = [0] * n_counters
        for j, presses in enumerate(best_solution):
            for counter_idx in buttons[j]:
                if counter_idx < n_counters:
                    result[counter_idx] += presses
        print(f'Verification - Result: {result}')
        print(f'Verification - Target: {targets}')
        print(f'Match: {result == targets}')
    else:
        print('No valid solution found - this machine may be truly unsolvable')
        print('(The linear system has no non-negative integer solution)')