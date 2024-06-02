# import tkinter as tk
# from tkinter import scrolledtext
# from tkinter import ttk

# # Assuming your lexical_Analyzer, Syntax_Analyzer, and Semantic_Analyzer are imported
# from LexicalAnalyzer import tokenize
# from SyntaxAnalyzer import Parser
# from SemanticAnalyzer import SemanticAnalyzer
# from AllMain import build_symbol_table

# class CodeAnalyzerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("AA Language")
        
#         style = ttk.Style()
#         style.theme_use('alt')  # Change to 'alt' theme for a more modern look
        
#         # Customize button colors and add shadow effect to sidebar
#         style.configure('TButton', 
#                         foreground='white', 
#                         background='#007acc', 
#                         font=('Helvetica', 10, 'bold'))
#         style.configure('Sidebar.TFrame', background='#2f353a', borderwidth=2, relief='raised')
#         style.configure('Sidebar.TLabel', background='#2f353a', foreground='white', font=('Helvetica', 12, 'bold'))

#         # Create a frame for the sidebar
#         sidebar_frame = ttk.Frame(self.root, style='Sidebar.TFrame', padding="10 10 10 10")
#         sidebar_frame.grid(row=0, column=0, sticky=(tk.N, tk.S))

#         # Create a frame for the main content area
#         mainframe = ttk.Frame(self.root, padding="10 10 10 10")
#         mainframe.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

#         self.root.columnconfigure(1, weight=1)
#         self.root.rowconfigure(0, weight=1)
        
#         # Add buttons to the sidebar
#         self.run_button = ttk.Button(sidebar_frame, text="Run", command=self.run_analysis, style='TButton')
#         self.run_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

#         self.tokens_button = ttk.Button(sidebar_frame, text="Show Tokens", command=self.show_tokens, style='TButton')
#         self.tokens_button.grid(row=1, column=0, padx=10, pady=10, sticky='w')

#         self.symbol_table_button = ttk.Button(sidebar_frame, text="Show Symbol Table", command=self.show_symbol_table, style='TButton')
#         self.symbol_table_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

#         # Label as placeholder for code editor
#         self.placeholder_label = tk.Label(mainframe, text="Enter code here...", fg='grey')
#         self.placeholder_label.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

#         # Text widget for code editor
#         self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30)
#         self.code_editor.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
#         self.code_editor.bind("<FocusIn>", self.remove_placeholder)
#         self.code_editor.bind("<FocusOut>", self.add_placeholder)

#         # Text widget for results (hidden by default)
#         self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=10, height=10)
#         self.results_display.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

#         self.add_placeholder()

#     def add_placeholder(self, event=None):
#         if not self.code_editor.get("1.0", tk.END).strip():
#             self.placeholder_label.lift(self.code_editor)

#     def remove_placeholder(self, event=None):
#         self.placeholder_label.lower(self.code_editor)

#     def run_analysis(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)
        
#         parser = Parser(tokens)
#         parser.parse()
#         errors.extend(parser.errors)
        
#         semantic = SemanticAnalyzer(symbol_table, tokens)
#         semantic.analyze()
#         errors.extend(semantic.errors)

#         self.results_display.delete("1.0", tk.END)
#         if errors:
#             self.show_errors_popup(errors)
#         else:
#             self.results_display.insert(tk.END, 'No Errors were found\n')

#     def show_errors_popup(self, errors):
#         error_window = tk.Toplevel(self.root)
#         error_window.title("Errors")
#         error_text = scrolledtext.ScrolledText(error_window, wrap=tk.WORD, width=80, height=30)
#         error_text.pack(padx=10, pady=10)
#         for error in errors:
#             error_text.insert(tk.END, error + '\n')

#     def show_tokens(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)

#         tokens_str = "\n".join([f"{token}" for token in tokens])

#         token_window = tk.Toplevel(self.root)
#         token_window.title("Tokens")
#         token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30)
#         token_text.pack(padx=10, pady=10)
#         token_text.insert(tk.END, tokens_str)

#     def show_symbol_table(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)

#         symbol_table_str = "\n".join([f"{lexeme}: {info}" for lexeme, info in symbol_table.items()])

#         symbol_table_window = tk.Toplevel(self.root)
#         symbol_table_window.title("Symbol Table")
#         symbol_table_text = scrolledtext.ScrolledText(symbol_table_window, wrap=tk.WORD, width=80, height=30)
#         symbol_table_text.pack(padx=10, pady=10)
#         symbol_table_text.insert(tk.END, symbol_table_str)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CodeAnalyzerApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from ttkthemes import ThemedTk
from LexicalAnalyzer import tokenize
from SyntaxAnalyzer import Parser
from SemanticAnalyzer import SemanticAnalyzer
from AllMain import build_symbol_table
from CodeGenerator import CodeGenerator

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Analyzer")

        # Apply the Equilux theme
        self.root.set_theme('equilux')

        # Create a frame for better layout management
        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Heading for code editor
        self.code_editor_label = ttk.Label(mainframe, text="Code Editor")
        self.code_editor_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.code_editor.grid(row=1, column=0, padx=10, pady=5)

        # Heading for results display
        self.results_display_label = ttk.Label(mainframe, text="Output")
        self.results_display_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.results_display.grid(row=1, column=1, padx=10, pady=5)

        # Run button
        self.run_button = ttk.Button(mainframe, text="Run", style='Run.TButton', command=self.run_analysis)
        self.run_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Show Tokens button
        self.tokens_button = ttk.Button(mainframe, text="Show Tokens", command=self.show_tokens,)
        self.tokens_button.grid(row=2, column=1, padx=5, pady=10, sticky='w')

        # Show Symbol Table button
        self.symbol_table_button = ttk.Button(mainframe, text="Show Symbol Table", command=self.show_symbol_table,)
        self.symbol_table_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

    def run_analysis(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table = build_symbol_table(tokens)
        
        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)
        
        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)

        self.results_display.delete("1.0", tk.END)
        if errors:
            self.results_display.config(foreground='red')
            for error in errors:
                self.results_display.insert(tk.END, error + '\n')
        else:
            self.results_display.config(foreground='green')
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            self.results_display.insert(tk.END, assembly_code)

    def show_tokens(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)

        tokens_str = "\n".join([f"{token}" for token in tokens])

        token_window = tk.Toplevel(self.root)
        token_window.title("Tokens")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, tokens_str)

    def show_symbol_table(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table = build_symbol_table(tokens)

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

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CodeAnalyzerApp(root)
    root.mainloop()