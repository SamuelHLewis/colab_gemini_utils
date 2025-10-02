# Colab Gemini Utils

## Introduction
This is a guide for working in Google Colab with Gemini. It contains some usage recommendations and workflow guides, and some helper scripts to make switching between a codebase and a colab notebook less painful.

**NOTE:** You should use Gemini and Google Colab through a Google account that is suitable for the task at hand. Don't use your personal account for work projects, and don't use your work account for personal projects.

### Gemini in Colab vs Code Assistant CLIs

#### Similarities
Gemini in Colab shares many features with using code assistants in their CLIs (e.g. Claude Code etc):
* Model directly edits code
* Code changes are highlighted before edits are applied
* User retains control of command execution
* Reasoning explained and to-do list produced for complex tasks
* Codebase rules (styling, preferred unit test framework etc) can be set, albeit manually for each session

#### Differences
However, there are some things that CLI code assistants can do but Gemini in Colab cannot:
* No direct reading and editing of files. Instead, code must be copied in and out of a Colab notebook (but see the Workflow Guide for a workaround)
* No automatic mechanism to set a system prompt (but see Usage Tips for a workaround)
* No autonomous running of bash commands e.g. launching UIs
* No memory of previous coding sessions

## Workflow Guide
The main source of friction when using Gemini in Colab is in copying your code into a Colab notebook at the start, and copying it out again at the end. To make this easier, there are helper scripts in this repo that automate this process.

### Installation
Use poetry to install the requirements for the helper scripts:
```bash
poetry install --no-root
```
If you don't have poetry already, follow [these instructions](https://python-poetry.org/docs/#installation) to install it.

### Importing code into Colab with `codebase_to_colab.py`
`scripts/codebase_to_colab.py` copies each file in your codebase to a code cell in a jupyter notebook, and writes the name of each file to a markdown cell above its contents. A demo codebase is supplied in the `demo` folder to demonstrate this. You can run the script on the demo repo as follows:
```bash
python ./scripts/codebase_to_colab.py --codebase_path=./demo --output_notebook=codebase.ipynb --gemini_prompt_path=./prompts/example_prompt.md
```
This will generate a notebook called `codebase.ipynb`, which you can then upload to Google Drive and start working in Colab with Gemini.
**NOTE** if the above command doesn't work, you may have to invoke it with python3 instead:
```bash
python3 ./scripts/codebase_to_colab.py --codebase_path=./demo --output_notebook=codebase.ipynb --gemini_prompt_path=./prompts/example_prompt.md
```

**NOTE:** this script ignores any files that are in the `colab.ignore` file. If you have secrets, API keys, IP addresses etc that you do not want to copy out of your codebase, add them to `colab.ignore` and they will be skipped.

### Exporting code out of Colab with `colab_to_codebase.py`
`colab_to_codebase.py` reconstructs your codebase from a colab notebook. It does this by extracting the pairs of markdown cell - code cell from your colab notebook, and writing each to a file, where the file name is what was specified in the markdown cell, and the file contents are what was in the corresponding code cell. You can run the script to reconstruct the demo repo as follows:
```bash
python ./scripts/colab_to_codebase.py --notebook_path codebase.ipynb
```
This will recreate the entire directory from the contents of the colab notebook, asking for confirmation before a pre-existing file is overwritten. Git will pick up any changes, and they can be committed to your repo in the standard way.

## Usage Tips

### Enforcing Coding Standards
To enforce a set of standards for styling, infrastructure etc, follow this process:
1. When you launch a new Colab session, write your standards into a markdown cell at the top
    * if you are using `scripts/codebase_to_colab.py`, this will be done for you if you save your prompt to a markdown file and specify it with `--gemini_prompt_path`
2. As your first prompt to Gemini, tell it to read the cell. For example, use the prompt:

        The Gemini System Prompt cell holds the rules that I want you to follow. Confirm that you understand them, and ask about any ambiguous rules.
3. Check Gemini's response, and clarify any ambiguities that it has highlighted.

Your standards are now in the context for that coding session. However, this is not a guarantee that they will always be followed, so continue to check Gemini's outputs.

### Complex Tasks
If you ask Gemini to generate a complicated piece of code, it will usually write a plan beforehand and ask you to confirm each step as it writes the corresponding code. This allows you to redirect it to modify its plan, but sometimes it will stall and not continue on to the next step. If this happens, you can usually get it to move on to the next step by saying something like:
```
Continue with your plan
```