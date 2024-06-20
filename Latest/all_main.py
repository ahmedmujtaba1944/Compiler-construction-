import re
from lexical_analyzer import tokenize
from syntax_analyzer import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator

Errors = []

def build_symbol_table(tokens):
    symbol_table = {}
    current_data_type = None
    current_name = None
    for token_type, lexeme, line_number, *data_type in tokens:
        current_data_type = data_type[0] if data_type else None
        if token_type == 'VARIABLE':
            current_name = lexeme
            if current_name in symbol_table or current_data_type is None:
                current_name = None
                continue
            symbol_table[current_name] = {
                'token_type': 'VARIABLE',
                'data_type': current_data_type,
                'line_number': line_number,
                'value': None
            }
        elif token_type == 'LITERAL' or token_type == 'CONSTANT':
            if current_name is None:
                continue
            if current_name in symbol_table and symbol_table[current_name]['token_type'] == 'VARIABLE':
                symbol_table[current_name]['value'] = lexeme
            current_name = None
        elif token_type == 'FUNCTION':
            current_name = lexeme
            if current_name in symbol_table:
                continue
            if current_data_type is not None:
                symbol_table[current_name] = {
                    'token_type': 'FUNCTION',
                    'data_type': current_data_type,
                    'line_number': line_number,
                    'value': None
                }

    return symbol_table

def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code

code = read_code_from_file(r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\Latest\code_file.txt')

tokens, errors = tokenize(code)

if errors:
    for error in errors:
        print(error)
else:
    symbol_table = build_symbol_table(tokens)
    parser = Parser(tokens)
    parser.parse()
    
    if parser.errors:
        for error in parser.errors:
            print(error)
    else:
        semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
        semantic_analyzer.analyze()
        
        if semantic_analyzer.errors:
            for error in semantic_analyzer.errors:
                print(error)
        else:
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            with open("output.asm", "w") as f:
                f.write(assembly_code)
