# Advent of Code 2015 - Day 1: Not Quite Lisp (Part 1)
# Résolution de l'énigme selon les instructions du README-part1.md
import os

def main():
    # Chemin absolu du fichier input.txt pour éviter FileNotFoundError
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r") as f:
        instructions = f.read().strip()
    floor = 0
    for c in instructions:
        if c == '(':  # Monter d'un étage
            floor += 1
        elif c == ')':  # Descendre d'un étage
            floor -= 1
    print(f"Étage final atteint par le Père Noël : {floor}")

if __name__ == "__main__":
    main()
