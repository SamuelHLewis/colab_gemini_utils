import os
import re
import json
from pathlib import Path

def create_notebook_from_codebase(codebase_path, output_notebook_path, gemini_prompt_path):
    """
    Convert a Python codebase to a Colab notebook with each file as a separate cell.

    Args:
        codebase_path (str): Path to the codebase directory
        output_notebook_path (str): Path where the notebook will be saved
        gemini_prompt_path (str): Path to a markdown file holding the system prompt for gemini
    """

    # remove output notebook if it already exists, to prevent recursive listing of a notebook within the notebook of a codebase
    output_notebook_path = Path(output_notebook_path)
    output_notebook_path.unlink(missing_ok=True)

    # Initialize notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "colab": {
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

    # Get all Python files recursively
    codebase_path = Path(codebase_path)
    # note: files here have paths already
    codebase_filepaths = [f for f in codebase_path.rglob('*')
                          if f.is_file()
                          and not str(f).startswith('.git')
                          and not str(f).startswith('.pytest_cache')]

    # regardless of where the script has been called from, read colab.ignore from the same dir as this script 
    script_dir = Path(__file__).parent 
    with open(script_dir / 'colab.ignore', 'r') as f:
        colab_ignore = f.read()
    # remove any files that are irrelevant or sensitive
    filtered_filepaths = []
    for filepath in codebase_filepaths:
        if filepath.name not in colab_ignore:
            filtered_filepaths.append(filepath)

    # Sort files for consistent ordering
    filtered_filepaths.sort()

    # Add Gemini system prompt if given
    if gemini_prompt_path:
        with open(gemini_prompt_path, 'r', encoding='utf-8') as f:
            gemini_prompt = f.read()
        gemini_prompt_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"{gemini_prompt}\n",
            ]
        }
        notebook["cells"].append(gemini_prompt_cell)

    # Process each file
    for filepath in filtered_filepaths:
        try:
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Create markdown cell with filename
            markdown_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"## 📁 `{filepath}`\n"
                ]
            }

            # Create code cell with file content
            code_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": content.splitlines(keepends=True) if content else [""]
            }

            # Add cells to notebook
            notebook["cells"].append(markdown_cell)
            notebook["cells"].append(code_cell)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            continue

    # Save notebook
    try:
        with open(output_notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        print(f"✅ Notebook saved successfully to: {output_notebook_path}")
        print(f"📊 Total cells created: {len(notebook['cells'])}")

    except Exception as e:
        print(f"❌ Error saving notebook: {e}")

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

def extract_file_code_pairs(notebook_contents: dict):
    """
    Extracts pairs of filenames and code contents from a notebook dictionary.
    Note: it is assumed that the notebook structure alternates between markdown cells with the filename
    and code cells with the code contained in that file

    Args:
        notebook_contents (dict): The contents of a notebook, as loaded from a JSON file.
    """
    file_code_pairs = []
    current_filepath = None

    for cell in notebook_contents.get('cells', []):  # Use .get() to safely access 'cells'
        if cell.get('cell_type') == 'markdown':  # Use .get() to safely access 'cell_type'
            # Look for a markdown cell that seems to contain a file path
            source = ''.join(cell.get('source', [])) # Use .get() and join list of strings
            match = re.search(r'##\s*📁\s*(.*)', source)
            if match:
                current_filepath = match.group(1).strip()
                current_filepath = re.sub(r'\`', '', current_filepath)
            else:
                current_filepath = None # Reset if the markdown cell doesn't match the pattern
        elif cell.get('cell_type') == 'code' and current_filepath: # Use .get() to safely access 'cell_type'
            # If the previous cell was a file path markdown and this is a code cell
            code_content = ''.join(cell.get('source', [])) # Use .get() and join list of strings
            file_code_pairs.append((current_filepath, code_content))
            current_filepath = None # Reset after pairing

    if not file_code_pairs:
        print("No file path and code pairs found in the notebook.")
        # Decide how to handle this case - maybe return an empty list or raise an error
        return [] # Returning an empty list for now
    else:
        return file_code_pairs
