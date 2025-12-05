def merge_ranges(ranges):
    """Merge overlapping ranges and return a list of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort ranges by start value
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if current range overlaps or is adjacent to the last merged range
        if current_start <= last_end + 1:
            # Merge the ranges by extending the end if necessary
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as a new range
            merged.append((current_start, current_end))

    return merged


def count_fresh_ids(ranges):
    """Count the total number of ingredient IDs covered by the ranges."""
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    return total


def main():
    # Read the input file
    with open('input.txt', 'r') as file:
        lines = file.read().strip().split('\n')

    # Find the blank line that separates ranges from ingredient IDs
    blank_line_index = lines.index('')

    # Parse the fresh ID ranges (only the first section)
    fresh_ranges = []
    for i in range(blank_line_index):
        parts = lines[i].split('-')
        start = int(parts[0])
        end = int(parts[1])
        fresh_ranges.append((start, end))

    # Count the total number of fresh ingredient IDs
    total_fresh = count_fresh_ids(fresh_ranges)

    print(f"Total number of fresh ingredient IDs: {total_fresh}")


if __name__ == "__main__":
    main()
