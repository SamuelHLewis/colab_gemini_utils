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
## Differences
However, there are some things that CLI code assistants can do but Gemini in Colab cannot:
* No direct reading and editing of files. Instead, code must be copied in and out of a Colab notebook
* No autonomous running of bash commands e.g. launching UIs
* No imports of screenshots
* No automatic mechanism to set a system prompt
* No memory of previous coding sessions
* No guarantee of edits being applied to an existing chunk of text