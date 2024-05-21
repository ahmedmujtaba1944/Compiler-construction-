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
        if self.current_token is None and len(self.block_stack) > 0:
            self.errors.append(f"Syntax error: Missing '}}' of Block at line {self.block_stack[-1][1]}")

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
            if self.current_token[1] in ['iff', 'otherwise', 'then']:
                self.conditional_statement()
            elif self.current_token[1] in ['repeat', 'rotate']:
                self.loop_statement()
            elif self.current_token[1] in ['stop', 'resume']:
                self.advance()
                self.match('STATEMENT_END')
        elif self.current_token[0] == 'FUNCTION':
            self.function_call()
            self.match('STATEMENT_END')
        elif self.current_token[0] == 'VARIABLE':
            self.assignment()
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
        self.match('VARIABLE')
        if self.current_token and self.current_token[0] == 'ASSIGN':
            self.match('ASSIGN')
            while self.current_token and self.current_token[0] != 'STATEMENT_END':
                if self.expression():
                    break
        self.match('STATEMENT_END')

    def assignment(self):
        self.match('VARIABLE')
        self.match('ASSIGN')
        while self.current_token and self.current_token[0] != 'STATEMENT_END':
            if self.expression():
                break
        self.match('STATEMENT_END')

    def condition(self):
        self.expression()
        self.match('OPERATOR')
        self.expression()

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
                        self.match('SEPERATOR')
                else:
                    self.errors.append(f"Syntax error: Expected VARIABLE, found {self.current_token[1]} at line {self.current_token[2]}")
            elif self.current_token[0] == 'VARIABLE':
                self.match(self.current_token[0])
            elif self.current_token[0] == 'LITERAL':
                self.match(self.current_token[0])
                if self.current_token[0] != 'RPAREN':
                    self.match('SEPERATOR')
            else:
                self.errors.append(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
                self.advance()

    def function_call(self):
        self.match('FUNCTION')
        self.match('LPAREN')
        self.argument_list()
        self.match('RPAREN')

    def block(self):
        if self.current_token[0] == 'LCURLY':
            self.block_stack.append(self.current_token)
        self.match('LCURLY')
        while self.current_token and self.current_token[0] != 'RCURLY':
            self.statement()
        if self.current_token and self.current_token[0] == 'RCURLY':
            self.block_stack.pop()
        self.match('RCURLY')
