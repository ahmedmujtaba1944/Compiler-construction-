# from lexical_Analyzer import tokenize
# from Syntax_Analyzer import Parser
# from Semantic_Analyzer import SemanticAnalyzer

# def main():
#     # with open('code.txt', 'r') as file:
#     #     code = file.read()
#     file_path = r'G:\University_Study\8th Semester\Compiler-construction\cc-project\Compiler-construction-\New\code.txt'
#     with open(file_path, 'r') as file:
#          code = file.read()


#     tokens, lexical_errors = tokenize(code)

#     if lexical_errors:
#         for error in lexical_errors:
#             print(error)
#     else:
#         print("Lexical Analysis successful!")
#         print(tokens)

#         parser = Parser(tokens)
#         parser.parse()

#         if parser.errors:
#             for error in parser.errors:
#                 print(error)
#         else:
#             print("Syntax Analysis successful!")

#             semantic_analyzer = SemanticAnalyzer(tokens)
#             semantic_errors = semantic_analyzer.analyze()

#             if semantic_errors:
#                 for error in semantic_errors:
#                     print(error)
#             else:
#                 print("Semantic Analysis successful!")

# if __name__ == "__main__":
#     main()

from lexical_Analyzer import LexicalAnalyzer
from parser import Parser
from Semantic_Analyzer import SemanticAnalyzer

def main():
    # Read the program from a file or take input from the user
    program = """
integer userAge!
showOut("Enter your Age")!
getInput(userAge)!
iff (userAge >= 18) {
    showOut("yes!!, you are eligible for CNIC")!
}
then {
    showOut("Sorry!!, you are not eligible for CNIC")!
}
"""

    # Lexical Analysis
    lex_analyzer = LexicalAnalyzer(program)
    lex_analyzer.analyze()
    tokens = lex_analyzer.get_tokens()

    # Parsing
    parser = Parser(tokens)
    parser.parse()
    parse_tree = parser.get_parse_tree()

    # Semantic Analysis
    semantic_analyzer = SemanticAnalyzer(tokens)
    semantic_analyzer.analyze()

    # Display errors, if any
    if semantic_analyzer.errors:
        print("Semantic Errors:")
        for error in semantic_analyzer.errors:
            print(error)
    else:
        print("No Semantic Errors found. Program is semantically correct.")

if __name__ == "__main__":
    main()
