import re
from sementic import SemanticAnalyzer
class SyntaxError(Exception):
    def __init__(self, message, token=None, code_line="", line_number=0, expected_tokens=None):
        self.message = message
        if token:
            self.message += f" at line {token['line']} col {token['column']}"
            self.pointer_line = ' ' * (token['column'] - 1) + '^'
        self.code_line = code_line
        self.line_number = line_number
        self.expected_tokens = expected_tokens
        super().__init__(self.message)

    def __str__(self):
        error_message = f"{self.message}\n"
        if self.code_line:
            error_message += f"  {self.line_number}: {self.code_line}\n      {self.pointer_line}"
        if self.expected_tokens:
            error_message += f"\nExpected tokens: {', '.join(self.expected_tokens)}"
        return error_message


# Define the patterns for different lexical elements in the language
TOKEN_PATTERNS = [
    ('DATATYPE', r'\b(integer|line|decimal|single|flag)\b'),
    ('VALUE', r'\"[^\"]*\"|\d+(\.\d+)?|\'[^\']*\'|yes|no'),
    ('FUNCTION_DEF', r'blank\s+[a-zA-Z][_a-zA-Z0-9]*\s*\(\s*\)'),
    ('VARIABLE', r'\b[a-zA-Z][_a-zA-Z0-9]*\b'),
    ('ASSIGN', r'='),
    ('CONDITIONAL_KEYWORD', r'\b(iff|otherwise|then)\b'),
    ('ITERATIVE_KEYWORD', r'\b(rotate|repeat)\b'),
    ('LOOP_CONTROL_KEYWORD', r'\b(stop|resume)\b'),
    ('PRINT_KEYWORD', r'\b(showOut)\b'),
    ('COMMENT', r'@.*'),
    ('STATEMENT_TERMINATOR', r'!'),
]

# Compile the regular expressions into a single pattern
TOKEN_REGEX = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS))


def tokenize(source_code):
    tokens = []
    errors = []
    line_num = 1

    for match in TOKEN_REGEX.finditer(source_code):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - source_code.rfind('\n', 0, match.start())

        if kind == 'COMMENT':
            continue  # Ignore comments

        tokens.append({
            'type': kind,
            'value': value,
            'line': line_num,
            'column': column
        })

        if kind == 'STATEMENT_TERMINATOR':
            line_num += 1

    return tokens, errors


def create_symbol_table(tokens):
    symbol_table = {}

    for i in range(len(tokens)):
        if tokens[i]['type'] == 'DATATYPE':
            if tokens[i + 1]['type'] == 'VARIABLE':
                data_type = tokens[i]['value']
                variable_name = tokens[i + 1]['value']
                i += 2
                value = None
                if tokens[i]['type'] == 'ASSIGN':
                    if tokens[i + 1]['type'] == 'VALUE':
                        value = tokens[i + 1]['value']
                        i += 1
                if variable_name not in symbol_table:
                    symbol_table[variable_name] = {
                        'datatype': data_type,
                        'value': value
                    }
    return symbol_table


def print_symbol_table(symbol_table):
    print("Symbol Table:")
    for variable, info in symbol_table.items():
        print(f"{variable}: {info['datatype']} = {info['value']}")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.current_token = tokens[self.current_index] if tokens else None

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def eat(self, expected_type):
        if self.current_token and self.current_token['type'] == expected_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected {expected_type} but found {self.current_token['type']}")

    def parse(self):
        while self.current_token:
            if self.current_token['type'] == 'DATATYPE':
                self.declaration()
            elif self.current_token['type'] == 'PRINT_KEYWORD':
                self.print_statement()
            else:
                raise SyntaxError("Invalid statement",
                                  self.current_token)

    def declaration(self):
        self.eat('DATATYPE')
        variable_name = self.current_token['value']
        self.eat('VARIABLE')
        self.eat('ASSIGN')
        value = self.current_token['value']
        self.eat('VALUE')
        self.eat('STATEMENT_TERMINATOR')
        print(f"Declared variable: {variable_name} = {value}")

    def print_statement(self):
        self.eat('PRINT_KEYWORD')
        variable_name = self.current_token['value']
        self.eat('VARIABLE')
        self.eat('STATEMENT_TERMINATOR')
        print(f"Printed value: {variable_name}")

