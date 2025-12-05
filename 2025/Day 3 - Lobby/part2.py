def find_max_joltage(bank):
    """
    Find the maximum joltage by selecting exactly 12 batteries from the bank.

    This is equivalent to removing exactly (len(bank) - 12) batteries to maximize
    the resulting number. We use a monotonic stack algorithm.

    Args:
        bank: A string of digits representing a battery bank

    Returns:
        The maximum joltage (12-digit number) possible from this bank
    """
    k = len(bank) - 12  # Number of digits to remove
    stack = []
    to_remove = k

    for digit in bank:
        # While we can still remove digits and current digit is larger than stack top
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # If we still need to remove digits, remove from the end
    while to_remove > 0:
        stack.pop()
        to_remove -= 1

    # Convert to integer
    result = ''.join(stack)
    return int(result)


def main():
    """
    Read the input file and display the maximum joltage for each bank.
    Part 2: Each bank now produces a 12-digit joltage number.
    """
    try:
        with open('input.txt', 'r') as file:
            banks = [line.strip() for line in file if line.strip()]

        print("Part 2 - Maximum joltage (12 batteries) for each bank:")
        print("=" * 80)

        total_joltage = 0
        for i, bank in enumerate(banks, 1):
            max_joltage = find_max_joltage(bank)
            total_joltage += max_joltage
            print(f"Bank {i}: {max_joltage}")

        print("=" * 80)
        print(f"Total banks processed: {len(banks)}")
        print(f"Total output joltage: {total_joltage}")

    except FileNotFoundError:
        print("Error: input.txt file not found!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
