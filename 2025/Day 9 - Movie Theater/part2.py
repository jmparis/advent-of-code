import time
from collections import defaultdict

def main():
    start_time = time.time()

    # Read input
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # Parse the red tile coordinates
    red_tiles = []
    for line in lines:
        line = line.strip()
        if line:
            x, y = map(int, line.split(','))
            red_tiles.append((x, y))

    red_set = set(red_tiles)
    n = len(red_tiles)

    print(f"Number of red tiles: {n}")

    # Build segments (horizontal and vertical) between consecutive red tiles
    # The polygon is formed by connecting consecutive red tiles
    h_segments = []  # (y, x_min, x_max) - horizontal segments
    v_segments = []  # (x, y_min, y_max) - vertical segments

    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]

        if y1 == y2:
            # Horizontal segment
            h_segments.append((y1, min(x1, x2), max(x1, x2)))
        elif x1 == x2:
            # Vertical segment
            v_segments.append((x1, min(y1, y2), max(y1, y2)))

    print(f"Horizontal segments: {len(h_segments)}, Vertical segments: {len(v_segments)}")

    # Precompute horizontal segment coverage
    h_coverage = defaultdict(list)
    for seg_y, x_min, x_max in h_segments:
        h_coverage[seg_y].append((x_min, x_max))
    for y in h_coverage:
        h_coverage[y].sort()

    # Precompute vertical segment coverage
    v_coverage = defaultdict(list)
    for seg_x, y_min, y_max in v_segments:
        v_coverage[seg_x].append((y_min, y_max))
    for x in v_coverage:
        v_coverage[x].sort()

    # Sort vertical segments by x for ray casting
    v_segments_sorted = sorted(v_segments, key=lambda s: s[0])

    # Get all unique y values from red tiles
    all_y = sorted(set(y for x, y in red_tiles))
    print(f"Unique y values: {len(all_y)}")

    def is_on_boundary(x, y):
        """Check if point is on any connecting segment between red tiles (boundary)"""
        # Check horizontal segments
        if y in h_coverage:
            for x_min, x_max in h_coverage[y]:
                if x_min <= x <= x_max:
                    return True

        # Check vertical segments
        if x in v_coverage:
            for y_min, y_max in v_coverage[x]:
                if y_min <= y <= y_max:
                    return True

        return False

    def count_crossings_to_right(x, y):
        """Count how many vertical segments are crossed by a ray going right from (x, y)"""
        crossings = 0
        for seg_x, seg_y_min, seg_y_max in v_segments_sorted:
            if seg_x <= x:
                continue
            # Use half-open interval [y_min, y_max) to handle vertices correctly
            if seg_y_min <= y < seg_y_max:
                crossings += 1
        return crossings

    def is_inside_polygon(x, y):
        """Ray casting algorithm to check if point is inside polygon"""
        return count_crossings_to_right(x, y) % 2 == 1

    def is_valid_tile(x, y):
        """Check if tile is red or green (valid for rectangle)"""
        if (x, y) in red_set:
            return True
        if is_on_boundary(x, y):
            return True
        return is_inside_polygon(x, y)

    def get_valid_x_range_for_y(y):
        """
        Get the valid x-ranges (inside or on boundary) for a given y.
        Returns a list of (x_min, x_max) tuples representing valid ranges.
        """
        # Find all vertical segment x-coordinates that span this y
        crossing_x = []
        for seg_x, seg_y_min, seg_y_max in v_segments_sorted:
            # A vertical segment contributes to the boundary at y if y is within its range
            if seg_y_min <= y <= seg_y_max:
                crossing_x.append(seg_x)
        
        crossing_x = sorted(set(crossing_x))
        
        if not crossing_x:
            return []
        
        # Build ranges - the interior is between pairs of crossings (odd-even rule)
        # For a simple polygon, we alternate between inside and outside
        ranges = []
        
        # Check each pair of consecutive crossings
        for i in range(len(crossing_x) - 1):
            x_left = crossing_x[i]
            x_right = crossing_x[i + 1]
            
            # Check if the midpoint is inside the polygon
            mid_x = (x_left + x_right) // 2
            if is_inside_polygon(mid_x, y) or is_on_boundary(mid_x, y):
                ranges.append((x_left, x_right))
        
        # Merge overlapping/adjacent ranges
        if not ranges:
            return []
        
        ranges.sort()
        merged = [list(ranges[0])]
        for r in ranges[1:]:
            if r[0] <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], r[1])
            else:
                merged.append(list(r))
        
        return [tuple(r) for r in merged]

    # Precompute valid ranges for all y values in red tiles
    print("Precomputing valid x-ranges for each y...")
    valid_ranges_cache = {}
    for y in all_y:
        valid_ranges_cache[y] = get_valid_x_range_for_y(y)

    def is_x_range_valid_for_y(y, x_min, x_max):
        """Check if the entire x range [x_min, x_max] is valid for given y"""
        if y in valid_ranges_cache:
            ranges = valid_ranges_cache[y]
        else:
            ranges = get_valid_x_range_for_y(y)
        
        for r_min, r_max in ranges:
            if r_min <= x_min and x_max <= r_max:
                return True
        return False

    def check_rectangle_valid(x1, y1, x2, y2):
        """Check if rectangle is valid - all tiles must be red or green"""
        min_x_r = min(x1, x2)
        max_x_r = max(x1, x2)
        min_y_r = min(y1, y2)
        max_y_r = max(y1, y2)

        # Check all y values in the rectangle that are in our red tile y-coordinates
        for y in all_y:
            if min_y_r <= y <= max_y_r:
                if not is_x_range_valid_for_y(y, min_x_r, max_x_r):
                    return False
        
        # For y values between red tile y-coordinates, the valid x-range
        # is determined by the vertical segments that span that y
        # We need to check representative y values between consecutive red tile y-values
        prev_y = None
        for y in all_y:
            if y > max_y_r:
                break
            if y >= min_y_r:
                if prev_y is not None and prev_y >= min_y_r:
                    # Check a representative y value between prev_y and y
                    test_y = prev_y + 1
                    if test_y < y and min_y_r <= test_y <= max_y_r:
                        if not is_x_range_valid_for_y(test_y, min_x_r, max_x_r):
                            return False
            prev_y = y
        
        return True

    # Find the largest valid rectangle
    max_area = 0
    best_rect = None

    # Build pairs sorted by potential area
    print("Building pairs sorted by potential area...")
    
    pairs = []
    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            pairs.append((area, i, j))
    
    # Sort by area descending
    pairs.sort(reverse=True)
    
    print(f"Total pairs: {len(pairs)}")
    print("Checking pairs in order of decreasing potential area...")
    
    checked = 0
    for area, i, j in pairs:
        # Early termination
        if area <= max_area:
            print(f"Early termination at pair {checked}: potential area {area} <= max area {max_area}")
            break
        
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        
        checked += 1
        if checked % 1000 == 0:
            print(f"Checked {checked} pairs, current max area: {max_area}")

        # Check if rectangle is valid
        if check_rectangle_valid(x1, y1, x2, y2):
            if area > max_area:
                max_area = area
                best_rect = (x1, y1, x2, y2)
                print(f"New max area: {max_area} with rectangle corners ({x1},{y1}) and ({x2},{y2})")

    end_time = time.time()
    
    print(f"\n=== RESULT ===")
    print(f"Maximum area: {max_area}")
    if best_rect:
        x1, y1, x2, y2 = best_rect
        print(f"Rectangle corners: ({x1},{y1}) and ({x2},{y2})")
        print(f"Width: {abs(x2-x1)+1}, Height: {abs(y2-y1)+1}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    return max_area

if __name__ == "__main__":
    main()