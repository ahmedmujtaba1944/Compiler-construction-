import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from lexical_analyzer import tokenize
from syntax_analyzer import Parser
from semantic_analyzer import SemanticAnalyzer
from all_main import build_symbol_table
from code_generator import CodeGenerator
from code_executor import AssemblyInterpreter

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A++ Language")
        
        # Set the main frame with light blue background
        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create left frame for buttons
        left_frame = ttk.Frame(mainframe, width=200, padding="10 10 10 10", style="Left.TFrame")
        left_frame.grid(row=0, column=0, sticky="ns")
        
        # Create center frame for code editor
        center_frame = ttk.Frame(mainframe, padding="10 10 10 10", style="Center.TFrame")
        center_frame.grid(row=0, column=1, sticky="nsew")
        mainframe.grid_columnconfigure(1, weight=1)
        
        # Create right frame for results display
        right_frame = ttk.Frame(mainframe, padding="10 10 10 10", style="Right.TFrame")
        right_frame.grid(row=0, column=2, sticky="ns")
        mainframe.grid_columnconfigure(2, weight=1)
        
        # Set background colors
        self.style = ttk.Style()
        self.style.configure("Left.TFrame", background="white")
        self.style.configure("Center.TFrame", background="white")
        self.style.configure("Right.TFrame", background="white")
        self.style.configure("TLabel", background="white")
        self.style.configure("TButton", background="white")

        # Buttons on side navbar
        image = Image.open("run_btn.png")
        image = image.resize((25, 25))
        self.run_button_image = ImageTk.PhotoImage(image)
        button_width = 20  # Width for all buttons

        self.run_button = ttk.Button(left_frame, text="Run", width=button_width, compound=tk.RIGHT, command=self.run_analysis)
        self.run_button.pack(fill=tk.X, pady=5)

        self.tokens_button = ttk.Button(left_frame, text="Tokens", command=self.show_tokens, width=button_width)
        self.tokens_button.pack(fill=tk.X, pady=5)

        self.symbol_table_button = ttk.Button(left_frame, text="Symbol Table", command=self.show_symbol_table, width=button_width)
        self.symbol_table_button.pack(fill=tk.X, pady=5)

        self.assembly_button = ttk.Button(left_frame, text="Assembly", command=self.show_assembly, width=button_width)
        self.assembly_button.pack(fill=tk.X, pady=5)


        self.clear_button = ttk.Button(left_frame, text="Clear code", command=self.clear_fields, width=button_width)
        self.clear_button.pack(fill=tk.X, pady=5)
        
        # Heading for code editor
        self.code_editor_label = ttk.Label(center_frame, text="Code", font=('Arial', 12))
        self.code_editor_label.pack(anchor=tk.W)

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(center_frame, wrap=tk.WORD, width=40, height=30, background='white', foreground='black', insertbackground='black')
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        self.code_editor.focus()
        
        # Heading for results display
        self.results_display_label = ttk.Label(right_frame, text="Output", font=('Arial', 12))
        self.results_display_label.pack(anchor=tk.W)

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=30, background='white', foreground='black', insertbackground='black', font=('Arial', 13))
        self.results_display.pack(fill=tk.BOTH, expand=True)

    def run_analysis(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            self.results_display.delete("1.0", tk.END)
            self.results_display.config(foreground='red')
            self.results_display.insert(tk.END, "Error: Your Code editor is empty. Please enter some code.")
            return

        tokens, errors = tokenize(code)
        symbol_table, symbol_table_errors = build_symbol_table(tokens)
        errors.extend(symbol_table_errors)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)

        self.results_display.delete("1.0", tk.END)
        if errors:
            errors = set(errors)
            self.results_display.config(foreground='red')
            for error in errors:
                self.results_display.insert(tk.END, error + '\n')
        else:
            self.results_display.config(foreground='green')
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            interpreter = AssemblyInterpreter()
            interpreter.execute(assembly_code)
            code = interpreter.debug()
            code_str = "\n".join(f"{key}: {value}" for key, value in code.items())
            self.results_display.insert(tk.END, code_str)

    def show_assembly(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table, er = build_symbol_table(tokens)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)
        code_generator = CodeGenerator(symbol_table, tokens)
        assembly_code = code_generator.generate()

        token_window = tk.Toplevel(self.root)
        token_window.title("Assembly Language")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, assembly_code)

    def show_tokens(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)

        tokens_str = "\n".join([f"{token}" for token in tokens])

        token_window = tk.Toplevel(self.root)
        token_window.title("Tokens")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, tokens_str)

    def update_symbol_table(self, symbol_table, interpreter_variables):
        for var_name, value in interpreter_variables.items():
            if var_name in symbol_table:
                symbol_table[var_name]['value'] = value
        return symbol_table

    def show_symbol_table(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table, symbol_table_errors = build_symbol_table(tokens)
        errors.extend(symbol_table_errors)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
        semantic_analyzer.analyze()
        errors.extend(semantic_analyzer.errors)

        if errors:
            for error in errors:
                print(error)
        else:
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            interpreter = AssemblyInterpreter()
            interpreter.execute(assembly_code)
            symbol_table = self.update_symbol_table(symbol_table, interpreter.debug())
            symbol_table_window = tk.Toplevel(self.root)
            symbol_table_window.title("Symbol Table")
            columns = ('Lexeme', 'Token Type', 'Data Type', 'Line Number', 'Value')
            tree = ttk.Treeview(symbol_table_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor='center', width=100)

            for lexeme, info in symbol_table.items():
                tree.insert('', tk.END, values=(lexeme, info['token_type'], info['data_type'], info['line_number'], info['value']))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def clear_fields(self):
        self.code_editor.delete("1.0", tk.END)
        self.results_display.delete("1.0", tk.END)
        self.results_display.config(foreground='black')


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = CodeAnalyzerApp(root)
    root.geometry("1200x700")  # Set a default window size
    root.mainloop()
