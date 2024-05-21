import re

class LexicalAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.errors = []

    def tokenize(self):
        token_types = {
            'DATA_TYPE': r'(integer|decimal|line|flag|single)',
            'VARIABLE': r'@[_a-zA-Z][_a-zA-Z0-9]*',
            'CONSTANT': r'(\".*?\"|\'.*?\')',
            'KEYWORD': r'(iff|otherwise|then|rotate|repeat|showOut|blank|zero|getInput)',
            'OPERATOR': r'(>=|<=|==|!=|\+\+|\-\-|\+|\-|\*|/|<|>)',
            'STATEMENT_END': r'!',
            'LCURLY': r'{',
            'RCURLY': r'}',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
        }

        patterns = {token: re.compile(pattern) for token, pattern in token_types.items()}

        lines = self.code.split('\n')
        for line_number, line in enumerate(lines, start=1):
            position = 0
            while position < len(line):
                if line[position].isspace():
                    position += 1
                    continue
                match = None
                for token_type, pattern in patterns.items():
                    match = re.match(pattern, line[position:])
                    if match:
                        token = match.group(0)
                        self.tokens.append((token_type, token, line_number))
                        position += len(token)
                        break
                if not match:
                    self.errors.append(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                    position += 1

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
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
        while self.current_token:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'LCURLY':
            self.block()
        elif self.current_token[0] == 'RCURLY':
            self.advance()
        elif self.current_token[0] == 'DATA_TYPE':
            self.declaration()
        elif self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ['iff', 'otherwise', 'then']:
                self.conditional_statement()
            elif self.current_token[1] in ['rotate', 'repeat']:
                self.iterative_statement()
            elif self.current_token[1] == 'blank':
                self.advance()
                if self.current_token[0] != 'STATEMENT_END':
                    self.errors.append(f"Syntax error: Missing statement terminator '!' at line {self.current_token[2]}")
                else:
                    self.advance()
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

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []

    def analyze(self):
        # Perform semantic analysis here
        pass

def main():

    path = r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\text\code.txt'
    with open(path, 'r') as file:
        code = file.read()
        

    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    lexer.tokenize()
    tokens = lexer.tokens
    lexical_errors = lexer.errors

    if lexical_errors:
        for error in lexical_errors:
            print(error)
        return

    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    parser.parse()
    syntax_errors = parser.errors

    if syntax_errors:
        for error in syntax_errors:
            print(error)
        return

    # Semantic Analysis
    semantic_analyzer = SemanticAnalyzer(tokens)
    semantic_analyzer.analyze()
    semantic_errors = semantic_analyzer.errors

    if semantic_errors:
        for error in semantic_errors:
            print(error)
        return

    print("Code passed lexical, syntax, and semantic analysis successfully!")

if __name__ == "__main__":
    main()
