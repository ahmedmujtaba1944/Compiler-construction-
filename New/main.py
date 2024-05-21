from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer

def main():
    # Path to the code file
    file_path = r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\New\code.txt'
    
    # Read the code from the file
    with open(file_path, 'r') as file:
        code = file.read()

    # Perform lexical analysis
    tokens, lexical_errors = tokenize(code)

    # Display lexical errors, if any
    if lexical_errors:
        for error in lexical_errors:
            print(error)
    else:
        print("Lexical Analysis successful!")
        print(tokens)

        # Parse the tokens
        parser = Parser(tokens)
        parser.parse()

        # Display syntax errors, if any
        if parser.errors:
            for error in parser.errors:
                print(error)
        else:
            print("Syntax Analysis successful!")

            # Perform semantic analysis
            semantic_analyzer = SemanticAnalyzer(tokens)
            semantic_errors = semantic_analyzer.analyze()

            # Display semantic errors, if any
            if semantic_errors:
                for error in semantic_errors:
                    print(error)
            else:
                print("Semantic Analysis successful!")

if __name__ == "__main__":
    main()
