#!/usr/bin/env python3

def count_paths_from_you_to_out():
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

    # Count paths using DFS
    def dfs(current, visited, path_count):
        if current == 'out':
            return path_count + 1

        if current in visited:
            return path_count  # Avoid cycles

        visited.add(current)

        for neighbor in graph.get(current, []):
            path_count = dfs(neighbor, visited.copy(), path_count)

        return path_count

    # Start from 'you'
    return dfs('you', set(), 0)

if __name__ == '__main__':
    result = count_paths_from_you_to_out()
    print(f"Number of paths from 'you' to 'out': {result}")