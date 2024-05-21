class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = {}
        self.errors = []

    def analyze(self):
        self.check_variable_usage()
        self.check_function_calls()
        self.check_data_type()
        self.check_type_compatibility()

    def check_variable_usage(self):
        for token in self.tokens:
            if token[0] == 'VARIABLE' and token[1] not in self.symbol_table:
                self.errors.append(f"Semantic error: Variable '{token[1]}' used without declaration at line {token[2]}")

    def check_function_calls(self):
        for token in self.tokens:
            if token[0] == 'FUNCTION' and token[1] not in self.symbol_table:
                self.errors.append(f"Semantic error: Function '{token[1]}' called without definition at line {token[2]}")

    def check_data_type(self):
        for lexeme, info in self.symbol_table.items():
            if info['token_type'] == 'VARIABLE' and info['data_type'] != None and info['value'] != None:
                if info['data_type'] == 'integer':
                    if not info['value'].isdigit():
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'decimal':
                    try:
                        float(info['value'])
                    except ValueError:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'line':
                    if not info['value'].startswith('"') or not info['value'].endswith('"'):
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'single':
                    if len(info['value']) != 1 or not info['value'].isalpha():
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'flag':
                    if info['value'] not in ['yes', 'no']:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")

    def check_type_compatibility(self):
        for i, token in enumerate(self.tokens):
            if token[0] == 'OPERATOR':
                if i == 0 or i == len(self.tokens) - 1:
                    self.errors.append(f"Semantic error: Operator '{token[1]}' requires two operands at line {token[2]}")
                    continue
                    
                previous_token = self.tokens[i - 1]
                next_token = self.tokens[i + 1]
                if previous_token[0] not in ['VARIABLE','FUNCTION','LITERAL'] or next_token[0] not in ['VARIABLE','FUNCTION','LITERAL']:
                    self.errors.append(f"Semantic error: Operator '{token[1]}' requires two variable operands at line {token[2]}")
                    continue

                if previous_token[0] == 'LITERAL':
                    previous_token_type = 'integer' if previous_token[1].isdigit() else ('decimal' if '.' in previous_token[1] else 'line')
                else: 
                    left_operand_type = self.symbol_table[previous_token[1]]['type']

                if next_token[0] == 'LITERAL':
                    next_token_type = 'integer' if next_token[1].isdigit() else ('decimal' if '.' in next_token[1] else 'line')
                else:
                    right_operand_type = self.symbol_table[next_token[1]]['type']

                if left_operand_type != right_operand_type:
                    self.errors.append(f"Semantic error: Type mismatch in expression at line {token[2]}")
