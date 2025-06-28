# Bloon 🎈

A simple little GUI to make working with LLMs and codebases less of a headache.

Ever get a huge code dump from an LLM and have to manually create every single file and folder? Or wanted to give an LLM your whole project for context without zipping it up?

That's what Bloon is for. It helps you shuttle your code between a **file tree** and a **single Markdown file**, making it way easier to work with Large Language Models.


*(You should probably replace this with your own screenshot!)*

## What's it do?

Bloon has three main jobs:

*   **Deflate:** "Packs" a whole folder of code into one big Markdown file. This is perfect for pasting into an LLM as context.
*   **Inflate:** "Unpacks" that Markdown file and recreates the entire file and folder structure for you. It even `git init`s the folder and commits the new files so you're ready to go.
*   **Apply Patch:** For a more advanced workflow. Give your LLM the "deflated" project, ask for changes as a `unified diff`, and paste the diff into this tab. Bloon will apply the changes to your local code using `git apply`.

## Getting Started

This is a simple Python script, so there's not much to it.

1.  **You'll need:**
    *   Python 3
    *   Tkinter (usually included, but on some Linux distros you might need to install it, e.g., `sudo apt-get install python3-tk`)
    *   `git` installed and available in your PATH.

2.  **Save the code** as something like `bloon.py`.

3.  **Run it** from your terminal:
    ```bash
    python bloon.py
    ```

That's it. The GUI should pop up, and you can start inflating and deflating your projects.

## The Magic Format

Bloon uses a simple Markdown structure that's easy for both humans and LLMs to read:

```markdown
## path/to/your/file.py
```python
# Your python code goes here
print("Hello, world!")
```

## another/file.js
```javascript
// Your javascript code
console.log("Hello again!");
```

Simple, right? Now go make your LLM do the boring work for you.
