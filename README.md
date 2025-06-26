# bLoon

A simple Python Tkinter application that parses a Markdown file containing header + code-block pairs and creates a corresponding file tree structure on disk.

---

## Features

- Pick a Markdown file and an (empty) target directory via a GUI  
- Parses headers (`# …` through `###### …`) as file paths  
- Extracts the following fenced code block as file content  
- Automatically creates nested directories  
- Real-time progress logging and visual feedback  
- Cross-platform (Windows, macOS, Linux)  
- No external dependencies—uses only the Python standard library  

---

## Table of Contents

1. [Getting Started](#getting-started)  
2. [Usage](#usage)  
3. [Markdown File Format](#markdown-file-format)  
4. [Implementation Details](#implementation-details)  
5. [License](#license)  

---

## Getting Started

### Prerequisites

- Python 3.6+ (includes `tkinter`, `re`, `pathlib`, `os`)  

### Installation

1. Clone this repository or download the script.  
2. Ensure the file is named `markdown_to_files.py`.

```bash
git clone https://github.com/yourusername/markdown-to-file-tree.git
cd markdown-to-file-tree
```

---

## Usage

1. Run the application:

   ```bash
   python markdown_to_files.py
   ```

2. In the GUI:

   - **Markdown File**: Click **Browse** and select your `.md` file.  
   - **Target Directory**: Click **Browse** and choose an *empty* directory (it will refuse a non-empty directory).  
   - Click **Convert** to start parsing and file creation.  

3. Watch the **Progress** log and **Progress Bar** for real-time feedback.  
4. On completion, you’ll get a popup indicating how many files were created.

---

## Markdown File Format

The converter expects your Markdown to contain pairs of:

1. A header (`#`, `##`, …, `######`) whose text is treated as a relative file path.  
2. A fenced code block immediately following the header, whose contents become the file’s content.

Example:

```markdown
## src/app.js
```javascript
console.log("Hello, world!");
```

### components/Button.tsx
```typescript
export const Button = () => <button>Click me</button>;
```

##### utils/helpers.py
```python
def greet(name):
    return f"Hello, {name}!"
```
```

- Header levels (1–6) are all supported.  
- Language specifier (e.g., ```javascript) is ignored in output.  

---

## Implementation Details

- **GUI**: Built with `tkinter` and `ttk` for cross-platform look and feel.  
- **Parsing**: Uses a single regex (`re.MULTILINE | re.DOTALL`) to locate `header → code block` pairs.  
- **File System**:  
  - Checks that the target directory is empty or non-existent.  
  - Creates nested directories via `pathlib.Path.mkdir(parents=True, exist_ok=True)`.  
- **Robustness**:  
  - Continues on individual file write errors, logs failures.  
  - Displays popups on critical errors or when no valid pairs are found.  
- **Progress Feedback**:  
  - Scrollable text area for detailed logs.  
  - Indeterminate progress bar during conversion.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
