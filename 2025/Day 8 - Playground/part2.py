"""
Part 2 solution for Day 8 - Playground

Reads `input.txt` from the same directory, parses 3D coordinates (X,Y,Z) one per line,
sorts all pairwise distances (Euclidean, squared distances used for comparisons),
then connects pairs in increasing distance order until all points are in a single
connected component. When the final union that makes the whole set connected occurs,
prints the product of the X coordinates of the two points that were just connected.

If input has fewer than 2 points, prints 0.
"""

import os
from collections import Counter


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        self.count -= 1
        return True


def load_points(path):
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("``") or line.startswith("//"):
                continue
            parts = line.split(",")
            if len(parts) != 3:
                continue
            try:
                x, y, z = map(int, parts)
            except ValueError:
                continue
            pts.append((x, y, z))
    return pts


def main():
    base = os.path.dirname(__file__)
    input_path = os.path.join(base, "input.txt")
    if not os.path.exists(input_path):
        print(f"input.txt not found at {input_path}")
        return

    points = load_points(input_path)
    n = len(points)
    if n < 2:
        print(0)
        return

    # build all edges
    edges = []
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i + 1, n):
            xj, yj, zj = points[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            d2 = dx * dx + dy * dy + dz * dz
            edges.append((d2, i, j))

    # sort edges by distance
    edges.sort()

    uf = UnionFind(n)

    last_pair = None
    for d2, i, j in edges:
        if uf.union(i, j):
            # this union decreased component count
            last_pair = (i, j)
            if uf.count == 1:
                # found the final union that connects all points
                xi = points[i][0]
                xj = points[j][0]
                print(xi * xj)
                return

    # If we finished and never reached a single component (shouldn't happen), print 0
    print(0)


if __name__ == "__main__":
    main()

