# class SemanticAnalyzer:
#     def __init__(self, symbol_table, tokens):
#         self.symbol_table = symbol_table
#         self.tokens = tokens
#         self.current_token_index = 0
#         self.current_token = self.tokens[self.current_token_index] if self.tokens else None
#         self.errors = []

#     def analyze(self):
#         self.check_variable_usage()
#         self.check_function_calls()
#         self.check_data_type()
#         self.check_type_compatibility()

#     def check_variable_usage(self):
#         for token_type, lexeme, line_number, *data_type in self.tokens:
#             if token_type == 'VARIABLE' and lexeme not in self.symbol_table:
#                 self.errors.append(f"Semantic error: Variable '{lexeme}' used without declaration at line {line_number}")

#     def check_function_calls(self):
#         for token_type, lexeme, line_number, *data_type in self.tokens:
#             if token_type == 'FUNCTION' and lexeme not in self.symbol_table:
#                 self.errors.append(f"Semantic error: Function '{lexeme}' called without definition at line {line_number}")

#     def check_data_type(self):
#         for lexeme, info in self.symbol_table.items():
#             if info['token_type'] == 'VARIABLE' and info['data_type'] != None and info['value'] != None:
#                 if info['data_type'] == 'integer':
#                     if isinstance(int(info['value']), int):
#                         continue
#                     else:
#                         self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
#                 elif info['data_type'] == 'decimal':
#                     if isinstance(float(info['value']), float):
#                         continue
#                     else:
#                         self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
#                 elif info['data_type'] == 'line':
#                     if isinstance(info['value'], str):
#                         continue
#                     else:
#                         self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
#                 elif info['data_type'] == 'flag':
#                     if info['value'] in ['yes', 'no']:
#                         continue
#                     else:
#                         self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")

#     def check_type_compatibility(self):
#         operator_tokens = ['+', '-', '*', '/','%']
#         for i, (token_type, lexeme, line_number, *data_type) in enumerate(self.tokens):
#             if token_type == 'OPERATOR' and lexeme in operator_tokens:
#                 if i == 0 or i == len(self.tokens) - 1:
#                     self.errors.append(f"Semantic error: Operator '{lexeme}' requires two operands at line {line_number}")
#                     continue
                    
#                 previous_token = self.tokens[i - 1]
#                 next_token = self.tokens[i + 1]
#                 if previous_token[0] not in ['VARIABLE','FUNCTION','LITERAL'] or next_token[0] not in ['VARIABLE','FUNCTION','LITERAL']:
#                     self.errors.append(f"Semantic error: Operator '{lexeme}' requires two variable operands at line {line_number}")
#                     continue
#                 if previous_token[0] == 'LITERAL':
#                     try:
#                         float(previous_token[1])  # Attempt to convert to float
#                         previous_token_type = 'decimal'
#                     except ValueError:
#                         try:
#                             int(previous_token[1])  # Attempt to convert to int
#                             previous_token_type = 'integer'
#                         except ValueError:
#                             previous_token_type = None 
#                 else: 
#                     left_operand_type = self.symbol_table[previous_token[1]]['data_type'] if self.symbol_table[previous_token[1]]['data_type'] else None
#                 if next_token[0] == 'LITERAL':
#                     try:
#                         float(next_token[1])  # Attempt to convert to float
#                         next_token_type = float
#                     except ValueError:
#                         try:
#                             int(next_token[1])  # Attempt to convert to int
#                             next_token_type = int
#                         except ValueError:
#                             next_token_type = None
#                 else:
#                     right_operand_type = self.symbol_table[next_token[1]]['data_type'] 
#                 if left_operand_type is None or right_operand_type is None:
#                     self.errors.append(f"Semantic error: Type not defined at line {line_number}")
#                     continue

#                 if left_operand_type in ['decimal', 'integer'] or right_operand_type in ['decimal', 'integer']:
#                     continue
#                 else:
#                     self.errors.append(f"Semantic error: Operands must be integer or float types for arithmetic operations at line {line_number}")
#                     continue
                
#                 if lexeme in ['-', '/', '*', '%'] and left_operand_type in ['line','flag'] or right_operand_type in ['line','flag']:
#                     self.errors.append(f"Semantic error: Cannot perform these operations on line {line_number}")
#                     continue

#                 if left_operand_type != right_operand_type:
#                     self.errors.append(f"Semantic error: Type mismatch in expression at line {line_number}")



class SemanticAnalyzer:
    def __init__(self, symbol_table, tokens):
        self.symbol_table = symbol_table
        self.tokens = tokens
        self.errors = []

    def analyze(self):
        self.check_variable_usage()
        self.check_function_calls()
        self.check_data_type()
        self.check_type_compatibility()

    def check_variable_usage(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'VARIABLE' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Variable '{lexeme}' used without declaration at line {line_number}")

    def check_function_calls(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'FUNCTION' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Function '{lexeme}' called without definition at line {line_number}")

    def check_data_type(self):
        for lexeme, info in self.symbol_table.items():
            if info['token_type'] == 'VARIABLE' and info['data_type'] is not None and info['value'] is not None:
                if info['data_type'] == 'integer':
                    if not isinstance(info['value'], int):
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'decimal':
                    if not isinstance(info['value'], float):
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'line':
                    if not isinstance(info['value'], str):
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'flag':
                    if info['value'] not in ['yes', 'no']:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")

    def check_type_compatibility(self):
        operator_tokens = ['+', '-', '*', '/', '%']
        for i, (token_type, lexeme, line_number, *data_type) in enumerate(self.tokens):
            if token_type == 'OPERATOR' and lexeme in operator_tokens:
                if i == 0 or i == len(self.tokens) - 1:
                    self.errors.append(f"Semantic error: Operator '{lexeme}' requires two operands at line {line_number}")
                    continue

                previous_token = self.tokens[i - 1]
                next_token = self.tokens[i + 1]

                if previous_token[0] not in ['VARIABLE', 'FUNCTION', 'LITERAL'] or next_token[0] not in ['VARIABLE', 'FUNCTION', 'LITERAL']:
                    self.errors.append(f"Semantic error: Operator '{lexeme}' requires two operands at line {line_number}")
                    continue

                left_operand_type = self.get_operand_type(previous_token)
                right_operand_type = self.get_operand_type(next_token)

                if left_operand_type is None or right_operand_type is None:
                    self.errors.append(f"Semantic error: Type not defined for operands at line {line_number}")
                    continue

                if left_operand_type in ['decimal', 'integer'] and right_operand_type in ['decimal', 'integer']:
                    if lexeme in ['-', '/', '*', '%'] and (left_operand_type in ['line', 'flag'] or right_operand_type in ['line', 'flag']):
                        self.errors.append(f"Semantic error: Cannot perform '{lexeme}' operation on non-numeric types at line {line_number}")
                    continue
                else:
                    self.errors.append(f"Semantic error: Operands must be integer or decimal types for arithmetic operations at line {line_number}")
                    continue

                if left_operand_type != right_operand_type:
                    self.errors.append(f"Semantic error: Type mismatch in expression at line {line_number}")

    def get_operand_type(self, token):
        token_type, lexeme, *rest = token
        if token_type == 'LITERAL':
            try:
                float(lexeme)  # Attempt to convert to float
                return 'decimal'
            except ValueError:
                try:
                    int(lexeme)  # Attempt to convert to int
                    return 'integer'
                except ValueError:
                    return None
        elif token_type == 'VARIABLE' or token_type == 'FUNCTION':
            return self.symbol_table.get(lexeme, {}).get('data_type')
        return None

