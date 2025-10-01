import nbformat
import sys
import argparse
from src.utils import extract_file_code_pairs, write_file_with_confirmation

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Colab notebook to a Python codebase"
    )
    parser.add_argument(
        '--notebook_path',
        dest='notebook_path',
        help='Path to the notebook to be converted to a codebase'
    )
    args = parser.parse_args()

    try:
        with open(args.notebook_path, 'r') as f:
            notebook_contents = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"Error: Notebook file not found at '{args.notebook_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading notebook: {e}")
        sys.exit(1)


    file_code_pairs = extract_file_code_pairs(notebook_contents)

    for filepath, code in file_code_pairs:
        write_file_with_confirmation(filepath, code)

    print("Code extraction and saving process finished.")

if __name__ == "__main__":
    main()