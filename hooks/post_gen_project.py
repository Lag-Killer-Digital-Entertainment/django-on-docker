from pathlib import Path


ignore_path = Path(".gitignore")


with ignore_path.open("a") as gitignore:
    gitignore.write("\n.env*\n")
