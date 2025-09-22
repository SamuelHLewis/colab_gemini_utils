# colab_gemini_utils
## Introduction
This is a guide for working in Google Colab with Gemini. It contains some usage recommendations and workflow guides, and some helper scripts to make switching between a codebase and a colab notebook less painful.

## Gemini in Colab vs Code Assistant CLIs
### Similarities
Gemini in Colab shares many features with using code assistants in their CLIs (e.g. Claude Code etc):
* Model directly edits code
* Code changes are highlighted before edits are applied
* User retains control of command execution
* Reasoning explained and to-do list produced for complex tasks
* Codebase rules (styling, preferred unit test framework etc) can be set, albeit manually for each session
### Differences
However, there are some things that CLI code assistants can do but Gemini in Colab cannot:
* No direct reading and editing of files. Instead, code must be copied in and out of a Colab notebook
* No autonomous running of bash commands e.g. launching UIs
* No imports of screenshots
* No automatic mechanism to set a system prompt
* No memory of previous coding sessions
* No guarantee of edits being applied to an existing chunk of text

# Usage Tips
## Enforcing Coding Standards
To enforce a set of standards for styling, infrastructure etc, follow this process:
1. Write your standards into a markdown file. An example file is in `prompts/gemini_colab_prompt.md`
2. When you launch a new Colab session, create a markdown cell at the top
3. Copy the contents of that markdown file into it
4. As your first prompt to Gemini, tell it to read the cell. For example, use the prompt:

        The Gemini System Prompt cell holds the rules that I want you to follow. Confirm that you understand them, and ask about any ambiguous rules.
5. Check Gemini's response, and clarify any ambiguities that it has highlighted.

Your standards are now in the context for that coding session. However, this is not a guarantee that they will always be followed, so continue to check Gemini's outputs.
