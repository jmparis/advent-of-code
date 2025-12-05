def is_fresh(ingredient_id, fresh_ranges):
    """Check if an ingredient ID falls within any of the fresh ranges."""
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def main():
    # Read the input file
    with open('input.txt', 'r') as file:
        lines = file.read().strip().split('\n')

    # Find the blank line that separates ranges from ingredient IDs
    blank_line_index = lines.index('')

    # Parse the fresh ID ranges
    fresh_ranges = []
    for i in range(blank_line_index):
        parts = lines[i].split('-')
        start = int(parts[0])
        end = int(parts[1])
        fresh_ranges.append((start, end))

    # Parse the available ingredient IDs
    ingredient_ids = []
    for i in range(blank_line_index + 1, len(lines)):
        ingredient_ids.append(int(lines[i]))

    # Count how many ingredient IDs are fresh
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, fresh_ranges):
            fresh_count += 1

    print(f"Number of fresh ingredient IDs: {fresh_count}")


if __name__ == "__main__":
    main()
