class CodeGenerator:
    def __init__(self,symbol_table, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.assembly_code = []
        self.symbol_table = symbol_table
        self.label_count = 0

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def generate(self):
        self.program()
        return "\n".join(self.assembly_code)

    def program(self):
        while self.current_token:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'LCURLY':
            self.advance()
        elif self.current_token[0] == 'RCURLY':
            self.advance()
        elif self.current_token[0] == 'DATA_TYPE':
            self.declaration()
        elif self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ['iff', 'otherwise', 'then']:
                self.conditional_statement()
            elif self.current_token[1] in ['repeat', 'rotate']:
                self.loop_statement()
            elif self.current_token[1] == 'Blank':
                self.function_definition()
            elif self.current_token[1] == 'resume' or self.current_token[1] == 'stop':
                self.advance()
        elif self.current_token[0] == 'FUNCTION':            
            self.function_call()
            self.advance()
        elif self.current_token[0] == 'VARIABLE':
            self.assignment()
        else:
            self.advance()

    def declaration(self):
        data_type = self.current_token[1]
        self.advance()
        variable_name = self.current_token[1]
        self.advance()
        if self.current_token[0] == 'STATEMENT_END':
            self.advance()
        else:
            self.assignment(variable_name, data_type)

    def assignment(self, variable_name=None, data_type=None):
        if not variable_name:
            variable_name = self.current_token[1]
            self.advance()
        self.advance()
        value = self.current_token[1]
        self.advance()
        if data_type == 'integer':
            self.assembly_code.append(f"MOV {variable_name}, {value}")
        elif data_type == 'decimal':
            self.assembly_code.append(f"MOV {variable_name}, {value}")
        elif data_type == 'line':
            self.assembly_code.append(f"MOV {variable_name}, '{value}'")
        elif data_type == 'flag':
            self.assembly_code.append(f"MOV {variable_name}, {1 if value == 'true' else 0}")
        self.advance()

    def condition(self):
        left_operand = self.current_token[1]
        self.advance()
        operator = self.current_token[1]
        self.advance()
        right_operand = self.current_token[1]
        self.advance()
        self.assembly_code.append(f"CMP {left_operand}, {right_operand}")
        if operator == '==':
            self.assembly_code.append("JE")
        elif operator == '!=':
            self.assembly_code.append("JNE")
        elif operator == '<':
            self.assembly_code.append("JL")
        elif operator == '>':
            self.assembly_code.append("JG")
        elif operator == '<=':
            self.assembly_code.append("JLE")
        elif operator == '>=':
            self.assembly_code.append("JGE")

    def conditional_statement(self):
        if self.current_token[1] == 'iff':
            self.advance()
            self.condition()
            label = self.new_label()
            self.assembly_code.append(f"JMP {label}")
            self.advance()
            self.assembly_code.append(f"{label}:")
        elif self.current_token[1] == 'otherwise':
            self.advance()
            self.condition()
            label = self.new_label()
            self.assembly_code.append(f"JMP {label}")
            self.advance()
            self.assembly_code.append(f"{label}:")
        elif self.current_token[1] == 'then':
            self.advance()
            label = self.new_label()
            self.assembly_code.append(f"JMP {label}")
            self.advance()
            self.assembly_code.append(f"{label}:")

    def loop_statement(self):
        if self.current_token[1] == 'repeat':
            self.advance()
            self.advance()
            self.declaration()
            self.condition()
            self.advance()
            self.advance()
        elif self.current_token[1] == 'rotate':
            self.advance()
            self.advance()
            self.condition()
            self.advance()
            self.advance()

    def function_call(self):
        function_name = self.current_token[1]
        self.advance()
        self.advance()
        args = []
        while self.current_token[0] != 'RPAREN':
            args.append(self.current_token[1])
            self.advance()
            if self.current_token[0] == 'SEPERATOR':
                self.advance()
        self.assembly_code.append(f"CALL {function_name} {', '.join(args)}")
        self.advance()

    def function_definition(self):
        if self.current_token[1] == 'Blank':
            self.advance()
        else:
            self.advance()
        function_name = self.current_token[1]
        self.advance()
        self.advance()
        self.assembly_code.append(f"{function_name}:")
        while self.current_token[0] != 'RPAREN':
            self.advance()
        self.advance()
        self.advance()

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"