def is_invalid_id(num):
    """
    Check if a number is an invalid ID (Part 2 rules).
    Invalid IDs are numbers where a sequence of digits is repeated at least twice.
    For example: 
    - 55 (5 twice)
    - 6464 (64 twice)
    - 123123123 (123 three times)
    - 1212121212 (12 five times)
    - 1111111 (1 seven times)
    No leading zeroes allowed.
    """
    num_str = str(num)
    length = len(num_str)

    # Check if the number starts with 0 (leading zero - not allowed)
    if num_str[0] == '0':
        return False

    # Try all possible pattern lengths from 1 to length//2
    # The pattern must repeat at least twice
    for pattern_len in range(1, length // 2 + 1):
        # Check if the length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]

            # Check if pattern starts with 0 (would be leading zero)
            if pattern[0] == '0':
                continue

            # Check if repeating this pattern gives us the original number
            repetitions = length // pattern_len
            if pattern * repetitions == num_str and repetitions >= 2:
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