class SemanticAnalyzer:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.current_index = 0
        self.current_token = tokens[self.current_index] if tokens else None
        self.current_scope = []

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def eat(self, expected_type):
        if self.current_token and self.current_token['type'] == expected_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected {expected_type} but found {self.current_token['type']}")

    def parse(self):
        while self.current_token:
            if self.current_token['type'] == 'DATATYPE':
                self.declaration()
            elif self.current_token['type'] == 'PRINT_KEYWORD':
                self.print_statement()
            elif self.current_token['type'] == 'CONDITIONAL_KEYWORD':
                self.conditional_statement()
            else:
                raise SyntaxError("Invalid statement",
                                  self.current_token)

    def declaration(self):
        self.eat('DATATYPE')
        variable_name = self.current_token['value']
        self.eat('VARIABLE')
        self.eat('ASSIGN')
        value = self.current_token['value']
        self.eat('VALUE')
        self.eat('STATEMENT_TERMINATOR')

        # Check if variable already exists in current scope
        if variable_name in self.current_scope:
            raise SyntaxError(
                f"Variable '{variable_name}' already declared in this scope")
        
        # Add variable to symbol table
        self.symbol_table[variable_name] = {
            'datatype': self.current_token['value'],
            'value': value
        }
        self.current_scope.append(variable_name)  # Add variable to current scope

    def print_statement(self):
        self.eat('PRINT_KEYWORD')
        variable_name = self.current_token['value']
        self.eat('VARIABLE')
        self.eat('STATEMENT_TERMINATOR')

        # Check if variable exists in symbol table
        if variable_name not in self.symbol_table:
            raise SyntaxError(
                f"Variable '{variable_name}' not declared")
        
        # Print the value of the variable
        print(f"Printed value: {self.symbol_table[variable_name]['value']}")

    def conditional_statement(self):
        self.eat('CONDITIONAL_KEYWORD')
        condition_variable = self.current_token['value']
        self.eat('VARIABLE')
        
        # Check if condition variable exists in symbol table
        if condition_variable not in self.symbol_table:
            raise SyntaxError(
                f"Variable '{condition_variable}' not declared")
        
        # Check if condition_variable is of type 'flag'
        if self.symbol_table[condition_variable]['datatype'] != 'flag':
            raise SyntaxError(
                f"Condition variable '{condition_variable}' must be of type 'flag'")
        
        # Consume the block
        self.eat('STATEMENT_TERMINATOR')
        while self.current_token and self.current_token['type'] != 'then':
            self.advance()
        self.eat('then')
        self.eat('STATEMENT_TERMINATOR')
        
        # Track variable scope within the conditional block
        conditional_scope = self.current_scope.copy()
        
        # Parse statements inside the conditional block
        while self.current_token and self.current_token['type'] != 'STATEMENT_TERMINATOR':
            if self.current_token['type'] == 'PRINT_KEYWORD':
                self.print_statement()
            else:
                raise SyntaxError("Invalid statement inside conditional block",
                                  self.current_token)
        
        # Restore the original scope after the block
        self.current_scope = conditional_scope.copy()

if __name__ == '__main__':
    source_code = '''
integer myAge = 8!
line uniName = "Riphah International University"!
decimal pi = 3.14!
single a = '1'!
flag pass = yes!
flag fail = no!
showOut("Enter your Age")!
getInput(userAge)!
iff ( userAge >= 18 ) {
    showOut("Yes!!, you are eligible for CNIC")!
}
then {
    showOut("Sorry!!, you are not eligible for CNIC")!
}
'''

    tokens, errors = tokenize(source_code)
    if errors:
        print("Errors found while tokenizing:")
        for error in errors:
            print(error)
    else:
        symbol_table = create_symbol_table(tokens)
        print_symbol_table(symbol_table)

        parser = Parser(tokens)
        try:
            parser.parse()
            semantic_analyzer = SemanticAnalyzer(tokens, symbol_table)
            semantic_analyzer.parse()
        except SyntaxError as e:
            print(f"Syntax Error: {e}")

semantic = SemanticAnalyzer(tokens, symbol_table)
semantic.parse()
