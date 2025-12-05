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


def solve():
    """Solve the paper roll accessibility problem."""
    # Read the input file
    with open('input.txt', 'r') as f:
        lines = f.read().strip().split('\n')

    # Parse the grid
    grid = [list(line) for line in lines]

    # Count accessible rolls (rolls with < 4 neighbors)
    accessible_count = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                neighbors = count_neighbors(grid, row, col)
                if neighbors < 4:
                    accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    result = solve()
    print(f"Number of accessible paper rolls: {result}")
