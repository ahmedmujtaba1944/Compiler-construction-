class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = {}
        self.errors = []
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def analyze(self):
        self.program()

    def program(self):
        self.statement_list()

    def statement_list(self):
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
            elif self.current_token[1] in ['repeat', 'rotate']:
                self.loop_statement()
            elif self.current_token[1] == 'zero':
                self.function_definition()
            elif self.current_token[1] == 'stop' or self.current_token[1] == 'resume':
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
            self.errors.append(f"Semantic error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            self.advance()

    def declaration(self):
        datatype = self.current_token[1]
        self.match('DATA_TYPE')
        var_name = self.current_token[1]
        self.match('VARIABLE')
        if var_name in self.symbol_table:
            self.errors.append(f"Semantic error: Variable '{var_name}' already declared at line {self.current_token[2]}")
        else:
            self.symbol_table[var_name] = datatype

        if self.current_token[0] == 'STATEMENT_END':
            self.match('STATEMENT_END')
        elif self.current_token[0] == 'ASSIGN':
            self.match('ASSIGN')
            self.expression()
            self.match('STATEMENT_END')
        else:
            self.errors.append(f"Semantic error: Expected '!' or '=', found {self.current_token[1]} at line {self.current_token[2]}")

    def assignment(self):
        var_name = self.current_token[1]
        if var_name not in self.symbol_table:
            self.errors.append(f"Semantic error: Variable '{var_name}' not declared at line {self.current_token[2]}")
        self.match('VARIABLE')
        self.match('ASSIGN')
        self.expression()
        self.match('STATEMENT_END')

    def expression(self):
        if self.current_token[0] in ['LITERAL', 'CONSTANT', 'VARIABLE', 'OPERATOR']:
            if self.current_token[0] == 'VARIABLE':
                var_name = self.current_token[1]
                if var_name not in self.symbol_table:
                    self.errors.append(f"Semantic error: Variable '{var_name}' not declared at line {self.current_token[2]}")
            self.match(self.current_token[0])
        elif self.current_token[0] == 'FUNCTION':
            self.function_call()
        else:
            self.errors.append(f"Semantic error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            self.advance()

    def conditional_statement(self):
        if self.current_token[1] == 'iff':
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

    def condition(self):
        self.expression()
        self.match('OPERATOR')
        self.expression()

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
                self.errors.append(f"Semantic error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
        else:
            self.errors.append(f"Semantic error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")

    def function_definition(self):
        func_name = self.current_token[1]
        if func_name in self.symbol_table:
            self.errors.append(f"Semantic error: Function '{func_name}' already declared at line {self.current_token[2]}")
        self.match('FUNCTION')
        self.match('LPAREN')
        self.argument_list()
        self.match('RPAREN')
        self.match('STATEMENT_END')
        self.block()

    def function_call(self):
        func_name = self.current_token[1]
        if func_name not in self.symbol_table:
            self.errors.append(f"Semantic error: Function '{func_name}' not declared at line {self.current_token[2]}")
        self.match('FUNCTION')
        self.match('LPAREN')
        self.argument_list()
        self.match('RPAREN')

    def argument_list(self):
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] == 'DATA_TYPE':
                self.match(self.current_token[0])
                if self.current_token[0] == 'VARIABLE':
                    self.match('VARIABLE')
                    if self.current_token[0] != 'RPAREN':
                        self.match('SEPERATOR')
                else:
                    self.errors.append(f"Semantic error: Expected VARIABLE, found {self.current_token[1]} at line {self.current_token[2]}")
            elif self.current_token[0] == 'VARIABLE':
                self.match(self.current_token[0])
            elif self.current_token[0] == 'LITERAL':
                self.match(self.current_token[0])
                if self.current_token[0] != 'RPAREN':
                    self.match('SEPERATOR')
            elif self.current_token[0] == 'CONSTANT':
                self.match('CONSTANT')
            else:
                self.errors.append(f"Semantic error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
                self.advance()

    def block(self):
        self.match('LCURLY')
        self.statement_list()
        self.match('RCURLY')

    def match(self, expected_token_type):
        if self.current_token and self.current_token[0] == expected_token_type or self.current_token == None:
            self.advance()
        else:
            self.errors.append(f"Semantic error: Expected {expected_token_type}, found {self.current_token[0] if self.current_token else 'EOF'} at line {self.current_token[2]}")
