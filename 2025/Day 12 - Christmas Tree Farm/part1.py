#!/usr/bin/env python3

import sys
from collections import defaultdict

def parse_input(filename):
    """Parse the input file into shapes and regions"""
    with open(filename, 'r') as f:
        content = f.read().strip()

    # Split into shapes and regions sections
    # Find where shapes end and regions begin
    lines = content.split('\n')
    shapes_section_lines = []
    regions_section_lines = []

    in_shapes = True
    for line in lines:
        if line.strip() == '':
            continue
        if in_shapes and ':' in line and line.split(':')[0].strip().isdigit():
            # This is a shape definition
            shapes_section_lines.append(line)
        elif in_shapes and (line.startswith('#') or line.startswith('.')):
            # This is shape data
            shapes_section_lines.append(line)
        elif 'x' in line and ':' in line:
            # This looks like a region definition
            in_shapes = False
            regions_section_lines.append(line)
        elif not in_shapes:
            regions_section_lines.append(line)

    shapes_section = '\n'.join(shapes_section_lines)
    regions_section = '\n'.join(regions_section_lines)

    # Parse shapes
    shapes = {}
    shape_lines = shapes_section.split('\n')
    current_shape = None
    current_shape_data = []

    for line in shape_lines:
        if ':' in line:
            if current_shape is not None:
                shapes[current_shape] = current_shape_data
            current_shape = int(line.split(':')[0])
            current_shape_data = []
        elif line.strip():
            current_shape_data.append(line.strip())

    if current_shape is not None:
        shapes[current_shape] = current_shape_data

    # Parse regions
    regions = []
    for line in regions_section.split('\n'):
        if line.strip():
            parts = line.split(':')
            if len(parts) != 2:
                print(f"Skipping malformed line: {line}")
                continue

            size_part = parts[0].strip()
            counts_part = parts[1].strip()

            # Parse size
            if 'x' not in size_part:
                print(f"Skipping line with invalid size format: {line}")
                continue

            width, height = map(int, size_part.split('x'))

            # Parse counts
            counts = list(map(int, counts_part.split()))

            regions.append((width, height, counts))

    return shapes, regions

def get_shape_variations(shape_data):
    """Generate all possible rotations and flips of a shape"""
    variations = set()

    # Original shape
    original = tuple(shape_data)
    variations.add(original)

    # Generate all rotations (0, 90, 180, 270 degrees)
    for _ in range(3):
        # Rotate 90 degrees clockwise
        rotated = list(zip(*original[::-1]))
        rotated = [''.join(row) for row in rotated]
        original = tuple(rotated)
        variations.add(original)

    # Generate flipped versions
    flipped_original = tuple(line[::-1] for line in shape_data)
    variations.add(flipped_original)

    # Generate rotations of flipped version
    flipped = flipped_original
    for _ in range(3):
        # Rotate 90 degrees clockwise
        rotated = list(zip(*flipped[::-1]))
        rotated = [''.join(row) for row in rotated]
        flipped = tuple(rotated)
        variations.add(flipped)

    return list(variations)

def can_fit_presents(shapes, region_width, region_height, counts):
    """Check if all presents can fit in the region"""
    # This is a simplified approach - the actual problem is NP-hard
    # For the purpose of this example, we'll use a greedy approach

    # Calculate total area needed
    total_area = 0
    for shape_idx, count in enumerate(counts):
        if count > 0:
            shape_data = shapes[shape_idx]
            shape_area = sum(row.count('#') for row in shape_data)
            total_area += shape_area * count

    # Calculate region area
    region_area = region_width * region_height

    # Simple check: if total present area exceeds region area, it's impossible
    if total_area > region_area:
        return False

    # More sophisticated check would be needed for actual solution
    # This is a placeholder - the real solution would involve backtracking
    # or other spatial arrangement algorithms

    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python part1.py <input_file>")
        return

    input_file = sys.argv[1]
    shapes, regions = parse_input(input_file)

    # Precompute all shape variations
    shape_variations = {}
    for shape_idx, shape_data in shapes.items():
        shape_variations[shape_idx] = get_shape_variations(shape_data)

    print(f"Found {len(shapes)} shapes and {len(regions)} regions")

    # Check each region
    fitting_regions = 0

    for i, (width, height, counts) in enumerate(regions):
        if can_fit_presents(shapes, width, height, counts):
            fitting_regions += 1
            print(f"Region {i+1} ({width}x{height}): Fits")
        else:
            print(f"Region {i+1} ({width}x{height}): Does not fit")

    print(f"\nTotal regions that fit: {fitting_regions}")

if __name__ == "__main__":
    main()