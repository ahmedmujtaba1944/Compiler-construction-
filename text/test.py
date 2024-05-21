import re

# Define token types
token_types = {
    'KEYWORD': r'\b(?:iif|otherwise|then|repeat|rotate|Blank|resume|stop|null)\b',
    'DATA_TYPE': r'\b(?:integer|decimal|line|flag|single)\b',
    'OPERATOR': r'(?:<=|>=|==|!=|\+\+|\-\-|\+|\-|\*|/|<|>|%)',
    'IDENTIFIER': r'\$[_a-zA-Z][_a-zA-Z0-9]*',
    'PROCEDURE': r'\b(?:repeat|rotate)\b',
    'CONSTANT': r'(?:\".*?\"|\'.*?\')',
    'LITERAL': r'\b(?:yes|no|\d+\.\d*|\d+)\b',
    'ASSIGN': r'=',
    'LCURLY': r'{',
    'RCURLY': r'}',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'SEPARATOR': r',',
    'STATEMENT_END': r'\!',
}

# Create regular expressions for tokenization
patterns = {token: re.compile(pattern) for token, pattern in token_types.items()}

def tokenize(code):
    Errors = []
    tokens = []
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        position = 0
        while position < len(line):
            if line[position].isspace():  # Skip whitespace
                position += 1
                continue
            match = None
            for token_type, pattern in token_types.items():
                match = re.match(pattern, line[position:])
                if match:
                    token = match.group(0)
                    if token_type == 'IDENTIFIER':
                        prev_token_index = len(tokens) - 1
                        data_type = None  # Default to None
                        if prev_token_index >= 0 and tokens[prev_token_index][0] == 'DATA_TYPE' or tokens[prev_token_index][1] == 'Blank':
                            data_type = tokens[prev_token_index][1]
                        while position + len(token) < len(line) and line[position + len(token)].isspace():
                            position += 1
                        if position + len(token) < len(line) and line[position + len(token)] == '(':
                            tokens.append(('FUNCTION', token, line_number, data_type))
                        else:
                            tokens.append(('VARIABLE', token, line_number, data_type))
                    else:
                        tokens.append((token_type, token, line_number))
                    position += len(token)
                    break
            if not match:
                Errors.append(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                print(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                position += 1

    return tokens, Errors

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.block_stack = []
        self.errors = []

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def match(self, expected_token_type):
        if self.current_token and self.current_token[0] == expected_token_type:
            self.advance()
        else:
            self.errors.append(f"Syntax error: Expected {expected_token_type}, found {self.current_token[0] if self.current_token else 'EOF'} at line {self.current_token[2]}")

    def parse(self):
        self.program()
        
    def program(self):
        self.statement_list()
        
    def statement_list(self):
        while self.current_token:
            self.statement()
        if self.current_token == None and len(self.block_stack) > 0:
            er = '}'
            self.errors.append(f"Syntax error: Missing {er} of Block at line {self.block_stack[-1][1]}")
                
    def statement(self):
        if self.current_token[0] == 'LCURLY':
            self.block()
        elif self.current_token[0] == 'RCURLY':
            if self.block_stack:
                self.block_stack.pop()
                self.advance()
        elif self.current_token[0] == 'DATA_TYPE':
            self.declaration()
        elif self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ['iif', 'otherwise', 'then']:
                self.conditional_statement()
            elif self.current_token[1] in ['repeat', 'rotate']:
                self.loop_statement()
            elif self.current_token[1] == 'Blank':
                self.function_definition()
            elif self.current_token[1] == 'resume' or self.current_token[1] == 'stop':
                self.advance()
                self.match('STATEMENT_END')
        elif self.current_token[0] == 'FUNCTION':            
            self.function_call()
            self.match('STATEMENT_END')
        elif self.current_token[0] == 'VARIABLE':
            self.assignment()
        elif self.current_token == None:
            pass
        else:
            self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            self.advance()

    def expression(self):
        if self.current_token[0] in ['LITERAL', 'CONSTANT', 'VARIABLE', 'OPERATOR']:
            self.match(self.current_token[0])
            return False
        elif self.current_token[0] == 'FUNCTION':
            self.function_call()
            return True
        else:
            self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            return True

    def declaration(self):
        self.match('DATA_TYPE')
        if self.current_token[0] == 'FUNCTION':
            self.function_definition()
        else:
            self.match('VARIABLE')
            if self.current_token == None:
                self.errors.append('Syntax Error: Missing ! at the end.')
            elif self.current_token[0] == 'STATEMENT_END':
                self.match('STATEMENT_END')
            else:
                self.match('ASSIGN')
                while self.current_token[0] != 'STATEMENT_END':
                    if self.expression():
                        break
                self.match('STATEMENT_END')

    def assignment(self):
        self.match('VARIABLE')
        self.match('ASSIGN')
        while self.current_token[0] != 'STATEMENT_END':
            if self.expression():
                break
        self.match('STATEMENT_END')
        
    def condition(self):
        self.expression()
        self.match('OPERATOR')
        self.expression()

    def conditional_statement(self):
        if self.current_token[1] == 'iif':
            self.match('KEYWORD')
            self.condition()
            self.block()
        elif self.current_token[1] == 'otherwise':
            self.match('KEYWORD')
            self.condition()
            self.block()
        elif self.current_token[1] == 'then':
            self.match('KEYWORD')
            self.block()

    def loop_progression(self):
        if self.current_token[0] == 'VARIABLE':
            self.match('VARIABLE') 
            self.match('OPERATOR')
            if self.current_token[0] == 'VARIABLE':
                self.match('VARIABLE') 
        elif self.current_token[0] == 'OPERATOR':
            self.match('OPERATOR')  
            if self.current_token[0] == 'LITERAL':
                self.match('LITERAL')  
            elif self.current_token[0] == 'VARIABLE':
                self.match('VARIABLE')  
            else:
                self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
        else:
            self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")

    def loop_statement(self):
        if self.current_token[1] == 'repeat':
            self.match('KEYWORD')
            self.match('LPAREN')
            self.declaration()
            self.condition()
            self.match('STATEMENT_END')
            self.loop_progression()
            self.match('RPAREN')
            self.block()
        elif self.current_token[1] == 'rotate':
            self.match('KEYWORD')
            self.match('LPAREN')
            self.condition()
            self.match('RPAREN')
            self.block()

    def argument_list(self):  
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] == 'DATA_TYPE':
                self.match(self.current_token[0])
                if self.current_token[0] == 'VARIABLE':
                    self.match('VARIABLE')
                    if self.current_token[0] != 'RPAREN':
                        self.match('SEPARATOR')
                else:
                    self.errors.append(f"Syntax error: Expected VARIABLE, found {self.current_token[1]} at line {self.current_token[2]}")
            elif self.current_token[0] == 'VARIABLE':
                self.match(self.current_token[0])
            elif self.current_token[0] == 'LITERAL':
                self.match(self.current_token[0])
                if self.current_token[0] != 'RPAREN':
                    self.match('SEPARATOR')
            else:
                self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")

    def block(self):
        self.match('LCURLY')
        self.block_stack.append((self.current_token[1], self.current_token[2]))
        while self.current_token and self.current_token[0] != 'RCURLY':
            self.statement()
        self.match('RCURLY')
        self.block_stack.pop()

    def function_definition(self):
        self.match('Blank')
        self.match('VARIABLE')
        self.match('LPAREN')
        self.argument_list()
        self.match('RPAREN')
        self.block()

    def function_call(self):
        if self.current_token[0] == 'FUNCTION':
            self.match('FUNCTION')
            self.match('LPAREN')
            self.argument_list()
            self.match('RPAREN')

# Example usage
code = """
integer $x = 5!
Blank $func1() {
    $x = $x + 1!
}
repeat ($x < 10, $x++) {
    $func1()
}
"""

tokens, Errors = tokenize(code)
print("Tokens:")
for token in tokens:
    print(token)
parser = Parser(tokens)
parser.parse()
print("Syntax Errors:")
for error in parser.errors:
    print(error)
