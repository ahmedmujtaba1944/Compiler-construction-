import re

# Define token types
token_types = {
    'INTEGER': r'\d+',
    'STRING': r'\".*?\"',
    'DECIMAL': r'\d+\.\d+',
    'CHAR': r'\'.\'',
    'BOOL': r'yes|no',
    'KEYWORD': r'iff|otherwise|then|repeat|rotate|stop|resume|blank|zero|getInput|showOut',
    'DATATYPE': r'integer|line|decimal|single|flag',
    'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9]*',
    'OPERATOR': r'[+\-*/><=!]+',
    'PUNCTUATION': r'[\(\),!\{\}]',
    'COMMENT': r'@.*?$'
}

# Tokenize function
def tokenize(code):
    tokens = []
    code_lines = code.split('\n')
    line_number = 1
    for line in code_lines:
        line = line.strip()
        if line:
            while line:
                match = None
                for token_type, pattern in token_types.items():
                    match = re.match(pattern, line)
                    if match:
                        value = match.group(0)
                        if token_type != 'COMMENT':
                            tokens.append((token_type, value, line_number))
                        line = line[len(value):].strip()
                        break
                if not match:
                    print(f"Lexical Error: Invalid token at line {line_number}")
                    break
            line_number += 1
    return tokens

# Test the lexer
code = """
integer myVar = 10!
&&&
line myString = "Hello, World!"!
iff (myVar > 5) {
    showOut(myString)!
}
"""
tokens = tokenize(code)
for token in tokens:
    print(token)