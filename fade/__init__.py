from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .errors import FadeError

# ##################################
# Run function to execute the code
# ##################################

def run(text:str, env):
    """
    text should be a fade code.
    """
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    if ast is None:
        return None

    interpreter = Interpreter(ast, env)
    return interpreter.evaluate()
