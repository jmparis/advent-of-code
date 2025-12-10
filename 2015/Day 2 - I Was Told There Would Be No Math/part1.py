def calculate_wrapping_paper(l, w, h):
    """Calculate the total wrapping paper needed for a present.
    
    Surface area: 2*l*w + 2*w*h + 2*h*l
    Plus extra: area of the smallest side
    """
    side1 = l * w
    side2 = w * h
    side3 = h * l
    
    surface_area = 2 * side1 + 2 * side2 + 2 * side3
    smallest_side = min(side1, side2, side3)
    
    return surface_area + smallest_side


def main():
    total_paper = 0
    
    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                dimensions = line.split("x")
                l, w, h = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
                total_paper += calculate_wrapping_paper(l, w, h)
    
    print(f"Total square feet of wrapping paper needed: {total_paper}")


if __name__ == "__main__":
    main()