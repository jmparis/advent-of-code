#!/usr/bin/env python3

def parse_machine_line(line):
    """Parse a machine configuration line into target and buttons."""
    # Extract target configuration from brackets
    start_bracket = line.find('[')
    end_bracket = line.find(']')
    target_str = line[start_bracket+1:end_bracket]
    
    # Convert target to binary list (1 for #, 0 for .)
    target = [1 if c == '#' else 0 for c in target_str]
    
    # Extract buttons from parentheses
    button_configs = []
    start_paren = line.find('(')
    while start_paren != -1:
        end_paren = line.find(')', start_paren)
        if end_paren == -1:
            break
        
        button_str = line[start_paren+1:end_paren]
        if button_str:  # Skip empty buttons
            # Convert button config to list of indices
            if ',' in button_str:
                indices = [int(x.strip()) for x in button_str.split(',')]
            else:
                indices = [int(button_str)]
            button_configs.append(indices)
        
        start_paren = line.find('(', end_paren)
    
    return target, button_configs

def solve_min_presses_brute_force(target, button_configs):
    """Brute force solution."""
    n_buttons = len(button_configs)
    n_lights = len(target)
    
    min_presses = float('inf')
    
    # Try all possible combinations
    for combo in range(1 << n_buttons):
        # Simulate button presses
        lights = [0] * n_lights
        presses = 0
        
        for i in range(n_buttons):
            if (combo >> i) & 1:
                presses += 1
                for light_idx in button_configs[i]:
                    lights[light_idx] ^= 1
        
        # Check if this achieves the target
        if lights == target:
            min_presses = min(min_presses, presses)
    
    return min_presses if min_presses != float('inf') else None

