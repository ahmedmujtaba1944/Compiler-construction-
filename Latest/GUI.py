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

        self.root.set_theme('equilux')

        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Heading for code editor
        self.code_editor_label = ttk.Label(mainframe, text="Code Here ...", font=('Arial', 14))
        self.code_editor_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=80, height=20, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.code_editor.grid(row=1, column=0, padx=10, pady=5)
        self.code_editor.focus()
        # Heading for results display
        self.results_display_label = ttk.Label(mainframe, text="Output", font=('Arial', 12))
        self.results_display_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=80, height=5, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.results_display.grid(row=4, column=0, padx=10, pady=5)

        # image = Image.open("run_btn.png")  
        # image = image.resize((25, 25))  
        # self.run_button_image = ImageTk.PhotoImage(image)

        # Run button with image
        self.run_button = ttk.Button(mainframe, text="Run", compound=tk.RIGHT, command=self.run_analysis)
        self.run_button.grid(row=0, column=0, sticky='e')
        # self.run_button = ttk.Button(mainframe, text="Run", command=self.run_analysis)
        # self.run_button.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.run_button = ttk.Button(mainframe, text="Assembly Code", command=self.show_assembly)
        self.run_button.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        # Show Tokens button
        self.tokens_button = ttk.Button(mainframe, text="Show Tokens", command=self.show_tokens,)
        self.tokens_button.grid(row=2, column=0, padx=5, pady=10, sticky='w')

        # Show Symbol Table button
        self.symbol_table_button = ttk.Button(mainframe, text="Show Symbol Table", command=self.show_symbol_table,)
        self.symbol_table_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

    def run_analysis(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            self.results_display.delete("1.0", tk.END)
            self.results_display.config(foreground='red')
            self.results_display.insert(tk.END, "Error: Code editor is empty. Please enter some code.")

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
        symbol_table = build_symbol_table(tokens)
        
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
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, assembly_code)

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

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# import tkinter as tk
# from tkinter import scrolledtext, Menu, Frame, Label, Button, PhotoImage
# from tkinter import ttk
# from ttkthemes import ThemedTk
# from PIL import Image, ImageTk
# from lexical_analyzer import tokenize
# from syntax_analyzer import Parser
# from semantic_analyzer import SemanticAnalyzer
# from all_main import build_symbol_table
# from code_generator import CodeGenerator
# from code_executor import AssemblyInterpreter

# class CodeAnalyzerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A++ Language Compiler")
#         self.root.geometry("1366x768")
#         self.root.resizable(0, 0)
#         self.root.state('zoomed')
#         self.root.config(background='#eff5f6')

#         self.create_menu_bar()

#         mainframe = ttk.Frame(self.root, padding="10 10 10 10")
#         mainframe.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
#         self.root.columnconfigure(1, weight=1)
#         self.root.rowconfigure(0, weight=1)

#         self.create_sidebar()
#         self.create_toolbar(mainframe)
#         self.create_widgets(mainframe)

#     def create_menu_bar(self):
#         menu_bar = Menu(self.root)
#         self.root.config(menu=menu_bar)

#         file_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="File", menu=file_menu)
#         file_menu.add_command(label="New")
#         file_menu.add_command(label="Open")
#         file_menu.add_command(label="Save")
#         file_menu.add_command(label="Save As")
#         file_menu.add_separator()
#         file_menu.add_command(label="Exit", command=self.root.quit)

#         edit_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="Edit", menu=edit_menu)
#         edit_menu.add_command(label="Undo")
#         edit_menu.add_command(label="Redo")
#         edit_menu.add_separator()
#         edit_menu.add_command(label="Cut")
#         edit_menu.add_command(label="Copy")
#         edit_menu.add_command(label="Paste")

#         run_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="Run", menu=run_menu)
#         run_menu.add_command(label="Run Code", command=self.run_analysis)
#         run_menu.add_command(label="Show Tokens", command=self.show_tokens)
#         run_menu.add_command(label="Show Symbol Table", command=self.show_symbol_table)
#         run_menu.add_command(label="Show Assembly", command=self.show_assembly)

#     def create_sidebar(self):
#         sidebar = Frame(self.root, bg='#ffffff')
#         sidebar.grid(row=0, column=0, sticky='ns')

       
#         self.brandName = Label(sidebar, text='A++ Language', bg='#ffffff', font=("", 15, "bold"))
#         self.brandName.pack()

