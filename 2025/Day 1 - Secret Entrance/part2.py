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


def count_zero_crossings(current_position, direction, clicks):
    """
    Count how many times the dial points at 0 during a rotation.
    This includes both landing on 0 at the end AND passing through 0 during the rotation.

    Args:
        current_position: Current dial position (0-99)
        direction: 'L' for left or 'R' for right
        clicks: Number of clicks to rotate

    Returns:
        Number of times the dial points at 0 during this rotation
    """
    count = 0

    if clicks == 0:
        return 0

    if direction == 'R':
        # Moving right (toward higher numbers)
        # Count how many times we cross 0 (which is when position % 100 == 0)
        # We cross 0 when going from 99 to 0
        for i in range(1, clicks + 1):
            if (current_position + i) % 100 == 0:
                count += 1
    elif direction == 'L':
        # Moving left (toward lower numbers)
        # Count how many times we cross 0
        for i in range(1, clicks + 1):
            if (current_position - i) % 100 == 0:
                count += 1

    return count


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
    Counts ALL times the dial points at 0, including during rotations.
    (Method 0x434C49434B - "CLICK")

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
        print(f"Using password method 0x434C49434B (counting all clicks through 0)")
        print("-" * 40)

    for i, rotation_str in enumerate(rotations, 1):
        direction, clicks = parse_rotation(rotation_str)
        new_position = rotate_dial(position, direction, clicks)

        # Count how many times we point at 0 during this rotation
        zeros_in_rotation = count_zero_crossings(position, direction, clicks)
        zero_count += zeros_in_rotation

        if verbose:
            if zeros_in_rotation > 0:
                marker = f" ⭐ {zeros_in_rotation} zero(s)!"
            else:
                marker = ""
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
    print(f"🔑 Password (method 0x434C49434B): {zero_count}")
    print(f"📊 The dial pointed at 0 a total of {zero_count} time(s) (including during rotations)")


if __name__ == "__main__":
    main()
