from .lexer         import Lexer
from .parser        import Parser
from .environment   import Environment
from .interpreter   import Interpreter
from .errors        import FadeError

# ##################################
# Run function to execute the code
# ##################################

def run(text:str, env, debug_level=0)->list:
    """
    text should be a fade code.
    """
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    if debug_level > 0: print(tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    if debug_level > 1: print(ast)

    if ast is None:
        return [None]

    interpreter = Interpreter(ast, env)
    return_values = interpreter.evaluate()
    return return_values