#         sidebar_icons = [
#             ('Ruc', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\run_icon.png'),
#             ('Tokes', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\tokens.png'),
#             ('SymbleTable', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\symbol_table_icon.png'),
#             ('Assembly', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\assembly_icon.png')
#         ]

#         for text, icon_path in sidebar_icons:
#             self.add_sidebar_button(sidebar, text, icon_path)

#     def add_sidebar_button(self, sidebar, text, icon_path):
#         icon = ImageTk.PhotoImage(Image.open(icon_path).resize((24, 24)))
#         icon_label = Label(sidebar, image=icon, bg='#ffffff')
#         icon_label.image = icon  # Keep a reference to avoid garbage collection
#         icon_label.pack(pady=10)

#         text_button = Button(sidebar, text=text, bg='#ffffff', font=("", 13, "bold"), bd=0, cursor='hand2', activebackground='#ffffff')
#         text_button.pack()

#     def create_toolbar(self, mainframe):
#         toolbar = ttk.Frame(mainframe)
#         toolbar.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

#         run_icon = ImageTk.PhotoImage(Image.open(r"G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\run_icon.png").resize((24, 24)))
#         tokens_icon = ImageTk.PhotoImage(Image.open(r"G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\tokens.png").resize((24, 24)))
#         symbol_table_icon = ImageTk.PhotoImage(Image.open(r"G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\symbol_table_icon.png").resize((24, 24)))
#         assembly_icon = ImageTk.PhotoImage(Image.open(r"G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\assembly_icon.png").resize((24, 24)))

#         self.run_button = ttk.Button(toolbar, image=run_icon, command=self.run_analysis)
#         self.run_button.image = run_icon
#         self.run_button.pack(side=tk.LEFT, padx=2)

#         self.tokens_button = ttk.Button(toolbar, image=tokens_icon, command=self.show_tokens)
#         self.tokens_button.image = tokens_icon
#         self.tokens_button.pack(side=tk.LEFT, padx=2)

#         self.symbol_table_button = ttk.Button(toolbar, image=symbol_table_icon, command=self.show_symbol_table)
#         self.symbol_table_button.image = symbol_table_icon
#         self.symbol_table_button.pack(side=tk.LEFT, padx=2)

#         self.assembly_button = ttk.Button(toolbar, image=assembly_icon, command=self.show_assembly)
#         self.assembly_button.image = assembly_icon
#         self.assembly_button.pack(side=tk.LEFT, padx=2)

#     def create_widgets(self, mainframe):
#         self.code_editor_label = ttk.Label(mainframe, text="Code Here ...", font=('Arial', 14))
#         self.code_editor_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

#         self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=50, height=30, background='white', foreground='black', insertbackground='black')
#         self.code_editor.grid(row=2, column=0, padx=10, pady=5, sticky='ns')
#         self.code_editor.focus()

#         self.results_display_label = ttk.Label(mainframe, text="Output", font=('Arial', 12))
#         self.results_display_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

#         self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=50, height=30, background='white', foreground='black', insertbackground='black')
#         self.results_display.grid(row=2, column=1, padx=10, pady=5, sticky='ns')

#     def run_analysis(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         if not code:
#             self.results_display.delete("1.0", tk.END)
#             self.results_display.config(foreground='red')
#             self.results_display.insert(tk.END, "Error: Code editor is empty. Please enter some code.")
#             return

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
#             errors = set(errors)
#             self.results_display.config(foreground='red')
#             for error in errors:
#                 self.results_display.insert(tk.END, error + '\n')
#         else:
#             self.results_display.config(foreground='green')
#             code_generator = CodeGenerator(symbol_table, tokens)
#             assembly_code = code_generator.generate()
#             interpreter = AssemblyInterpreter()
#             interpreter.execute(assembly_code)
#             code = interpreter.debug()
#             code_str = "\n".join(f"{key}: {value}" for key, value in code.items())
#             self.results_display.insert(tk.END, code_str)

#     def show_assembly(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)
        
#         parser = Parser(tokens)
#         parser.parse()
#         errors.extend(parser.errors)
        
