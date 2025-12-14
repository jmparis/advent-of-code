#!/usr/bin/env python3

def count_paths_svr_to_out_with_dac_fft():
    # Read the input file
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Parse the graph
    graph = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split device and outputs
        parts = line.split(': ')
        device = parts[0]
        outputs = parts[1].split()

        graph[device] = outputs

    # Memoization cache: (current, visited_dac, visited_fft) -> count
    memo = {}

    def dfs(current, visited, visited_dac, visited_fft):
        # Create cache key
        cache_key = (current, visited_dac, visited_fft)

        if cache_key in memo:
            return memo[cache_key]

        if current == 'out':
            # Only count paths that have visited both dac and fft
            result = 1 if (visited_dac and visited_fft) else 0
            memo[cache_key] = result
            return result

        if current in visited:
            memo[cache_key] = 0
            return 0  # Avoid cycles

        visited.add(current)

        # Check if we've visited the required nodes
        current_visited_dac = visited_dac or (current == 'dac')
        current_visited_fft = visited_fft or (current == 'fft')

        total = 0
        for neighbor in graph.get(current, []):
            total += dfs(neighbor, visited.copy(), current_visited_dac, current_visited_fft)

        visited.remove(current)
        memo[cache_key] = total
        return total

    # Start from 'svr'
    return dfs('svr', set(), False, False)

if __name__ == '__main__':
    result = count_paths_svr_to_out_with_dac_fft()
    print(f"Number of paths from 'svr' to 'out' that visit both 'dac' and 'fft': {result}")