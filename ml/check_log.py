from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "access.log"

with open(file_path, "r") as f:
    for i in range(10):
        print(f.readline())