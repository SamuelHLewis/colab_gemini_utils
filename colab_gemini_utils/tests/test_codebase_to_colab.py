from src.utils import extract_file_code_pairs

def test_extract_file_code_pairs_with_demo_notebook():
    """
    Test that extract_file_code_pairs correctly extracts file-code pairs
    from a demo notebook.
    """
    # Create a dummy notebook resembling the output of codebase_to_colab
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": "## 📁 `demo/main.py`\n"
            },
            {
                "cell_type": "code",
                "source": "from utils.formatting import print_util\nfrom utils.maths import add_util\n\ntotal = add_util(1, 1)\nprint_util(total)\n"
            },
            {
                "cell_type": "markdown",
                "source": "## 📁 `demo/utils/formatting.py`\n"
            },
            {
                "cell_type": "code",
                "source": "def print_util(user_input):\n    print(user_input)\n    return\n"
            },
            {
                "cell_type": "markdown",
                "source": "## 📁 `demo/utils/maths.py`\n"
            },
            {
                "cell_type": "code",
                "source": "def add_util(num1, num2):\n    sum = num1 + num2\n    return sum\n"
            }
        ],
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

    extracted_pairs = extract_file_code_pairs(notebook_content)

    # Define the expected output
    expected_pairs = [
        ("demo/main.py", "from utils.formatting import print_util\nfrom utils.maths import add_util\n\ntotal = add_util(1, 1)\nprint_util(total)\n"),
        ("demo/utils/formatting.py", "def print_util(user_input):\n    print(user_input)\n    return\n"),
        ("demo/utils/maths.py", "def add_util(num1, num2):\n    sum = num1 + num2\n    return sum\n")
    ]

    # Assert that the extracted pairs match the expected pairs
    assert extracted_pairs == expected_pairs