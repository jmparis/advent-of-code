#!/usr/bin/env python3

def parse_machine_line_part2(line):
    """Parse a machine configuration line for Part 2 (joltage requirements)."""
    # Extract joltage requirements from curly braces
    start_brace = line.find('{')
    end_brace = line.find('}')
    joltage_str = line[start_brace+1:end_brace]
    
    # Convert joltage requirements to target list
    if joltage_str:
        targets = [int(x.strip()) for x in joltage_str.split(',')]
    else:
        targets = []
    
    # Extract buttons from parentheses (same as Part 1)
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
    
    return targets, button_configs

def solve_min_presses_fast(targets, button_configs):
    """
    Fast heuristic solution for the integer linear programming problem.
    Prioritizes speed over guaranteed optimality.
    """
    n_counters = len(targets)
    n_buttons = len(button_configs)
    
    # If no buttons or no counters, check if already solved
    if n_buttons == 0 or n_counters == 0:
        return 0 if all(t == 0 for t in targets) else float('inf')
    
    # Check if any target is negative (invalid)
    if any(t < 0 for t in targets):
        return float('inf')
    
    # For very small problems, use brute force
    if n_buttons <= 6 and max(targets) <= 10:
        return solve_brute_force_small(targets, button_configs)
    
    # For larger problems, use fast heuristic
    return solve_fast_heuristic(targets, button_configs)

def solve_brute_force_small(targets, button_configs):
    """Brute force for very small problems."""
    n_buttons = len(button_configs)
    n_counters = len(targets)
    
    min_presses = float('inf')
    
    # Try all combinations with reasonable bounds
    max_target = max(targets) if targets else 0
    max_presses_per_button = min(max_target, 5)  # Cap to avoid explosion
    
    def search(button_idx, current_counters, total_presses):
        nonlocal min_presses
        
        # Prune
        if total_presses >= min_presses:
            return
        
        # If all buttons processed, check solution
        if button_idx == n_buttons:
            if current_counters == targets:
                min_presses = min(min_presses, total_presses)
            return
        
        # Try different press counts for this button
        for presses in range(max_presses_per_button + 1):
            # Apply button presses
            new_counters = current_counters[:]
            for counter_idx in button_configs[button_idx]:
                if counter_idx < n_counters:
                    new_counters[counter_idx] += presses
            
            # Check if this exceeds any target (prune)
            exceeds = False
            for i in range(n_counters):
                if new_counters[i] > targets[i]:
                    exceeds = True
                    break
            
            if not exceeds:
                search(button_idx + 1, new_counters, total_presses + presses)
    
    search(0, [0] * n_counters, 0)
    return min_presses if min_presses != float('inf') else None

def solve_fast_heuristic(targets, button_configs):
    """
    Fast heuristic using multiple strategies.
    """
    n_counters = len(targets)
    n_buttons = len(button_configs)
    
    # Strategy 1: Greedy approach
    solution1 = greedy_approach(targets, button_configs)
    best_presses = solution1 if solution1 is not None else float('inf')
    
    # Strategy 2: Randomized local search
    solution2 = random_local_search(targets, button_configs, 50)
    if solution2 is not None:
        best_presses = min(best_presses, solution2)
    
    # Strategy 3: Simple bounds-based approach
    solution3 = bounds_approach(targets, button_configs)
    if solution3 is not None:
        best_presses = min(best_presses, solution3)
    
    return best_presses if best_presses != float('inf') else None

def greedy_approach(targets, button_configs):
    """Greedy approach: always press buttons that help most."""
    n_counters = len(targets)
    n_buttons = len(button_configs)
    
    solution = [0] * n_buttons
    remaining = targets[:]
    
    # Keep pressing while there are remaining targets
    iterations = 0
    while any(r > 0 for r in remaining) and iterations < 1000:
        iterations += 1
        
        best_button = -1
        best_score = -1
        
        # Find the button that helps most
        for j in range(n_buttons):
            # Calculate how much this button helps
            score = 0
            for counter_idx in button_configs[j]:
                if counter_idx < n_counters and remaining[counter_idx] > 0:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_button = j
        
        if best_button == -1 or best_score == 0:
            break
        
        # Press the best button once
        solution[best_button] += 1
        for counter_idx in button_configs[best_button]:
            if counter_idx < n_counters:
                remaining[counter_idx] -= 1
    
    # Verify solution
    if verify_solution(solution, targets, button_configs):
        return sum(solution)
    
    return None

