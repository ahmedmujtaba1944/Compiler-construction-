#all_main.py
import re
from lexical_analyzer import tokenize
from syntax_analyzer import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator

Errors = []

# Function to build the symbol table
def build_symbol_table(tokens):
    symbol_table = {}
    current_data_type = None
    current_name = None
    error = []
    for token_type, lexeme, line_number, *data_type in tokens:
        
        current_data_type = data_type[0] if data_type else None
        if token_type == 'VARIABLE':
            current_name = lexeme
            if current_data_type == None:
                current_name = None
                continue
            symbol_table[current_name] = {
                'token_type': 'VARIABLE',
                'data_type': current_data_type,
                'line_number': line_number,
                'value': None  
            }
        elif token_type == 'LITERAL' or token_type == 'CONSTANT':
            if current_name is None or current_name not in symbol_table:
                continue
            
            if symbol_table[current_name]['token_type'] == 'VARIABLE':
                symbol_table[current_name]['value'] = lexeme
            current_name = None  # Reset current_name after assigning value
        elif token_type == 'FUNCTION':
            current_name = lexeme
            if current_name in symbol_table:
                continue
            data_type = data_type[0] if data_type else None
            if data_type != None:
                symbol_table[current_name] = {
                    'token_type': 'FUNCTION',
                    'data_type': data_type,
                    'line_number': line_number,
                    'value': None  
                }   

    return symbol_table, error

# Read code from a file
def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code

# Use a raw string or forward slashes for the file path
# file_path = r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Last_day_a++\code_file.txt'
file_path = r'D:\Study\BScs 8th Semester(Final)\Compiler Construction(CC)\CC\Another\code_file.txt'
# Alternatively, you could use forward slashes:
# file_path = 'G:/University_Study/8th Semester/Compiler-construction/Last_Day/Last_day_a++/code.txt'

code = read_code_from_file(file_path)

# Tokenize the code
tokens, errors = tokenize(code)
Errors.extend(errors)

# Build the symbol table
symbol_table, symbol_table_errors = build_symbol_table(tokens)
Errors.extend(symbol_table_errors)

# Parse the code
parser = Parser(tokens)
parser.parse()
Errors.extend(parser.errors)

# Analyze semantics
semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
semantic_analyzer.analyze()
Errors.extend(semantic_analyzer.errors)

if Errors:
    for error in Errors:
        print(error)
else:
    # Generate assembly code
    code_generator = CodeGenerator(symbol_table, tokens)
    assembly_code = code_generator.generate()
    with open("output.asm", "w") as f:
        f.write(assembly_code)