#         semantic = SemanticAnalyzer(symbol_table, tokens)
#         semantic.analyze()
#         errors.extend(semantic.errors)
        
#         code_generator = CodeGenerator(symbol_table, tokens)
#         assembly_code = code_generator.generate()
        
#         token_window = tk.Toplevel(self.root)
#         token_window.title("Assembly Language")
#         token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
#         token_text.pack(padx=10, pady=10)
#         token_text.insert(tk.END, assembly_code)

#     def show_tokens(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)

#         tokens_str = "\n".join([f"{token}" for token in tokens])

#         token_window = tk.Toplevel(self.root)
#         token_window.title("Tokens")
#         token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
#         token_text.pack(padx=10, pady=10)
#         token_text.insert(tk.END, tokens_str)

#     def show_symbol_table(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)

#         symbol_table_window = tk.Toplevel(self.root)
#         symbol_table_window.title("Symbol Table")
#         columns = ('Lexeme', 'Token Type', 'Data Type', 'Line Number', 'Value')
#         tree = ttk.Treeview(symbol_table_window, columns=columns, show='headings')
#         for col in columns:
#             tree.heading(col, text=col)
#             tree.column(col, anchor='center', width=100)

#         for lexeme, info in symbol_table.items():
#             tree.insert('', tk.END, values=(lexeme, info['token_type'], info['data_type'], info['line_number'], info['value']))

#         tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# if __name__ == "__main__":
#     root = ThemedTk(theme="window")
#     app = CodeAnalyzerApp(root)
#     root.mainloop()

# ========================================================================================================================

# import tkinter as tk
# from tkinter import scrolledtext, Menu, Frame, Label, Button, PhotoImage
# from tkinter import ttk
# from ttkthemes import ThemedTk
# from PIL import Image, ImageTk
# from lexical_analyzer import tokenize
# from syntax_analyzer import Parser
# from semantic_analyzer import SemanticAnalyzer
# from all_main import build_symbol_table
# from code_generator import CodeGenerator
# from code_executor import AssemblyInterpreter

# class CodeAnalyzerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A++ Language Compiler")
#         self.root.geometry("1366x768")
#         self.root.resizable(0, 0)
#         self.root.state('zoomed')
#         self.root.config(background='#eff5f6')

#         self.create_menu_bar()

#         mainframe = ttk.Frame(self.root, padding="10 10 10 10")
#         mainframe.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
#         self.root.columnconfigure(1, weight=1)
#         self.root.rowconfigure(0, weight=1)

#         self.create_sidebar()
#         self.create_widgets(mainframe)

#     def create_menu_bar(self):
#         menu_bar = Menu(self.root)
#         self.root.config(menu=menu_bar)

#         file_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="File", menu=file_menu)
#         file_menu.add_command(label="New")
#         file_menu.add_command(label="Open")
#         file_menu.add_command(label="Save")
#         file_menu.add_command(label="Save As")
#         file_menu.add_separator()
#         file_menu.add_command(label="Exit", command=self.root.quit)

#         edit_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="Edit", menu=edit_menu)
#         edit_menu.add_command(label="Undo")
#         edit_menu.add_command(label="Redo")
#         edit_menu.add_separator()
#         edit_menu.add_command(label="Cut")
#         edit_menu.add_command(label="Copy")
#         edit_menu.add_command(label="Paste")

#         run_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="Run", menu=run_menu)
#         run_menu.add_command(label="Run Code", command=self.run_analysis)
#         run_menu.add_command(label="Show Tokens", command=self.show_tokens)
#         run_menu.add_command(label="Show Symbol Table", command=self.show_symbol_table)
#         run_menu.add_command(label="Show Assembly", command=self.show_assembly)

#     def create_sidebar(self):
#         sidebar = Frame(self.root, bg='#ffffff', bd=5, relief='ridge')
#         sidebar.grid(row=0, column=0, sticky='ns')

#         self.brandName = Label(sidebar, text='A++ Language', bg='#ffffff', font=("", 30, "bold"))
#         self.brandName.pack(pady=40)

#         sidebar_icons = [
#             ('Run', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\run_icon.png', self.run_analysis),
#             ('Tokens', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\tokens.png', self.show_tokens),
#             ('Symbol Table', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\symbol_table_icon.png', self.show_symbol_table),
#             ('Assembly', r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\assembly_icon.png', self.show_assembly)
#         ]

