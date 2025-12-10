def calculate_ribbon(l, w, h):
    """Calculate the total ribbon needed for a present.

    Ribbon to wrap: smallest perimeter of any face
    Bow: cubic feet of volume (l * w * h)
    """
    # Smallest perimeter: 2 * min(l+w, w+h, h+l)
    smallest_perimeter = 2 * min(l + w, w + h, h + l)

    # Bow: volume
    bow = l * w * h

    return smallest_perimeter + bow


def main():
    total_ribbon = 0

    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                dimensions = line.split("x")
                l, w, h = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
                total_ribbon += calculate_ribbon(l, w, h)

    print(f"Total feet of ribbon needed: {total_ribbon}")


if __name__ == "__main__":
    main()