def is_invalid_id(num):
    """
    Check if a number is an invalid ID.
    Invalid IDs are numbers where a sequence of digits is repeated exactly twice.
    For example: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    No leading zeroes allowed.
    """
    num_str = str(num)
    length = len(num_str)

    # Must have even length to be repeated twice
    if length % 2 != 0:
        return False

    # Split in half
    half_len = length // 2
    first_half = num_str[:half_len]
    second_half = num_str[half_len:]

    # Check if both halves are identical
    if first_half == second_half:
        # Check for leading zeroes - first_half shouldn't start with 0
        # (unless it's just "0", but we're told numbers don't have leading zeroes)
        if first_half[0] != '0':
            return True

    return False


def parse_ranges(input_text):
    """
    Parse comma-separated ranges from input text.
    Returns a list of (start, end) tuples.
    """
    ranges = []
    parts = input_text.strip().split(',')

    for part in parts:
        if '-' in part:
            # Split on the last dash to handle negative numbers if any
            # But in this case all numbers are positive
            range_parts = part.split('-')
            # Handle cases where there might be multiple dashes
            if len(range_parts) == 2:
                start = int(range_parts[0])
                end = int(range_parts[1])
                ranges.append((start, end))
            else:
                # Find the split point - should be between two numbers
                # For simplicity with positive numbers:
                dash_pos = part.index('-')
                start = int(part[:dash_pos])
                end = int(part[dash_pos+1:])
                ranges.append((start, end))

    return ranges


def find_invalid_ids_in_range(start, end):
    """
    Find all invalid IDs in the given range [start, end].
    Returns a list of invalid IDs.
    """
    invalid_ids = []

    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)

    return invalid_ids


def main():
    # Read input from file
    with open('input.txt', 'r') as f:
        input_text = f.read()

    # Parse ranges
    ranges = parse_ranges(input_text)

    # Find all invalid IDs across all ranges
    all_invalid_ids = []

    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        all_invalid_ids.extend(invalid_ids)

    # Calculate the sum
    total = sum(all_invalid_ids)

    print(f"Total sum of invalid IDs: {total}")


if __name__ == "__main__":
    main()
