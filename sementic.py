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

# Example usage
if __name__ == '__main__':
    # Assume 'tokens' and 'symbol_table' are properly initialized
    semantic_analyzer = SemanticAnalyzer(tokens, symbol_table)
    semantic_analyzer.parse()
