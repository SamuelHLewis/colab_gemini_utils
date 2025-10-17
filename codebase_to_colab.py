import sys
import argparse
import traceback
from pathlib import Path
from utils import create_notebook_from_codebase

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
    parser.add_argument(
        '--ignore',
        dest='ignore_list',
        nargs='*',  # Allows zero or more arguments
        default=[], # Default to an empty list if no arguments are provided
        help='List of files or directories to ignore (space-separated)'
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
            gemini_prompt_path=args.gemini_prompt_path,
            ignore_list=args.ignore_list
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