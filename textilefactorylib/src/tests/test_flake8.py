import subprocess
import sys

def run_flake8(library_path):
    try:
        result = subprocess.run(
            ['flake8', library_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Flake8 analysis passed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Flake8 analysis failed:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

if __name__ == '__main__':
    library_path = '*/textilefactorylib'  # Replace with the path to your library
    run_flake8(library_path)