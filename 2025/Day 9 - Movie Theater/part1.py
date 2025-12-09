with open('input.txt', 'r') as f:
    lines = f.readlines()

# Parse the red tile coordinates
red_tiles = []
for line in lines:
    line = line.strip()
    if line:
        x, y = map(int, line.split(','))
        red_tiles.append((x, y))

# Find the largest rectangle using two red tiles as opposite corners
max_area = 0

for i in range(len(red_tiles)):
    for j in range(i + 1, len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]

        # Calculate the area of the rectangle with opposite corners at (x1, y1) and (x2, y2)
        # The rectangle dimensions are inclusive of both corners
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height

        max_area = max(max_area, area)

print(max_area)

