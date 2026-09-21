from .lexer         import Lexer
from .parser        import Parser
from .environment   import Environment
from .interpreter   import Interpreter
from .errors        import FadeError

# ##################################
# Run function to execute the code
# ##################################

def run(text:str, env, show_tokens:bool=False, show_ast:bool=False)->list:
    """
    text should be a fade code.
    """

    return_values = []

    lexer = Lexer(text)
    tokens = lexer.tokenize()
    if show_tokens is True: return_values.append(tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    if show_ast is True: return_values.append(ast)

    if ast is None:
        return [None]

    if not (show_tokens or show_ast):
        interpreter = Interpreter(ast, env)
        return_values = interpreter.evaluate()
    return return_values
