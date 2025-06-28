#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import re
import subprocess
import tempfile
from pathlib import Path

class MarkdownInflaterDeflater:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloon")
        self.root.geometry("800x600")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_inflate_tab()
        self.create_deflate_tab()
        #self.create_patch_tab()
        
    def create_inflate_tab(self):
        inflate_frame = ttk.Frame(self.notebook)
        self.notebook.add(inflate_frame, text="Inflate")
        
        # Input selection frame
        input_frame = ttk.LabelFrame(inflate_frame, text="Input", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        self.inflate_input_var = tk.StringVar(value="file")
        ttk.Radiobutton(input_frame, text="Markdown File", variable=self.inflate_input_var, 
                       value="file", command=self.toggle_inflate_input).pack(anchor='w')
        ttk.Radiobutton(input_frame, text="Paste Markdown", variable=self.inflate_input_var, 
                       value="paste", command=self.toggle_inflate_input).pack(anchor='w')
        
        # File selection
        self.file_frame = ttk.Frame(input_frame)
        self.file_frame.pack(fill='x', pady=5)
        
        self.inflate_file_var = tk.StringVar()
        ttk.Label(self.file_frame, text="Markdown File:").pack(side='left')
        ttk.Entry(self.file_frame, textvariable=self.inflate_file_var, width=50).pack(side='left', padx=5)
        ttk.Button(self.file_frame, text="Browse", 
                  command=lambda: self.browse_file(self.inflate_file_var, [("Markdown", "*.md")])).pack(side='left')
        
        # Text area for pasting
        self.paste_frame = ttk.Frame(input_frame)
        ttk.Label(self.paste_frame, text="Paste Markdown:").pack(anchor='w')
        self.inflate_text = scrolledtext.ScrolledText(self.paste_frame, height=15, width=70)
        self.inflate_text.pack(fill='both', expand=True)
        
        # Output folder selection
        output_frame = ttk.Frame(inflate_frame)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        self.inflate_output_var = tk.StringVar()
        ttk.Label(output_frame, text="Output Folder:").pack(side='left')
        ttk.Entry(output_frame, textvariable=self.inflate_output_var, width=50).pack(side='left', padx=5)
        ttk.Button(output_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.inflate_output_var)).pack(side='left')
        
        # Run button
        ttk.Button(inflate_frame, text="Run Inflate", command=self.run_inflate).pack(pady=10)
        
        # Initialize visibility
        self.toggle_inflate_input()
        
    def create_deflate_tab(self):
        deflate_frame = ttk.Frame(self.notebook)
        self.notebook.add(deflate_frame, text="Deflate")
        
        # Source folder selection
        source_frame = ttk.Frame(deflate_frame)
        source_frame.pack(fill='x', padx=10, pady=10)
        
        self.deflate_source_var = tk.StringVar()
        ttk.Label(source_frame, text="Source Folder:").pack(side='left')
        ttk.Entry(source_frame, textvariable=self.deflate_source_var, width=50).pack(side='left', padx=5)
        ttk.Button(source_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.deflate_source_var)).pack(side='left')
        
        # Target file selection
        target_frame = ttk.Frame(deflate_frame)
        target_frame.pack(fill='x', padx=10, pady=5)
        
        self.deflate_target_var = tk.StringVar()
        ttk.Label(target_frame, text="Target .md File:").pack(side='left')
        ttk.Entry(target_frame, textvariable=self.deflate_target_var, width=50).pack(side='left', padx=5)
        ttk.Button(target_frame, text="Browse", 
                  command=lambda: self.browse_save_file(self.deflate_target_var, [("Markdown", "*.md")])).pack(side='left')
        
        # Run button
        ttk.Button(deflate_frame, text="Run Deflate", command=self.run_deflate).pack(pady=10)
        
    def create_patch_tab(self):
        patch_frame = ttk.Frame(self.notebook)
        self.notebook.add(patch_frame, text="Apply Patch")
        
        # Instructions
        instructions_frame = ttk.LabelFrame(patch_frame, text="LLM Instructions", padding=10)
        instructions_frame.pack(fill='x', padx=10, pady=10)
        
        instructions_text = tk.Text(instructions_frame, height=6, width=70, wrap='word')
        instructions_text.pack(fill='x')
        instructions_text.insert('1.0', '''How to ask your LLM for a unified diff:

Output only a standard unified diff with changes.

Do not include any explanatory text—emit only the diff itself.''')
        instructions_text.config(state='disabled')
        
        # Input selection
        input_frame = ttk.LabelFrame(patch_frame, text="Patch Input", padding=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.patch_input_var = tk.StringVar(value="paste")
        ttk.Radiobutton(input_frame, text="Paste Diff", variable=self.patch_input_var, 
                       value="paste", command=self.toggle_patch_input).pack(anchor='w')
        ttk.Radiobutton(input_frame, text="Patch File", variable=self.patch_input_var, 
                       value="file", command=self.toggle_patch_input).pack(anchor='w')
        
        # File selection
        self.patch_file_frame = ttk.Frame(input_frame)
        self.patch_file_frame.pack(fill='x', pady=5)
        
        self.patch_file_var = tk.StringVar()
        ttk.Label(self.patch_file_frame, text="Patch File:").pack(side='left')
        ttk.Entry(self.patch_file_frame, textvariable=self.patch_file_var, width=50).pack(side='left', padx=5)
        ttk.Button(self.patch_file_frame, text="Browse", 
                  command=lambda: self.browse_file(self.patch_file_var, [("Patch", "*.patch"), ("All", "*.*")])).pack(side='left')
        
        # Text area for pasting
        self.patch_paste_frame = ttk.Frame(input_frame)
        self.patch_paste_frame.pack(fill='both', expand=True, pady=5)
        ttk.Label(self.patch_paste_frame, text="Paste Unified Diff:").pack(anchor='w')
        self.patch_text = scrolledtext.ScrolledText(self.patch_paste_frame, height=10, width=70)
        self.patch_text.pack(fill='both', expand=True)
        
        # Run button
        ttk.Button(patch_frame, text="Run Patch", command=self.run_patch).pack(pady=10)
        
        # Initialize visibility
        self.toggle_patch_input()
        
    def toggle_inflate_input(self):
        if self.inflate_input_var.get() == "file":
            self.file_frame.pack(fill='x', pady=5)
            self.paste_frame.pack_forget()
        else:
            self.file_frame.pack_forget()
            self.paste_frame.pack(fill='both', expand=True, pady=5)
            
    def toggle_patch_input(self):
        if self.patch_input_var.get() == "file":
            self.patch_file_frame.pack(fill='x', pady=5)
            self.patch_paste_frame.pack_forget()
        else:
            self.patch_file_frame.pack_forget()
            self.patch_paste_frame.pack(fill='both', expand=True, pady=5)
            
    def browse_file(self, var, filetypes):
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            var.set(filename)
            
    def browse_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)
            
    def browse_save_file(self, var, filetypes):
        filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".md")
        if filename:
            var.set(filename)
            
    def run_command(self, cmd, cwd=None):
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
            
    def get_language_from_extension(self, filename):
        """Map file extensions to markdown language identifiers"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'objc',
            '.mm': 'objcpp',
            '.pl': 'perl',
            '.sh': 'bash',
            '.bat': 'batch',
            '.ps1': 'powershell',
            '.html': 'html',
            '.htm': 'html',
            '.xml': 'xml',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.conf': 'conf',
            '.sql': 'sql',
            '.md': 'markdown',
            '.tex': 'latex',
            '.dockerfile': 'dockerfile',
            '.makefile': 'makefile',
            '.cmake': 'cmake',
            '.vim': 'vim',
            '.lua': 'lua',
            '.dart': 'dart',
            '.elm': 'elm',
            '.clj': 'clojure',
            '.ex': 'elixir',
            '.exs': 'elixir',
            '.erl': 'erlang',
            '.hrl': 'erlang',
            '.fs': 'fsharp',
            '.fsi': 'fsharp',
            '.fsx': 'fsharp',
            '.ml': 'ocaml',
            '.mli': 'ocaml',
            '.pas': 'pascal',
            '.pp': 'pascal',
            '.hs': 'haskell',
            '.lhs': 'haskell',
            '.jl': 'julia',
            '.nim': 'nim',
            '.nims': 'nim',
            '.cr': 'crystal',
            '.d': 'd',
            '.zig': 'zig',
            '.v': 'v',
            '.vhd': 'vhdl',
            '.vhdl': 'vhdl',
            '.sv': 'systemverilog',
            '.svh': 'systemverilog',
            '.asm': 'asm',
            '.s': 'asm',
            '.proto': 'protobuf',
            '.graphql': 'graphql',
            '.gql': 'graphql',
            '.sol': 'solidity',
            '.tf': 'hcl',
            '.tfvars': 'hcl',
            '.feature': 'gherkin',
            '.ipynb': 'jupyter',
            '.pug': 'pug',
            '.jade': 'jade',
            '.styl': 'stylus',
            '.coffee': 'coffeescript',
            '.litcoffee': 'coffeescript',
            '.vue': 'vue',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.svelte': 'svelte',
            '.prisma': 'prisma',
            '.gradle': 'gradle',
            '.groovy': 'groovy',
            '.gvy': 'groovy',
            '.kt': 'kotlin',
            '.kts': 'kotlin',
            '.matlab': 'matlab',
            '.octave': 'octave',
            '.rmd': 'rmarkdown',
            '.qmd': 'quarto',
            '.rst': 'restructuredtext',
            '.asciidoc': 'asciidoc',
            '.adoc': 'asciidoc',
            '.org': 'org',
            '.nix': 'nix',
            '.dhall': 'dhall',
            '.purs': 'purescript',
            '.idr': 'idris',
            '.agda': 'agda',
            '.lean': 'lean',
            '.coq': 'coq',
            '.vb': 'vbnet',
            '.vbs': 'vbscript',
            '.ahk': 'autohotkey',
            '.au3': 'autoit',
            '.applescript': 'applescript',
            '.scpt': 'applescript',
            '.ps': 'postscript',
            '.eps': 'postscript',
            '.f': 'fortran',
            '.for': 'fortran',
            '.f90': 'fortran',
            '.f95': 'fortran',
            '.cob': 'cobol',
            '.cbl': 'cobol',
            '.ada': 'ada',
            '.adb': 'ada',
            '.ads': 'ada',
            '.lisp': 'lisp',
            '.lsp': 'lisp',
            '.cl': 'commonlisp',
            '.el': 'elisp',
            '.scm': 'scheme',
            '.rkt': 'racket',
            '.tcl': 'tcl',
            '.awk': 'awk',
            '.sed': 'sed',
        }
        
        # Get extension
        path = Path(filename)
        ext = path.suffix.lower()
        
        # Check if it's a known dotfile
        if path.name.lower() == 'dockerfile':
            return 'dockerfile'
        elif path.name.lower() == 'makefile':
            return 'makefile'
        elif path.name.lower().startswith('.'):
            # For dotfiles, try to identify by name
            if 'bash' in path.name or 'profile' in path.name:
                return 'bash'
            elif 'gitignore' in path.name or 'gitconfig' in path.name:
                return 'gitconfig'
            elif 'vimrc' in path.name:
                return 'vim'
            elif 'zsh' in path.name:
                return 'zsh'
        
        # Return mapped extension or empty string for unknown
        return ext_map.get(ext, '')
            
    def run_inflate(self):
        # Get input
        if self.inflate_input_var.get() == "file":
            md_file = self.inflate_file_var.get()
            if not md_file or not os.path.exists(md_file):
                messagebox.showerror("Error", "Please select a valid Markdown file")
                return
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = self.inflate_text.get('1.0', 'end-1c')
            if not content.strip():
                messagebox.showerror("Error", "Please paste Markdown content")
                return
                
        output_folder = self.inflate_output_var.get()
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder")
            return
            
        try:
            # Create output folder if needed
            os.makedirs(output_folder, exist_ok=True)
            
            # Initialize git if not already
            git_dir = os.path.join(output_folder, '.git')
            if not os.path.exists(git_dir):
                success, msg = self.run_command('git init', cwd=output_folder)
                if not success:
                    messagebox.showerror("Git Error", f"Failed to initialize git:\n{msg}")
                    return
                    
                # Commit empty state
                success, msg = self.run_command('git commit --allow-empty -m "Initial empty state"', cwd=output_folder)
                if not success:
                    messagebox.showerror("Git Error", f"Failed to create initial commit:\n{msg}")
                    return
                    
            # Parse markdown sections
            sections = re.findall(r'## (.*?)\n```(\w*)\n(.*?)\n```', content, re.DOTALL)
            
            if not sections:
                messagebox.showwarning("Warning", "No code sections found in the Markdown")
                return
                
            # Process each section
            for filepath, language, code in sections:
                filepath = filepath.strip()
                full_path = os.path.join(output_folder, filepath)
                
                # Create directories
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Write or append to file
                mode = 'a' if os.path.exists(full_path) else 'w'
                with open(full_path, mode, encoding='utf-8') as f:
                    f.write(code)
                    if mode == 'a' and not code.endswith('\n'):
                        f.write('\n')
                        
            # Git add and commit
            success, msg = self.run_command('git add .', cwd=output_folder)
            if not success:
                messagebox.showerror("Git Error", f"Failed to add files:\n{msg}")
                return
                
            success, msg = self.run_command('git commit -m "Inflate from Markdown"', cwd=output_folder)
            if not success:
                messagebox.showwarning("Warning", f"Git commit failed (possibly no changes):\n{msg}")
            else:
                messagebox.showinfo("Success", f"Successfully inflated {len(sections)} file(s)")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            
    def run_deflate(self):
        source_folder = self.deflate_source_var.get()
        if not source_folder or not os.path.exists(source_folder):
            messagebox.showerror("Error", "Please select a valid source folder")
            return
            
        target_file = self.deflate_target_var.get()
        if not target_file:
            messagebox.showerror("Error", "Please specify a target .md file")
            return
            
        try:
            content = []
            file_count = 0
            
            # Walk directory tree
            for root, dirs, files in os.walk(source_folder):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    # Skip hidden files and binary files
                    if file.startswith('.'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, source_folder)
                    
                    # Skip binary files (basic check)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                    except:
                        continue
                        
                    # Determine language from extension
                    language = self.get_language_from_extension(file)
                    
                    # Add to content
                    content.append(f"## {relative_path}")
                    content.append(f"```{language}")
                    content.append(file_content.rstrip())
                    content.append("```")
                    content.append("")  # Empty line between sections
                    
                    file_count += 1
                    
            if file_count == 0:
                messagebox.showwarning("Warning", "No text files found in the source folder")
                return
                
            # Write to target file
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
                
            messagebox.showinfo("Success", f"Successfully deflated {file_count} file(s) to {target_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            
    def run_patch(self):
        # Get patch content
        if self.patch_input_var.get() == "file":
            patch_file = self.patch_file_var.get()
            if not patch_file or not os.path.exists(patch_file):
                messagebox.showerror("Error", "Please select a valid patch file")
                return
            with open(patch_file, 'r', encoding='utf-8') as f:
                patch_content = f.read()
        else:
            patch_content = self.patch_text.get('1.0', 'end-1c')
            if not patch_content.strip():
                messagebox.showerror("Error", "Please paste a unified diff")
                return
                
        try:
            # Check if we're in a git repository
            success, msg = self.run_command('git rev-parse --git-dir')
            if not success:
                messagebox.showerror("Error", "Not in a git repository. Please run from within a git repository.")
                return
                
            # Create temporary patch file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False, encoding='utf-8') as f:
                f.write(patch_content)
                temp_patch = f.name
                
            try:
                # Apply patch using git apply
                success, msg = self.run_command(f'git apply --3way "{temp_patch}"')
                
                if success:
                    messagebox.showinfo("Success", "Patch applied successfully")
                else:
                    # Try without 3way if it fails
                    success, msg = self.run_command(f'git apply "{temp_patch}"')
                    if success:
                        messagebox.showinfo("Success", "Patch applied successfully")
                    else:
                        messagebox.showerror("Error", f"Failed to apply patch:\n{msg}")
            finally:
                # Clean up temp file
                os.unlink(temp_patch)
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = tk.Tk()
    app = MarkdownInflaterDeflater(root)
    root.mainloop()

if __name__ == "__main__":
    main()