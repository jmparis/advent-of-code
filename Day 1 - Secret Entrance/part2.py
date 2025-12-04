def read_rotations(filename):
    """Read rotation instructions from a file."""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []


def rotate_dial(current_position, direction, clicks):
    """
    Rotate the dial from current position.

    Args:
        current_position: Current dial position (0-99)
        direction: 'L' for left (toward lower numbers) or 'R' for right (toward higher numbers)
        clicks: Number of clicks to rotate

    Returns:
        New position after rotation (0-99)
    """
    if direction == 'R':
        # Right: toward higher numbers (clockwise)
        new_position = (current_position + clicks) % 100
    elif direction == 'L':
        # Left: toward lower numbers (counterclockwise)
        new_position = (current_position - clicks) % 100
    else:
        raise ValueError(f"Invalid direction: {direction}")

    return new_position


def parse_rotation(rotation_str):
    """
    Parse a rotation string like 'R8' or 'L19'.

    Returns:
        Tuple of (direction, clicks)
    """
    direction = rotation_str[0].upper()
    clicks = int(rotation_str[1:])
    return direction, clicks


def solve_safe(rotations, verbose=True):
    """
    Process all rotations starting from position 50.

    Args:
        rotations: List of rotation strings
        verbose: If True, print each step

    Returns:
        Tuple of (final_position, zero_count)
    """
    position = 50
    zero_count = 0

    if verbose:
        print(f"Starting position: {position}")
        print("-" * 40)

    for i, rotation_str in enumerate(rotations, 1):
        direction, clicks = parse_rotation(rotation_str)
        new_position = rotate_dial(position, direction, clicks)

        if new_position == 0:
            zero_count += 1

        if verbose:
            marker = " ⭐ ZERO!" if new_position == 0 else ""
            print(f"Step {i}: {rotation_str} -> {position} → {new_position}{marker}")

        position = new_position

    if verbose:
        print("-" * 40)
        print(f"Final position: {position}")

    return position, zero_count


def main():
    """Main function to run the safe dial simulator."""
    input_file = "input.txt"

    print("Safe Dial Rotation Simulator")
    print("=" * 40)

    rotations = read_rotations(input_file)

    if not rotations:
        print(f"\nNo rotations found in '{input_file}'.")
        print("Please create an input.txt file with rotation instructions.")
        print("Format: One rotation per line (e.g., R8, L19)")
        return

    print(f"Loaded {len(rotations)} rotation(s)\n")

    final_position, zero_count = solve_safe(rotations, verbose=True)

    print(f"\n🔓 The safe dial points to: {final_position}")
    print(f"📊 The dial reached 0 a total of {zero_count} time(s)")


if __name__ == "__main__":
    main()
