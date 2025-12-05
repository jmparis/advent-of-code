def find_max_joltage(bank):
    """
    Find the maximum joltage by selecting any two batteries from the bank.

    Args:
        bank: A string of digits representing a battery bank

    Returns:
        The maximum joltage (two-digit number) possible from this bank
    """
    max_joltage = 0

    # Try all pairs of batteries (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form a two-digit number from positions i and j
            joltage = int(bank[i] + bank[j])
            max_joltage = max(max_joltage, joltage)

    return max_joltage


def main():
    """
    Read the input file and display the maximum joltage for each bank.
    """
    try:
        with open('input.txt', 'r') as file:
            banks = [line.strip() for line in file if line.strip()]

        print("Maximum joltage for each bank:")
        print("-" * 40)

        total_joltage = 0
        for i, bank in enumerate(banks, 1):
            max_joltage = find_max_joltage(bank)
            total_joltage += max_joltage
            print(f"Bank {i} ({bank}): {max_joltage} jolts")

        print("-" * 40)
        print(f"Total banks processed: {len(banks)}")
        print(f"Total output joltage: {total_joltage} jolts")

    except FileNotFoundError:
        print("Error: input.txt file not found!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