def solve_min_presses_optimized(target, button_configs):
    """
    Optimized solution for larger systems.
    Uses a combination of techniques to find minimum weight solution.
    """
    n_lights = len(target)
    n_buttons = len(button_configs)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in target) else None
    
    # Build the matrix A where A[i][j] = 1 if button j affects light i
    A = [[0] * n_buttons for _ in range(n_lights)]
    for j, button in enumerate(button_configs):
        for light_idx in button:
            if light_idx < n_lights:
                A[light_idx][j] = 1
    
    # Convert target to column vector b
    b = target[:]
    
    # Create augmented matrix [A|b]
    aug = [A[i][:] + [b[i]] for i in range(n_lights)]
    
    # Forward elimination to row echelon form
    row = 0
    col = 0
    pivot_cols = []
    
    while row < n_lights and col < n_buttons:
        # Find pivot
        pivot = -1
        for i in range(row, n_lights):
            if aug[i][col] == 1:
                pivot = i
                break
        
        if pivot == -1:
            col += 1
            continue
        
        # Swap rows
        aug[row], aug[pivot] = aug[pivot], aug[row]
        pivot_cols.append(col)
        
        # Eliminate column below
        for i in range(row + 1, n_lights):
            if aug[i][col] == 1:
                for j in range(col, n_buttons + 1):
                    aug[i][j] ^= aug[row][j]
        
        row += 1
        col += 1
    
    # Back substitution to reduced row echelon form
    for i in range(len(pivot_cols) - 1, -1, -1):
        pivot_col = pivot_cols[i]
        # Eliminate column above
        for j in range(i):
            if aug[j][pivot_col] == 1:
                for k in range(pivot_col, n_buttons + 1):
                    aug[j][k] ^= aug[i][k]
    
    # Check for inconsistency
    for i in range(row, n_lights):
        if all(aug[i][j] == 0 for j in range(n_buttons)) and aug[i][n_buttons] == 1:
            return None  # No solution
    
    # Identify pivot and free variables
    pivot_vars = set(pivot_cols)
    free_vars = [i for i in range(n_buttons) if i not in pivot_vars]
    
    if not free_vars:
        # Unique solution
        solution = [0] * n_buttons
        for i, pivot_col in enumerate(pivot_cols):
            solution[pivot_col] = aug[i][n_buttons]
        return sum(solution)
    
    # Find particular solution (set all free variables to 0)
    particular = [0] * n_buttons
    for i, pivot_col in enumerate(pivot_cols):
        if i < len(aug):
            particular[pivot_col] = aug[i][n_buttons]
    
    # For small number of free variables, try all combinations
    if len(free_vars) <= 15:
        min_presses = float('inf')
        n_combinations = 1 << len(free_vars)
        
        for combo in range(n_combinations):
            # Build solution: particular + combination of null space basis
            solution = particular[:]
            
            # Set free variables according to combination
            for j, free_var in enumerate(free_vars):
                if (combo >> j) & 1:
                    solution[free_var] = 1
            
            # Update pivot variables based on the free variables
            for i, pivot_col in enumerate(pivot_cols):
                if i < len(aug):
                    # Calculate the value for this pivot variable
                    val = aug[i][n_buttons]
                    for j, free_var in enumerate(free_vars):
                        if (combo >> j) & 1:
                            # Check if this free variable appears in the equation
                            if free_var < len(aug[i]) - 1 and aug[i][free_var] == 1:
                                val ^= 1
                    solution[pivot_col] = val
            
            # Verify solution and count presses
            presses = sum(solution)
            
            # Quick check: verify the solution works
            works = True
            for i in range(n_lights):
                sum_val = 0
                for j in range(n_buttons):
                    sum_val ^= (A[i][j] & solution[j])
                if sum_val != b[i]:
                    works = False
                    break
            
            if works and presses < min_presses:
                min_presses = presses
        
        return min_presses if min_presses != float('inf') else 0
    else:
        # For many free variables, use heuristic search
        min_presses = float('inf')
        
        # Try several heuristic approaches
        for attempt in range(1000):
            # Approach 1: Start with particular solution
            solution = particular[:]
            
            # Randomly set some free variables
            for free_var in free_vars:
                if hash(free_var + attempt) % 3 == 0:  # Pseudo-random
                    solution[free_var] = 1
            
            # Update pivot variables
            for i, pivot_col in enumerate(pivot_cols):
                if i < len(aug):
                    val = aug[i][n_buttons]
                    for free_var in free_vars:
                        if solution[free_var] == 1 and free_var < len(aug[i]) - 1 and aug[i][free_var] == 1:
                            val ^= 1
                    solution[pivot_col] = val
            
            # Verify solution
            works = True
            for i in range(n_lights):
                sum_val = 0
                for j in range(n_buttons):
                    sum_val ^= (A[i][j] & solution[j])
                if sum_val != b[i]:
                    works = False
                    break
            
            if works:
                presses = sum(solution)
                if presses < min_presses:
                    min_presses = presses
        
        return min_presses if min_presses != float('inf') else 0

def solve_min_presses(target, button_configs):
    """
    Main solver that chooses the appropriate algorithm based on problem size.
    """
    n_buttons = len(button_configs)
    
    # Use brute force for smaller problems where we can guarantee optimality
    if n_buttons <= 20:
        return solve_min_presses_brute_force(target, button_configs)
    else:
        # Use optimized approach for larger problems
        return solve_min_presses_optimized(target, button_configs)

def main():
    """Main function to solve the factory problem."""
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    
    total_presses = 0
    valid_machines = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        try:
            target, button_configs = parse_machine_line(line)
            min_presses = solve_min_presses(target, button_configs)
            
            if min_presses is not None:
                total_presses += min_presses
                valid_machines += 1
                print(f"Machine {line_num}: {min_presses} presses")
            else:
                print(f"Machine {line_num}: No solution")
        
        except Exception as e:
            print(f"Error processing line {line_num}: {e}")
            print(f"Line content: {line}")
    
    print(f"\nTotal minimum presses for {valid_machines} machines: {total_presses}")
    return total_presses

if __name__ == "__main__":
    main()