#         for text, icon_path, command in sidebar_icons:
#             self.add_sidebar_button(sidebar, text, icon_path, command)

#     def add_sidebar_button(self, sidebar, text, icon_path, command):
#         icon = ImageTk.PhotoImage(Image.open(icon_path).resize((24, 24)))
#         button_frame = Frame(sidebar, bg='#ffffff')
#         button_frame.pack(pady=10, fill='x')

#         icon_label = Label(button_frame, image=icon, bg='#ffffff')
#         icon_label.image = icon  # Keep a reference to avoid garbage collection
#         icon_label.pack(side='left', padx=10)

#         text_button = Button(button_frame, text=text, bg='#ffffff', font=("", 13, "bold"), bd=0, cursor='hand2', activebackground='#ffffff', command=command)
#         text_button.pack(side='left')

#     def create_widgets(self, mainframe):
#         self.code_editor_label = ttk.Label(mainframe, text="main.a++", font=('Arial', 14))
#         self.code_editor_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

#         self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=35, background='white', foreground='black', insertbackground='black')
#         self.code_editor.grid(row=2, column=0, padx=10, pady=5, sticky='ns')
#         self.code_editor.focus()

#         self.results_display_label = ttk.Label(mainframe, text="Output", font=('Arial', 12))
#         self.results_display_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

#         self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=35, background='white', foreground='black', insertbackground='black')
#         self.results_display.grid(row=2, column=1, padx=10, pady=5, sticky='ns')

#     def run_analysis(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         if not code:
#             self.results_display.delete("1.0", tk.END)
#             self.results_display.config(foreground='red')
#             self.results_display.insert(tk.END, "Error: Code editor is empty. Please enter some code.")
#             return

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
#             errors = set(errors)
#             self.results_display.config(foreground='red')
#             for error in errors:
#                 self.results_display.insert(tk.END, error + '\n')
#         else:
#             self.results_display.config(foreground='green')
#             code_generator = CodeGenerator(symbol_table, tokens)
#             assembly_code = code_generator.generate()
#             interpreter = AssemblyInterpreter()
#             interpreter.execute(assembly_code)
#             code = interpreter.debug()
#             code_str = "\n".join(f"{key}: {value}" for key, value in code.items())
#             self.results_display.insert(tk.END, code_str)

#     def show_assembly(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)
        
#         parser = Parser(tokens)
#         parser.parse()
#         errors.extend(parser.errors)
        
#         semantic = SemanticAnalyzer(symbol_table, tokens)
#         semantic.analyze()
#         errors.extend(semantic.errors)
        
#         code_generator = CodeGenerator(symbol_table, tokens)
#         assembly_code = code_generator.generate()
        
#         token_window = tk.Toplevel(self.root)
#         token_window.title("Assembly Language")
#         token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
#         token_text.pack(padx=10, pady=10)
#         token_text.insert(tk.END, assembly_code)

#     def show_tokens(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)

#         tokens_str = "\n".join([f"{token}" for token in tokens])

#         token_window = tk.Toplevel(self.root)
#         token_window.title("Tokens")
#         token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='white', foreground='black', insertbackground='black')
#         token_text.pack(padx=10, pady=10)
#         token_text.insert(tk.END, tokens_str)

#     def show_symbol_table(self):
#         code = self.code_editor.get("1.0", tk.END).strip()
#         tokens, errors = tokenize(code)
#         symbol_table = build_symbol_table(tokens)

#         symbol_table_window = tk.Toplevel(self.root)
#         symbol_table_window.title("Symbol Table")
#         columns = ('Lexeme', 'Token Type', 'Data Type', 'Line Number', 'Value')
#         tree = ttk.Treeview(symbol_table_window, columns=columns, show='headings')
#         for col in columns:
#             tree.heading(col, text=col)
#             tree.column(col, anchor='center', width=100)

#         for lexeme, info in symbol_table.items():
#             tree.insert('', tk.END, values=(lexeme, info['token_type'], info['data_type'], info['line_number'], info['value']))

#         tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# if __name__ == "__main__":
#     root = ThemedTk(theme="window")
#     app = CodeAnalyzerApp(root)
#     root.mainloop()
