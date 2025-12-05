# Advent of Code 2015 - Day 1: Not Quite Lisp (Part 2)
# Trouver la position du premier caractère qui fait entrer le Père Noël au sous-sol (étage -1)
import os

def main():
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r") as f:
        instructions = f.read().strip()
    floor = 0
    for i, c in enumerate(instructions, start=1):
        if c == '(':  # Monter d'un étage
            floor += 1
        elif c == ')':  # Descendre d'un étage
            floor -= 1
        if floor == -1:
            print(f"Position du premier caractère qui fait entrer au sous-sol : {i}")
            return
    print("Le Père Noël n'est jamais entré au sous-sol.")

if __name__ == "__main__":
    main()

