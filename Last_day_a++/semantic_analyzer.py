import re
class SemanticAnalyzer:
    def __init__(self, symbol_table, tokens):
        self.symbol_table = symbol_table
        self.tokens = tokens
        self.errors = []
        self.current_token_index = 0

    def analyze(self):
        while self.current_token_index < len(self.tokens):
            token_type, lexeme, line_number, *data_type = self.tokens[self.current_token_index]
            if token_type == 'ASSIGN':
                self.check_assignment()
            self.current_token_index += 1

    def check_assignment(self):
        variable_token = self.tokens[self.current_token_index - 1]
        variable_name = variable_token[1]
        variable_type = self.symbol_table[variable_name]['data_type']
        value_token = self.tokens[self.current_token_index + 1]
        value_type = self.get_value_type(value_token[1])

        if variable_type != value_type:
            self.errors.append(f"Semantic error: Type mismatch on line {variable_token[2]}: cannot assign {value_type} to {variable_type}")

    def get_value_type(self, value):
        if re.match(r'^-?\d+$', value):
            return 'integer'
        elif re.match(r'^-?\d+\.\d*$', value):
            return 'decimal'
        elif re.match(r'^".*"$', value):
            return 'line'
        elif value in ['true', 'false']:
            return 'flag'
        else:
            return self.symbol_table.get(value, {}).get('data_type', 'unknown')

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
            if info['token_type'] == 'VARIABLE' and info['data_type'] != None and info['value'] != None:
                if info['data_type'] == 'integer':
                    if isinstance(int(info['value']), int):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'decimal':
                    if isinstance(float(info['value']), float):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'line':
                    if isinstance(info['value'], str):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'flag':
                    if info['value'] in ['true', 'false']:
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")

    # def check_type_compatibility(self):
    #     operator_tokens = ['+', '-', '*', '/','%']
    #     for i, (token_type, lexeme, line_number, *data_type) in enumerate(self.tokens):
    #         if token_type == 'OPERATOR' and lexeme in operator_tokens:
    #             if i == 0 or i == len(self.tokens) - 1:
    #                 self.errors.append(f"Semantic error: Operator '{lexeme}' requires two operands at line {line_number}")
    #                 continue
                    
    #             previous_token = self.tokens[i - 1]
    #             next_token = self.tokens[i + 1]
    #             if previous_token[0] not in ['VARIABLE','FUNCTION','LITERAL'] or next_token[0] not in ['VARIABLE','FUNCTION','LITERAL']:
    #                 self.errors.append(f"Semantic error: Operator '{lexeme}' requires two variable operands at line {line_number}")
    #                 continue
    #             if previous_token[0] == 'LITERAL':
    #                 try:
    #                     float(previous_token[1])  # Attempt to convert to float
    #                     previous_token_type = 'Fl'
    #                 except ValueError:
    #                     try:
    #                         int(previous_token[1])  # Attempt to convert to int
    #                         previous_token_type = 'Num'
    #                     except ValueError:
    #                         previous_token_type = None 
    #             else: 
    #                 # left_operand_type = self.symbol_table[previous_token[1]]['data_type'] if self.symbol_table[previous_token[1]]['data_type'] else None
    #                 if previous_token[1] in self.symbol_table:
    #                     left_operand_type = self.symbol_table[previous_token[1]]['data_type']
                    
    #             if next_token[0] == 'LITERAL':
    #                 try:
    #                     float(next_token[1])  # Attempt to convert to float
    #                     next_token_type = float
    #                 except ValueError:
    #                     try:
    #                         int(next_token[1])  # Attempt to convert to int
    #                         next_token_type = int
    #                     except ValueError:
    #                         next_token_type = None
    #             else:
    #                 # right_operand_type = self.symbol_table[next_token[1]]['data_type'] 
    #                 if next_token[1] in self.symbol_table:
    #                     right_operand_type = self.symbol_table[next_token[1]]['data_type']
    #             if left_operand_type is None or right_operand_type is None:
    #                 self.errors.append(f"Semantic error: Type not defined at line {line_number}")
    #                 continue

    #             if left_operand_type in ['Fl', 'Num'] or right_operand_type in ['Fl', 'Num']:
    #                 continue
    #             else:
    #                 self.errors.append(f"Semantic error: Operands must be integer or float types for arithmetic operations at line {line_number}")
    #                 continue
                
    #             if lexeme in ['-', '/', '*', '%'] and left_operand_type in ['Str','Bool'] or right_operand_type in ['Str','Bool']:
    #                 self.errors.append(f"Semantic error: Cannot perform these operations on line {line_number}")
    #                 continue

    #             if left_operand_type != right_operand_type:
    #                 self.errors.append(f"Semantic error: Type mismatch in expression at line {line_number}")
    def check_type_compatibility(self):
        operator_tokens = ['+', '-', '*', '/', '%']
        for i, (token_type, lexeme, line_number, *data_type) in enumerate(self.tokens):
            if token_type == 'OPERATOR' and lexeme in operator_tokens:
                if i == 0 or i == len(self.tokens) - 1:
                    self.errors.append(f"Semantic error: Operator '{lexeme}' requires two operands at line {line_number}")
                    continue
                    
                previous_token = self.tokens[i - 1]
                next_token = self.tokens[i + 1]
                
                # Initialize operands types
                left_operand_type = None
                right_operand_type = None
                
                # Check previous token type
                if previous_token[0] == 'LITERAL':
                    try:
                        float(previous_token[1])  # Attempt to convert to float
                        left_operand_type = 'decimal'
                    except ValueError:
                        try:
                            int(previous_token[1])  # Attempt to convert to int
                            left_operand_type = 'integer'
                        except ValueError:
                            left_operand_type = None
                else:
                    if previous_token[1] in self.symbol_table:
                        left_operand_type = self.symbol_table[previous_token[1]]['data_type']
                    else:
                        left_operand_type = None
                
                # Check next token type
                if next_token[0] == 'LITERAL':
                    try:
                        float(next_token[1])  # Attempt to convert to float
                        right_operand_type = 'decimal'
                    except ValueError:
                        try:
                            int(next_token[1])  # Attempt to convert to int
                            right_operand_type = 'integer'
                        except ValueError:
                            right_operand_type = None
                else:
                    if next_token[1] in self.symbol_table:
                        right_operand_type = self.symbol_table[next_token[1]]['data_type']
                    else:
                        right_operand_type = None
                
                # Check specific operations and their operand types
                if lexeme in ['-', '/', '*', '%'] and (left_operand_type in ['line', 'flag'] or right_operand_type in ['line', 'flag']):
                    self.errors.append(f"Semantic error: Cannot perform these operations on non-numeric types at line {line_number}")
                    continue
                
                # Check for type mismatch
                if left_operand_type != right_operand_type:
                    self.errors.append(f"Semantic error: Type mismatch in expression at line {line_number}")
                # Handle cases where type is not defined
                if left_operand_type is None or right_operand_type is None:
                    self.errors.append(f"Semantic error: Type not defined at line {line_number}")
                    continue
                
                # Check if both operands are numeric
                if left_operand_type in ['decimal', 'integer'] and right_operand_type in ['decimal', 'number']:
                    continue
                
                elif left_operand_type in ['integer', 'integer'] and right_operand_type in ['integer', 'number']:
                    continue                
                
                else:
                    self.errors.append(f"Semantic error: Operands must be integer or float types for arithmetic operations at line {line_number}")
                    continue
                

