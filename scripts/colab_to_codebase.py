import nbformat
import re
import os
import sys
import argparse

def write_file_with_confirmation(filepath, code):
    if os.path.exists(filepath):
        # Ask for confirmation before overwriting using command line input
        response = input(f"File '{filepath}' already exists. Overwrite? (yes/no): ").lower()
        if response == 'yes':
            write_file(filepath, code)
        else:
            print(f"Skipped writing to '{filepath}'.")
    else:
        # If file doesn't exist, just write it
        write_file(filepath, code)


def write_file(filepath, code):
    # Create directories if they don't exist
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Save the code to the file
    with open(filepath, 'w') as f:
        f.write(code)
    print(f"Successfully wrote to '{filepath}'.")

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
            notebook_object = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"Error: Notebook file not found at '{args.notebook_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading notebook: {e}")
        sys.exit(1)


    file_code_pairs = []
    current_filepath = None

    for cell in notebook_object.cells:
        if cell.cell_type == 'markdown':
            # Look for a markdown cell that seems to contain a file path
            match = re.search(r'##\s*📁\s*(.*)', cell.source)
            if match:
                current_filepath = match.group(1).strip()
                current_filepath = re.sub(r'\`', '', current_filepath)
            else:
                current_filepath = None # Reset if the markdown cell doesn't match the pattern
        elif cell.cell_type == 'code' and current_filepath:
            # If the previous cell was a file path markdown and this is a code cell
            file_code_pairs.append((current_filepath, cell.source))
            current_filepath = None # Reset after pairing

    if not file_code_pairs:
        print("No file path and code pairs found in the notebook.")
        sys.exit(0)

    for filepath, code in file_code_pairs:
        write_file_with_confirmation(filepath, code)

    print("Code extraction and saving process finished.")

if __name__ == "__main__":
    main()