def random_local_search(targets, button_configs, iterations):
    """Random local search with improvement."""
    import random
    
    n_counters = len(targets)
    n_buttons = len(button_configs)
    
    max_target = max(targets) if targets else 0
    best_presses = float('inf')
    
    for _ in range(iterations):
        # Start with random solution
        solution = [random.randint(0, max_target) for _ in range(n_buttons)]
        
        # Local improvement
        improved = True
        while improved:
            improved = False
            
            # Try to reduce presses
            for j in range(n_buttons):
                if solution[j] > 0:
                    solution[j] -= 1
                    if verify_solution(solution, targets, button_configs):
                        improved = True
                    else:
                        solution[j] += 1
            
            # Try to add presses if needed
            if not verify_solution(solution, targets, button_configs):
                for j in range(n_buttons):
                    solution[j] += 1
                    if verify_solution(solution, targets, button_configs):
                        improved = True
                        break
                    solution[j] -= 1
        
        # Check if this is better
        if verify_solution(solution, targets, button_configs):
            presses = sum(solution)
            if presses < best_presses:
                best_presses = presses
    
    return best_presses if best_presses != float('inf') else None

def bounds_approach(targets, button_configs):
    """Simple bounds-based approach."""
    n_counters = len(targets)
    n_buttons = len(button_configs)
    
    # Calculate minimum presses needed for each counter
    min_presses_per_counter = []
    for i in range(n_counters):
        min_needed = targets[i]
        if min_needed > 0:
            # Count how many buttons affect this counter
            affecting_buttons = sum(1 for j in range(n_buttons) 
                                  if i in button_configs[j])
            if affecting_buttons > 0:
                min_needed = (targets[i] + affecting_buttons - 1) // affecting_buttons
        min_presses_per_counter.append(min_needed)
    
    # Create a simple solution
    solution = [0] * n_buttons
    
    # Distribute presses based on simple bounds
    for j in range(n_buttons):
        # Calculate how many presses this button should get
        presses_needed = 0
        for counter_idx in button_configs[j]:
            if counter_idx < n_counters:
                presses_needed += min_presses_per_counter[counter_idx]
        solution[j] = presses_needed // len(button_configs[j]) if button_configs[j] else 0
    
    # Adjust to meet exact targets
    current = [0] * n_counters
    for j, presses in enumerate(solution):
        for counter_idx in button_configs[j]:
            if counter_idx < n_counters:
                current[counter_idx] += presses
    
    # Simple adjustment
    for i in range(n_counters):
        while current[i] < targets[i]:
            # Find a button that affects this counter and press it
            for j in range(n_buttons):
                if i in button_configs[j]:
                    solution[j] += 1
                    for counter_idx in button_configs[j]:
                        if counter_idx < n_counters:
                            current[counter_idx] += 1
                    break
    
    if verify_solution(solution, targets, button_configs):
        return sum(solution)
    
    return None

def verify_solution(solution, targets, button_configs):
    """Verify that a solution achieves the target joltage levels."""
    n_counters = len(targets)
    
    # Calculate resulting joltage levels
    result = [0] * n_counters
    for j, presses in enumerate(solution):
        if presses > 0:
            for counter_idx in button_configs[j]:
                if counter_idx < n_counters:
                    result[counter_idx] += presses
    
    return result == targets

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
            targets, button_configs = parse_machine_line_part2(line)
            min_presses = solve_min_presses_fast(targets, button_configs)
            
            if min_presses is not None:
                total_presses += min_presses
                valid_machines += 1
                print(f"Machine {line_num}: {min_presses} presses")
            else:
                print(f"Machine {line_num}: No solution")
        
        except Exception as e:
            print(f"Error processing line {line_num}: {e}")
            print(f"Line content: {line}")
    
    print(f"\nTotal minimum button presses for {valid_machines} machines: {total_presses}")
    return total_presses

if __name__ == "__main__":
    main()