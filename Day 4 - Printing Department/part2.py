def count_neighbors(grid, row, col):
    """Count the number of @ symbols in the 8 adjacent positions."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Define all 8 directions: N, S, E, W, NE, NW, SE, SW
    directions = [
        (-1, 0),   # North
        (1, 0),    # South
        (0, 1),    # East
        (0, -1),   # West
        (-1, 1),   # Northeast
        (-1, -1),  # Northwest
        (1, 1),    # Southeast
        (1, -1)    # Southwest
    ]

    count = 0
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Check bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1

    return count


def find_accessible_rolls(grid):
    """Find all accessible rolls (rolls with < 4 neighbors) in the current grid."""
    accessible = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                neighbors = count_neighbors(grid, row, col)
                if neighbors < 4:
                    accessible.append((row, col))

    return accessible


def remove_rolls(grid, positions):
    """Remove rolls at the specified positions by replacing them with '.'"""
    for row, col in positions:
        grid[row][col] = '.'


def solve():
    """Solve the iterative paper roll removal problem."""
    # Read the input file
    with open('input.txt', 'r') as f:
        lines = f.read().strip().split('\n')

    # Parse the grid (make it mutable)
    grid = [list(line) for line in lines]

    total_removed = 0

    # Keep removing accessible rolls until no more can be removed
    while True:
        # Find all accessible rolls in current state
        accessible = find_accessible_rolls(grid)

        # If no more accessible rolls, stop
        if not accessible:
            break

        # Remove all accessible rolls
        remove_rolls(grid, accessible)

        # Update total count
        total_removed += len(accessible)

        print(f"Removed {len(accessible)} rolls (total: {total_removed})")

    return total_removed


if __name__ == "__main__":
    result = solve()
    print(f"\nTotal rolls of paper removed: {result}")
