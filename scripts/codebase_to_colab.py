import sys
import json
import argparse
import traceback
from pathlib import Path

def create_notebook_from_codebase(codebase_path, output_notebook_path, gemini_prompt_path):
    """
    Convert a Python codebase to a Colab notebook with each file as a separate cell.
    
    Args:
        codebase_path (str): Path to the codebase directory
        output_notebook_path (str): Path where the notebook will be saved
        gemini_prompt_path (str): Path to a markdown file holding the system prompt for gemini
    """
    
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
    codebase_filepaths = [f for f in codebase_path.rglob('*') if f.is_file()]
    
    # remove any files that are irrelevant or sensitive
    with open('colab.ignore', 'r') as f:
        colab_ignore = f.read()
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

# Invoke with user inputs from CLI
def main():
    parser = argparse.ArgumentParser(
        description="Convert a Python codebase to a Colab notebook"
    )
    parser.add_argument(
        '--codebase_path',
        dest='codebase_path',
        help='Path to the codebase directory'
    )
    parser.add_argument(
        '--output_notebook',
        dest='output_notebook',
        help='Output notebook filename (e.g., notebook.ipynb)'
    )
    parser.add_argument(
        '--gemini_prompt_path',
        dest="gemini_prompt_path",
        required=False,
        help="Path to a markdown file containing the system prompt for gemini"
    )
    args = parser.parse_args()

    # Validate paths
    codebase_path = Path(args.codebase_path)
    if not codebase_path.exists():
        print(f"❌ Error: Codebase path '{codebase_path}' does not exist")
        return 1
    if not codebase_path.is_dir():
        print(f"❌ Error: '{codebase_path}' is not a directory")
        return 1
    
    # Ensure output has .ipynb extension
    output_path = Path(args.output_notebook)
    if output_path.suffix.lower() != '.ipynb':
        output_path = output_path.with_suffix('.ipynb')
        print(f"📝 Note: Added .ipynb extension. Output will be: {output_path}")

    if args.gemini_prompt_path:
        gemini_prompt_path = Path(args.gemini_prompt_path)
        if not codebase_path.exists():
            print(f"❌ Error: Gemini prompt path '{gemini_prompt_path}' does not exist")
            return 1
    
    try:
        create_notebook_from_codebase(
            codebase_path=str(codebase_path),
            output_notebook_path=str(output_path),
            gemini_prompt_path=args.gemini_prompt_path
        )
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return 1
    
if __name__ == "__main__":
    sys.exit(main())