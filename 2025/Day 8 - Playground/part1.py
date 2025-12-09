"""
Part 1 solution for Day 8 - Playground

Reads `input.txt` from the same directory, parses 3D coordinates (X,Y,Z) one per line,
finds the 1000 pairs of junction boxes which are closest together (by Euclidean distance),
connects those pairs (adds edges between them) and then computes the sizes of all
connected components. Prints the product of the sizes of the three largest components.

This script is robust to empty lines and ignores malformed lines.
"""

import os
import heapq
from collections import Counter


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

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
        return True


def load_points(path):
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Skip lines that are code fences or comments
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


def k_smallest_edges(points, k):
    # Compute all pairwise squared distances and return k smallest edges as (dist, i, j)
    n = len(points)
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
    if k >= len(edges):
        edges.sort()
        return edges
    # use heapq.nsmallest for efficiency
    return heapq.nsmallest(k, edges)


def main():
    base = os.path.dirname(__file__)
    input_path = os.path.join(base, "input.txt")
    if not os.path.exists(input_path):
        print(f"input.txt not found at {input_path}")
        return

    points = load_points(input_path)
    n = len(points)
    if n == 0:
        print("No points loaded.")
        return

    K = 1000
    # number of possible pairs
    max_pairs = n * (n - 1) // 2
    k = min(K, max_pairs)

    edges = k_smallest_edges(points, k)

    uf = UnionFind(n)
    # Connect the selected k pairs (even if union doesn't change components)
    for d2, i, j in edges:
        uf.union(i, j)

    # Count component sizes
    roots = [uf.find(i) for i in range(n)]
    ctr = Counter(roots)
    sizes = sorted(ctr.values(), reverse=True)

    # Take top 3 sizes
    top3 = sizes[:3]
    # If fewer than 3 components, multiply what's available
    prod = 1
    for s in top3:
        prod *= s

    print(prod)


if __name__ == "__main__":
    main()

