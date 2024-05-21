from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer

def main():
    # with open('code.txt', 'r') as file:
    #     code = file.read()
    file_path = r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\New\code.txt'
    with open(file_path, 'r') as file:
         code = file.read()


    tokens, lexical_errors = tokenize(code)

    if lexical_errors:
        for error in lexical_errors:
            print(error)
    else:
        print("Lexical Analysis successful!")
        print(tokens)

        parser = Parser(tokens)
        parser.parse()

        if parser.errors:
            for error in parser.errors:
                print(error)
        else:
            print("Syntax Analysis successful!")

            semantic_analyzer = SemanticAnalyzer(tokens)
            semantic_errors = semantic_analyzer.analyze()

            if semantic_errors:
                for error in semantic_errors:
                    print(error)
            else:
                print("Semantic Analysis successful!")

if __name__ == "__main__":
    main()
